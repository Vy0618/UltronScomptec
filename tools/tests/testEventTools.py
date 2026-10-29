"""Contract tests for composable JSON Lines producers and consumers."""
import io
import json
from pathlib import Path
import subprocess
import sys
import urllib.error

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'backend'))
from publicarEventos import main as publish
from schemas.event import EventCreate
from ponteUsb import Gateway, StdoutEvents, reading_from


def test_simulator_emits_valid_envelopes_without_network_or_collector_identity():
    result = subprocess.run([sys.executable, str(ROOT / 'tools/simuladorCnc.py'),
        '--machine-id', 'CNC-001', '--state', 'cycle', '--count', '8', '--interval', '0'],
        capture_output=True, text=True, check=True)
    assert result.stderr == ''
    events = [EventCreate.model_validate_json(line) for line in result.stdout.splitlines()]
    assert len(events) == 8 and len({event.event_id for event in events}) == 8
    assert all(event.machine_id == 'CNC-001' for event in events)
    assert {next(key for key, active in event.states.items() if active) for event in events} == {
        'em_execucao', 'pausa', 'parada', 'emergencia', 'motor_ligado', 'automatico', 'manual', 'alarme'}


def test_publisher_reads_json_lines_and_keeps_responses_in_stdout(monkeypatch, capsys):
    body = {'machine_id': 'CNC-001', 'states': {'alarme': True}}
    monkeypatch.setattr(sys, 'stdin', io.StringIO(json.dumps(body) + '\n\n'))
    requests = []
    def send(request, timeout):
        requests.append(request)
        return io.BytesIO(json.dumps({'id': 'accepted', **body}).encode())
    monkeypatch.setattr('urllib.request.urlopen', send)
    assert publish(['--api', 'http://127.0.0.1:8001/api', '--key', 'test']) == 0
    output = capsys.readouterr()
    assert output.err == '' and json.loads(output.out)['id'] == 'accepted'
    assert requests[0].full_url == 'http://127.0.0.1:8001/api/events'
    assert json.loads(requests[0].data) == body
    assert requests[0].get_header('X-api-key') == 'test'


@pytest.mark.parametrize('line', ['not json', '[]', '{"machine_id":"x","states":{"a":NaN}}'])
def test_invalid_publisher_input_stops_with_stderr_and_nonzero_exit(monkeypatch, capsys, line):
    monkeypatch.setattr(sys, 'stdin', io.StringIO(line + '\n'))
    assert publish([]) == 1
    output = capsys.readouterr()
    assert output.out == '' and 'Linha 1:' in output.err


def test_api_rejection_is_reported_without_fabricating_a_success(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'stdin', io.StringIO('{"machine_id":"missing","states":{"alarme":true}}\n'))
    def reject(*args, **kwargs):
        raise urllib.error.HTTPError('url', 404, 'Not Found', {}, io.BytesIO(b'{"detail":"unknown machine"}'))
    monkeypatch.setattr('urllib.request.urlopen', reject)
    assert publish([]) == 1
    output = capsys.readouterr()
    assert output.out == '' and 'unknown machine' in output.err


def test_serial_adapter_can_emit_the_same_machine_envelope_without_calling_api(capsys):
    payload = json.loads((ROOT/'firmware/optaCncMonitor/monitorSample.json').read_text())
    reading = reading_from({'protocol': 1, 'sequence': 1, 'uptime_ms': 1000, 'payload': payload})
    gateway = Gateway(StdoutEvents(), machine_id='CNC-001')
    envelope = gateway.payload_for(reading)
    gateway.send(reading, envelope)
    output = capsys.readouterr()
    event = EventCreate.model_validate_json(output.out)
    assert event.machine_id == 'CNC-001'
    assert event.states == payload['digital_signals']
    assert output.err == ''


def test_serial_default_uses_machine_identity_from_firmware_without_cli_mapping(capsys):
    payload = json.loads((ROOT/'firmware/optaCncMonitor/monitorSample.json').read_text())
    reading = reading_from({'protocol': 1, 'machine_id': '1', 'sequence': 1, 'uptime_ms': 1000, 'payload': payload})
    gateway = Gateway(StdoutEvents())
    gateway.send(reading, gateway.payload_for(reading))
    event = EventCreate.model_validate_json(capsys.readouterr().out)
    assert event.machine_id == '1' and event.states == payload['digital_signals']
