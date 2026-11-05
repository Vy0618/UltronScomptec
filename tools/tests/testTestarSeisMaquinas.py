"""Run the Windows fleet tutorial against the real API with isolated SQLite."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'backend'))
from main import app
from database.connection import get_db
from database.models import Base, CNC, MachineEvent


@pytest.mark.skipif(os.name != 'nt', reason='Tutorial script uses Windows PowerShell')
@pytest.mark.parametrize('ingest_key', ['', 'fleet-test-key'])
def test_fleet_script_reuses_six_machines_and_appends_valid_history(monkeypatch, ingest_key):
    shell = shutil.which('powershell.exe')
    if not shell:
        pytest.skip('Windows PowerShell is not installed')
    monkeypatch.setenv('INGEST_API_KEY', ingest_key)
    monkeypatch.delenv('DEVICE_API_KEY', raising=False)
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        app.dependency_overrides[get_db] = lambda: db
        client = TestClient(app)  # No lifespan: never connect to an installation database.

        class Adapter(BaseHTTPRequestHandler):
            def respond(self):
                body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
                headers = {name: self.headers[name] for name in ('Content-Type', 'X-API-Key') if name in self.headers}
                response = client.request(self.command, self.path, content=body or None, headers=headers)
                self.send_response(response.status_code)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(response.content)))
                self.end_headers()
                self.wfile.write(response.content)

            do_GET = respond
            do_POST = respond

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(('127.0.0.1', 0), Adapter)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            def run(rounds):
                command = [
                    shell, '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
                    '-File', str(ROOT / 'tools/testarSeisMaquinas.ps1'),
                    '-Api', f'http://127.0.0.1:{server.server_port}/api',
                    '-Rodadas', str(rounds), '-IntervaloSegundos', '0',
                ]
                if ingest_key:
                    command += ['-Chave', ingest_key]
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, errors='replace', timeout=40)
                assert result.returncode == 0, result.stdout + result.stderr

            run(0)
            first_ids = set(db.scalars(select(CNC.id)).all())
            assert len(first_ids) == 6
            assert db.scalar(select(func.count()).select_from(MachineEvent)) == 0
            run(2)
            assert set(db.scalars(select(CNC.id)).all()) == first_ids
            assert db.scalar(select(func.count()).select_from(MachineEvent)) == 12
            run(1)
            assert set(db.scalars(select(CNC.id)).all()) == first_ids
            readings = db.scalars(select(MachineEvent)).all()
            assert len(readings) == 18 and len({row.id for row in readings}) == 18
            assert all(set(row.digital_signals) == {
                'ativo', 'inativo', 'emergencia', 'motor_ligado', 'porta_aberta', 'alarme',
            } for row in readings)
            assert all(all(isinstance(value, bool) for value in row.digital_signals.values()) for row in readings)
            assert all(row.extra_signals['source'] == 'simulated' for row in readings)
            assert all(row.analog_signals == {} for row in readings)
            assert any(row.digital_signals['porta_aberta'] and row.digital_signals['emergencia'] for row in readings)
            assert any(row.digital_signals['alarme'] for row in readings)
            assert {row['status'] for row in client.get('/api/cncs/statuses').json()} == {
                'OPERANDO', 'PARADA', 'EMERGENCIA', 'ALARME',
            }
            assert client.get('/api/cncs/history').json()['total'] == 18
            for machine_id in first_ids:
                assert client.get(f'/api/cncs/{machine_id}/history').json()['total'] == 3
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=3)
            client.close()
            app.dependency_overrides.clear()
    engine.dispose()
