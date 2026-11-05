import io
import json
import os
from pathlib import Path
import sys
import threading
import urllib.error
from dataclasses import replace
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'backend'))
os.environ['DATABASE_URL'] = 'sqlite://'
from ponteUsb import Frames, Gateway, HttpApi, reading_from, sender
from main import app
from database.connection import get_db
from database.models import Base, MachineEvent


@pytest.fixture
def api(monkeypatch):
    monkeypatch.delenv('DEVICE_API_KEY', raising=False)
    monkeypatch.delenv('INGEST_API_KEY', raising=False)
    engine = create_engine('sqlite://', connect_args={'check_same_thread':False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        app.dependency_overrides[get_db] = lambda: db
        # Do not run lifespan or touch configured database/admin.
        client = TestClient(app)
        class Adapter:
            def post(self, path, body):
                response = client.post('/api'+path, json=body)
                if response.status_code >= 400:
                    raise urllib.error.HTTPError(path,response.status_code,response.text,{},None)
                return response.json()
        yield Adapter(), client, db
        client.close()
    app.dependency_overrides.clear()
    engine.dispose()


def frame():
    payload = json.loads((ROOT/'firmware/optaCncMonitor/monitorSample.json').read_text())
    payload.pop('event_id',None); payload.pop('timestamp',None)
    return {'protocol':1,'sequence':1,'uptime_ms':1000,'firmware_version':'opta-monitor-usb-2.1.1','payload':payload}


def test_chunks_registration_database_and_frontend(api):
    adapter,client,db=api
    chunks=Frames();text='CNC_JSON:'+json.dumps(frame());parsed=None
    for position in range(0,len(text),32):
        assert chunks.feed('I1 -> HIGH') is None
        parsed=chunks.feed('CNC_CHUNK:'+text[position:position+32])
    reading=reading_from(parsed)
    gateway=Gateway(adapter,mac='AA:BB:CC:DD:EE:11')
    data=gateway.payload_for(reading)
    result=gateway.send(reading,data)
    retry=gateway.send(reading,data)
    assert result['id']==retry['id']
    assert len(db.scalars(select(MachineEvent)).all())==1
    devices=client.get('/api/devices').json()
    assert len(devices)==1
    cnc=devices[0]['cnc_id']
    status=client.get(f'/api/cncs/{cnc}/status').json()
    assert status['gateway_online'] is True
    assert status['status']=='OPERANDO'
    assert status['digital_signals']==reading.payload['digital_signals']
    assert status['voltage_24v'] is None
    assert status['digital_signals']['emergencia'] is False
    assert client.get(f'/api/cncs/{cnc}/history').json()['total']==1


def test_generic_usb_event_preserves_current_and_simulation_metadata(api):
    adapter, client, _ = api
    machine = client.post('/api/cncs', json={'name': 'Corrente simulada'}).json()
    wire = frame()
    wire['payload']['analog_signals'] = {'current': 12.5}
    wire['payload']['extra_signals']['current_input']['source'] = 'simulated'
    reading = reading_from(wire)
    gateway = Gateway(adapter, machine_id=machine['code'])
    event = gateway.payload_for(reading)
    assert event['analog_signals'] == {'current': 12.5}
    assert gateway.send(reading, event)['analog_signals'] == {'current': 12.5}
    status = client.get(f"/api/cncs/{machine['id']}/status").json()
    assert status['extra_signals']['current_input']['source'] == 'simulated'
    for key, value in reading.payload['extra_signals'].items():
        assert event['extra_signals'][key] == value
        assert status['extra_signals'][key] == value
    assert event['extra_signals']['boot_id'] == gateway.session


@pytest.mark.parametrize('amps', [0, 24.0, 18.2])
def test_fixed_virtual_current_reaches_status_and_history_without_changing_ihm_states(api, amps):
    fixture = ROOT / '.build/firmware/ihm-usb-fixtures.txt'
    if not fixture.exists():
        pytest.skip('Gere ihm-usb-fixtures.txt com o teste C++ de telemetria')
    adapter, client, _ = api
    machine = client.post('/api/cncs', json={'name': 'IHM com corrente virtual'}).json()
    gateway = Gateway(adapter, machine_id=machine['id'], simulated_current=amps)
    expected_statuses = ('OPERANDO', 'PARADA', 'EMERGENCIA', 'PARADA',
                         'PARADA', 'ALARME', 'EMERGENCIA', 'EMERGENCIA')
    wires = fixture.read_text().splitlines()
    assert len(wires) == len(expected_statuses)
    for wire, expected_status in zip(wires, expected_statuses):
        parsed = Frames().feed(wire)
        reading = reading_from(parsed)
        body = gateway.payload_for(reading)
        saved = gateway.send(reading, body)
        assert saved['states'] == parsed['payload']['digital_signals']
        status = client.get(f"/api/cncs/{machine['id']}/status").json()
        assert status['status'] == expected_status
        assert status['analog_signals'] == {'current': amps}
        assert status['extra_signals']['current_input']['source'] == 'simulated'
        assert parsed['payload']['analog_signals'] == {}
    history = client.get(f"/api/cncs/{machine['id']}/history").json()
    assert history['total'] == len(wires)
    assert all(item['analog_signals'] == {'current': amps} for item in history['items'])
    assert all(item['extra_signals']['current_input']['source'] == 'simulated' for item in history['items'])


def test_existing_uuid_preserves_binding(api):
    adapter,client,db=api
    registration=adapter.post('/devices/register',{'mac_address':'AA:BB:CC:DD:EE:12'})
    gateway=Gateway(adapter,device_id=registration['device']['id'])
    reading=reading_from(frame())
    gateway.send(reading,gateway.payload_for(reading))
    assert len(client.get('/api/devices').json())==1
    assert client.get('/api/devices').json()[0]['cnc_id']==registration['cnc']['id']


def test_device_key_is_enforced(api,monkeypatch):
    adapter,client,_=api
    monkeypatch.setenv('DEVICE_API_KEY','test-key')
    assert client.post('/api/devices/register',json={'mac_address':'AA:BB:CC:DD:EE:13'}).status_code==401
    assert client.post('/api/devices/register',headers={'X-Device-Key':'test-key'},json={'mac_address':'AA:BB:CC:DD:EE:13'}).status_code==201


def test_host_session_changes_on_opta_reboot():
    gateway=Gateway(None,device_id='existing')
    reading=reading_from(frame())
    first=gateway.payload_for(reading)
    later=gateway.payload_for(replace(reading,sequence=2,uptime_ms=2000))
    reboot=gateway.payload_for(replace(reading,sequence=1,uptime_ms=1000))
    assert first['extra_signals']['boot_id']==later['extra_signals']['boot_id']
    assert reboot['event_id']!=first['event_id']


def test_serial_requires_versioned_acquisition_frame():
    with pytest.raises(ValueError, match='protocolo USB incompatível'):
        reading_from({'machine_active': True, 'digital_signals': {'em_execucao': True}})


def test_resync_and_malformed_frames():
    frames=Frames()
    assert frames.feed('CNC_CHUNK:CNC_JSON:{"truncated":') is None
    assert frames.feed('CNC_JSON:'+json.dumps(frame()))==frame()
    with pytest.raises(ValueError):reading_from({'protocol':2,'payload':{}})
    with pytest.raises(ValueError):reading_from({**frame(),'sequence':True})
    with pytest.raises(ValueError):frames.feed('CNC_JSON:{"value":NaN}')


@pytest.mark.parametrize('protocol', [True, 1.0, '1', None])
def test_usb_protocol_requires_an_integer_version(protocol):
    with pytest.raises(ValueError, match='protocolo USB incompatível'):
        reading_from({**frame(), 'protocol': protocol})


@pytest.mark.parametrize('number', ['NaN', 'Infinity', '-Infinity', '1e999', '-1e999'])
def test_usb_frames_reject_non_finite_numbers_including_exponent_overflow(number):
    with pytest.raises(ValueError, match='número não finito'):
        Frames().feed('CNC_JSON:{"analog_signals":{"current":' + number + '}}')


@pytest.mark.parametrize('response', [None, [], True, 'not an object'])
def test_http_adapter_rejects_non_object_success_responses(response, monkeypatch):
    monkeypatch.setattr('urllib.request.urlopen', lambda *args, **kwargs:
                        io.BytesIO(json.dumps(response).encode()))
    with pytest.raises(ValueError, match='resposta da API deve ser objeto JSON'):
        HttpApi('http://127.0.0.1:8000/api').post('/events', {})


@pytest.mark.parametrize('invalid', [None, [], {'device': None}, {'device': {}}, {'device': {'id': None}}])
def test_sender_recovers_from_malformed_registration_response(invalid):
    import queue
    stop = threading.Event()
    pending = queue.Queue()
    reading = reading_from(frame())
    pending.put(reading)
    calls = []
    device_id = '11111111-1111-4111-8111-111111111111'
    class RecoveringApi:
        def post(self, path, body):
            calls.append(path)
            if len(calls) == 1:
                return invalid
            if path == '/devices/register':
                return {'device': {'id': device_id}}
            stop.set()
            return {'id': 'saved'}
    class ImmediateStop:
        def is_set(self):
            return stop.is_set()
        def wait(self, seconds):
            return stop.is_set()
    gateway = Gateway(RecoveringApi(), mac='AA:BB:CC:DD:EE:51')
    sender(gateway, pending, ImmediateStop())
    assert calls == ['/devices/register', '/devices/register', f'/devices/{device_id}/telemetry']


def test_transient_retry_keeps_exact_payload():
    import queue
    stop=threading.Event();pending=queue.Queue();reading=reading_from(frame());pending.put(reading)
    calls=[]
    class Flaky:
        def payload_for(self,r):return {'event_id':'session:1','timestamp':r.captured_at}
        def send(self,r,payload):
            calls.append(dict(payload))
            if len(calls)==1:raise OSError('timeout')
            stop.set();return {'id':'saved'}
    class ImmediateStop:
        def is_set(self):return stop.is_set()
        def wait(self,seconds):return stop.is_set()
    sender(Flaky(),pending,ImmediateStop())
    assert len(calls)==2 and calls[0]==calls[1]


def test_duplicate_usb_frame_keeps_timestamp_and_event():
    gateway = Gateway(None, device_id='existing')
    first = reading_from(frame())
    again = replace(first, captured_at='2030-01-01T00:00:00Z')
    assert gateway.payload_for(first) == gateway.payload_for(again)


@pytest.mark.skipif(os.name != 'posix', reason='Ensaio de serial PTY exige POSIX/Linux')
def test_linux_serial_with_real_firmware_frame_reaches_api(api):
    """Real C++ bytes -> Linux tty -> pyserial -> bridge -> API -> SQLite."""
    import queue
    import time
    serial = pytest.importorskip('serial')
    from ponteUsb import receive
    fixture = ROOT / '.build/firmware/usb-fixture.txt'
    if not fixture.exists():
        pytest.skip('Gere usb-fixture.txt com o teste C++ de telemetria')
    wire = fixture.read_bytes()
    expected = json.loads(wire.decode().removeprefix('CNC_JSON:'))
    master, slave = os.openpty()
    pending, stop = queue.Queue(maxsize=1), threading.Event()
    errors = []
    try:
        with serial.Serial(os.ttyname(slave), 115200, timeout=0.05, exclusive=True) as port:
            def read():
                try:
                    receive(port, pending, stop)
                except Exception as error:
                    errors.append(error)
            worker = threading.Thread(target=read)
            worker.start()
            try:
                # A truncated frame is replaced by the next complete frame.
                os.write(master, b'CNC_JSON:{"protocol":\n')
                for start in range(0, len(wire), 37):
                    os.write(master, wire[start:start + 37])
                    time.sleep(0.001)
                reading = pending.get(timeout=3)
            finally:
                stop.set()
                worker.join(timeout=2)
            assert not worker.is_alive() and not errors
        adapter, client, db = api
        gateway = Gateway(adapter, mac='AA:BB:CC:DD:EE:31')
        payload = gateway.payload_for(reading)
        saved = gateway.send(reading, payload)
        assert gateway.send(reading, payload)['id'] == saved['id']
        assert len(db.scalars(select(MachineEvent)).all()) == 1
        assert saved['digital_signals'] == expected['payload']['digital_signals']
        assert saved['extra_signals']['timestamp_source'] == 'usb_host_receive'
        assert saved['extra_signals']['transport'] == 'usb_serial'
        assert saved['analog_signals'] == {} and saved['voltage_24v'] is None
        cnc = client.get('/api/devices').json()[0]['cnc_id']
        assert client.get(f'/api/cncs/{cnc}/status').json()['status'] == 'OPERANDO'
    finally:
        os.close(master)
        os.close(slave)


def test_list_ports_needs_no_identity(monkeypatch, capsys):
    from types import SimpleNamespace
    serial = pytest.importorskip('serial.tools.list_ports')
    from ponteUsb import main
    monkeypatch.setattr(sys, 'argv', ['ponteUsb.py', '--listar-portas'])
    monkeypatch.setattr(serial, 'comports', lambda: [SimpleNamespace(
        device='/dev/ttyACM0', description='Opta', serial_number='test-opta')])
    main()
    assert '/dev/ttyACM0 | Opta | serial=test-opta' in capsys.readouterr().out


def test_boolean_monitor_real_firmware_frame_reaches_api(api):
    fixture = ROOT / '.build/firmware/monitor-usb-fixture.txt'
    if not fixture.exists():
        pytest.skip('Gere monitor-usb-fixture.txt com o teste C++ de telemetria')
    frame = Frames().feed(fixture.read_text().strip())
    reading = reading_from(frame)
    adapter, client, db = api
    gateway = Gateway(adapter, mac='AA:BB:CC:DD:EE:41')
    payload = gateway.payload_for(reading)
    saved = gateway.send(reading, payload)
    assert saved['digital_signals'] == dict.fromkeys((
        'ativo', 'inativo', 'emergencia', 'motor_ligado', 'alarme', 'porta_aberta'), True)
    assert saved['machine_active'] is False
    assert saved['extra_signals']['profile'] == 'six_signals_current_reserved_v3'
    assert saved['extra_signals']['entradas_brutas'] == dict.fromkeys(
        (f'I{i}' for i in range(1, 7)), True)
    assert saved['voltage_24v'] is None and saved['analog_signals'] == {}
    assert gateway.send(reading, payload)['id'] == saved['id']
    assert len(db.scalars(select(MachineEvent)).all()) == 1
    cnc = client.get('/api/devices').json()[0]['cnc_id']
    assert client.get(f'/api/cncs/{cnc}/status').json()['status'] == 'EMERGENCIA'


def test_default_firmware_id_reaches_machine_dashboard_without_collector_registration(api):
    fixture = ROOT / '.build/firmware/monitor-usb-fixture.txt'
    if not fixture.exists():
        pytest.skip('Gere monitor-usb-fixture.txt com o teste C++ de telemetria')
    adapter, client, _ = api
    machine = client.post('/api/cncs', json={'name': 'IHM/CLP — ID 1'}).json()
    wire = Frames().feed(fixture.read_text().strip())
    assert wire['machine_id'] == '1'
    reading = reading_from(wire)
    gateway = Gateway(adapter)
    saved = gateway.send(reading, gateway.payload_for(reading))
    assert saved['machine_id'] == machine['id']
    assert saved['states'] == wire['payload']['digital_signals']
    assert client.get('/api/devices').json() == []
    status = client.get(f"/api/cncs/{machine['id']}/status").json()
    assert status['states'] == saved['states'] and status['online'] is True


def test_real_ihm_pin_frames_preserve_distinct_door_and_alarm_through_machine_api(api):
    """Actual C++ USB bytes -> bridge -> SQLite -> current and historical API."""
    fixture = ROOT / '.build/firmware/ihm-usb-fixtures.txt'
    if not fixture.exists():
        pytest.skip('Gere ihm-usb-fixtures.txt com o teste C++ de telemetria')
    wires = fixture.read_text().splitlines()
    # Independent expectations from Q0.0..Q0.5 -> I1..I6, not the firmware table.
    cases = [
        (0x01, {'ativo'}, 'OPERANDO', set(), {'ATIVIDADE_INFORMADA'}),
        (0x02, {'inativo'}, 'PARADA', set(), {'INATIVIDADE_INFORMADA'}),
        (0x04, {'emergencia'}, 'EMERGENCIA', set(), {'EMERGENCIA_ACIONADA'}),
        (0x08, {'motor_ligado'}, 'PARADA', set(), {'MOTOR_SEM_ATIVIDADE_CONFIRMADA'}),
        (0x10, {'porta_aberta'}, 'PARADA', set(), {'PORTA_ABERTA'}),
        (0x20, {'alarme'}, 'ALARME', set(), {'ALARME_ACIONADO'}),
        (0x14, {'emergencia', 'porta_aberta'}, 'EMERGENCIA',
         {'PORTA_ABERTA_EMERGENCIA'}, {'PORTA_ABERTA_EMERGENCIA'}),
        (0x24, {'emergencia', 'alarme'}, 'EMERGENCIA', set(), {'EMERGENCIA_COM_ALARME'}),
    ]
    assert len(wires) == len(cases)
    signals = ('ativo', 'inativo', 'emergencia', 'motor_ligado', 'porta_aberta', 'alarme')
    adapter, client, db = api
    machine = client.post('/api/cncs', json={'name': 'IHM Q0.0–Q0.5'}).json()
    gateway = Gateway(adapter)
    saved_readings = {}
    for sequence, (wire, case) in enumerate(zip(wires, cases), 1):
        mask, enabled, expected_status, expected_diagnostics, expected_outputs = case
        states = {signal: signal in enabled for signal in signals}
        parsed = Frames().feed(wire)
        assert parsed['sequence'] == sequence
        assert parsed['machine_id'] == '1'
        assert parsed['firmware_version'] == 'opta-monitor-usb-2.1.1'
        assert parsed['payload']['extra_signals']['profile'] == 'six_signals_current_reserved_v3'
        assert parsed['payload']['extra_signals']['entradas_brutas'] == {
            f'I{index + 1}': bool(mask & (1 << index)) for index in range(6)
        }
        assert parsed['payload']['digital_signals'] == states, f'IHM input mask {mask:#04x}'
        reading = reading_from(parsed)
        payload = gateway.payload_for(reading)
        assert payload['states'] == states
        saved = gateway.send(reading, payload)
        assert saved['machine_id'] == machine['id']
        assert saved['states'] == states
        status = client.get(f"/api/cncs/{machine['id']}/status").json()
        assert status['online'] is True
        assert status['states'] == states
        assert status['status'] == expected_status
        assert {item['code'] for item in status['diagnostics']} == expected_diagnostics
        assert {item['code'] for item in status['signal_outputs']} == expected_outputs
        fleet = client.get('/api/cncs/statuses').json()[0]
        for field in ('states', 'status', 'diagnostics', 'signal_outputs'):
            assert fleet[field] == status[field]
        saved_readings[saved['id']] = {
            'states': states,
            'machine_active': mask == 0x01,
            'signal_outputs': status['signal_outputs'],
        }
    assert client.get('/api/devices').json() == []
    assert len(db.scalars(select(MachineEvent)).all()) == len(cases)
    for endpoint in (f"/api/cncs/{machine['id']}/history", '/api/cncs/history'):
        history = client.get(endpoint).json()
        assert history['total'] == len(cases)
        assert [item['id'] for item in history['items']] == list(reversed(saved_readings))
        for item in history['items']:
            assert item['machine_id'] == machine['id']
            for field, expected in saved_readings[item['id']].items():
                assert item[field] == expected
