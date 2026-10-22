"""WiFi contract integration without a physical Opta or a real MySQL database."""
import os
import json
from pathlib import Path
import sys
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "tools"))
os.environ["DATABASE_URL"] = "sqlite://"

from main import app
from database.connection import get_db
from database.models import Base, Device, Telemetry
from services import clock, cncService, deviceService, telemetry
from schemas import device as device_schema
from simuladorWifi import OptaSimulator, Response, run_scenario


@pytest.fixture
def wifi_api(monkeypatch):
    monkeypatch.delenv("DEVICE_API_KEY", raising=False)
    current = [datetime(2026, 10, 21, 12, 0, 0)]
    for module in (clock, cncService, deviceService, telemetry):
        monkeypatch.setattr(module, "utcnow", lambda: current[0])
    monkeypatch.setattr(device_schema, "time", lambda: current[0].replace(tzinfo=timezone.utc).timestamp())
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)

    def database_session():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = database_session
    # No context manager: do not run application startup against configured DB/admin.
    client = TestClient(app)

    class Adapter:
        def request(self, method, path, payload=None):
            response = client.request(method, "/api" + path, json=payload)
            return Response(response.status_code, response.json())

    def advance(seconds):
        current[0] += timedelta(seconds=seconds)

    yield Adapter(), client, engine, current, advance
    client.close()
    app.dependency_overrides.clear()
    engine.dispose()


def simulator_for(api, current):
    return OptaSimulator(api, mac="02:55:4C:54:52:01", now=lambda: current[0].replace(tzinfo=timezone.utc))


def test_full_wifi_scenario_preserves_data_and_recovers(wifi_api):
    api, client, engine, current, advance = wifi_api
    simulator, report = run_scenario(
        api, mac="02:55:4C:54:52:02", offline_timeout=clock.OFFLINE_TIMEOUT_SECONDS,
        sleep=advance, now=lambda: current[0].replace(tzinfo=timezone.utc),
    )
    assert report["simulation"] is True and report["hardware_verified"] is False
    assert report["samples"] == 13
    assert all(check["passed"] for check in report["checks"])
    assert {check["name"] for check in report["checks"]} >= {
        "404_recadastra_sem_duplicar", "resposta_perdida_reenvio_idempotente",
        "reboot_nova_sessao_mesma_cnc", "pausa_detecta_sem_comunicacao",
        "horario_de_captura_preservado", "sensores_ausentes_sem_dados_inventados",
    }
    assert simulator.status()["status"] == "OPERANDO"
    with Session(engine) as db:
        devices = db.scalars(select(Device)).all()
        assert len(devices) == 1
        assert devices[0].name.startswith("SIMULADO") and devices[0].cnc.name.startswith("SIMULADO")
        readings = db.scalars(select(Telemetry)).all()
        assert len(readings) == 13
        assert all(reading.voltage_24v is None and reading.analog_signals == {} for reading in readings)


def test_collection_clock_skew_uses_ingestion_tolerance(wifi_api):
    api, client, _, current, _ = wifi_api
    simulator = simulator_for(api, current)
    simulator.register()
    payload = simulator.prepare("aguardando_reto")
    payload["timestamp"] = (current[0] + timedelta(seconds=30)).isoformat() + "Z"
    simulator.send(payload)
    snapshot = simulator.status()
    assert snapshot["status"] == "OPERANDO"
    assert snapshot["gateway_online"] is True
    assert snapshot["status_duration_seconds"] == 0
    assert clock.is_online(current[0] + timedelta(seconds=30)) is False
    payload = simulator.prepare("falha")
    payload["timestamp"] = (current[0] + timedelta(seconds=61)).isoformat() + "Z"
    assert client.post(f"/api/devices/{simulator.device_id}/telemetry", json=payload).status_code == 422


@pytest.mark.parametrize("gap_type", ["communication", "collection"])
def test_same_state_after_observation_gap_starts_a_new_duration(wifi_api, gap_type):
    api, _, _, current, advance = wifi_api
    simulator = simulator_for(api, current)
    simulator.register()
    first = simulator.send(simulator.prepare("aguardando_reto"))
    advance(clock.OFFLINE_TIMEOUT_SECONDS + 1)
    if gap_type == "collection":
        # Gateway is online, but it only delivers a historical sample.
        simulator.send(simulator.prepare("aguardando_reto", delay_seconds=clock.OFFLINE_TIMEOUT_SECONDS + 5))
        assert simulator.status()["status"] == "DADOS_DESATUALIZADOS"
    else:
        assert simulator.status()["status"] == "SEM_COMUNICACAO"
    resumed = simulator.send(simulator.prepare("aguardando_reto"))
    snapshot = simulator.status()
    assert snapshot["status"] == "OPERANDO"
    assert snapshot["status_since"] == resumed["timestamp"] != first["timestamp"]
    assert snapshot["status_duration_seconds"] == 0


def test_continuous_heartbeats_preserve_state_duration(wifi_api):
    api, _, _, current, advance = wifi_api
    simulator = simulator_for(api, current)
    simulator.register()
    first = simulator.send(simulator.prepare("aguardando_reto"))
    advance(5)
    simulator.send(simulator.prepare("aguardando_reto"))
    assert simulator.status()["status_since"] == first["timestamp"]
    assert simulator.status()["status_duration_seconds"] == 5


def test_renaming_offline_cnc_returns_effective_status(wifi_api):
    api, client, _, current, advance = wifi_api
    simulator = simulator_for(api, current)
    simulator.register()
    simulator.send(simulator.prepare("aguardando_reto"))
    advance(clock.OFFLINE_TIMEOUT_SECONDS + 1)
    response = client.put(f"/api/cncs/{simulator.cnc_id}", json={"name": "Mesa simulada"})
    assert response.status_code == 200
    assert response.json()["status"] == "SEM_COMUNICACAO"
    assert response.json()["status_since"] == simulator.status()["status_since"]


def test_payloads_from_real_firmware_serializer_reach_database(wifi_api):
    fixture_path = ROOT / ".build/firmware/telemetry-fixtures.json"
    if not fixture_path.exists():
        pytest.skip("Execute firmware/testarFirmware.ps1 para gerar os payloads pelo serializador C++ real")
    payloads = json.loads(fixture_path.read_text(encoding="utf-8"))
    assert isinstance(payloads, list) and len(payloads) == 6
    api, _, engine, current, _ = wifi_api
    simulator = simulator_for(api, current)
    simulator.register()
    ids = []
    for payload in payloads:
        # Preserve the C++ JSON body and align the server clock, not the payload.
        current[0] = datetime.fromisoformat(payload["timestamp"].replace("Z", "+00:00")).replace(tzinfo=None, microsecond=0)
        result = simulator.send(payload)
        ids.append(result["id"])
        assert result["digital_signals"] == payload["digital_signals"]
        assert result["extra_signals"] == payload["extra_signals"]
        assert result["analog_signals"] == {} and result["voltage_24v"] is None
        snapshot = simulator.status()
        expected_status = "ALARME" if payload["digital_signals"]["alarme"] else ("OPERANDO" if payload["machine_active"] else "PARADA")
        assert snapshot["status"] == expected_status
        assert snapshot["extra_signals"]["mesa"] == payload["extra_signals"]["mesa"]
    assert simulator.send(payloads[0])["id"] == ids[0]
    with Session(engine) as db:
        assert len(db.scalars(select(Telemetry)).all()) == len(payloads)
