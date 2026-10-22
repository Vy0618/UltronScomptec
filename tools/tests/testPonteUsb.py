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
from database.models import Base, Telemetry


@pytest.fixture
def api(monkeypatch):
    monkeypatch.delenv('DEVICE_API_KEY', raising=False)
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
    payload = json.loads((ROOT/'firmware/optaMesaMonitor/mesaSample.json').read_text())
    payload.pop('event_id',None); payload.pop('timestamp',None)
    return {'protocol':1,'sequence':1,'uptime_ms':1000,'firmware_version':'mesa-opta-usb-1.1.0','payload':payload}


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
    assert len(db.scalars(select(Telemetry)).all())==1
    devices=client.get('/api/devices').json()
    assert len(devices)==1
    cnc=devices[0]['cnc_id']
    status=client.get(f'/api/cncs/{cnc}/status').json()
    assert status['gateway_online'] is True
    assert status['status']=='OPERANDO'
    assert status['extra_signals']['mesa']==reading.payload['extra_signals']['mesa']
    assert status['voltage_24v'] is None
    assert 'emergencia' not in status['digital_signals']
    assert client.get(f'/api/cncs/{cnc}/history').json()['total']==1


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


def test_simulator_contract_maps_into_zip_contract(api):
    adapter,client,_=api
    reading=reading_from({'sequencia':1,'uptime_ms':1000,'machine_active':True,
        'digital_signals':{'ciclo':True,'alarme':False,'emergencia':None},
        'contadores':{'iniciadas':3,'reto':1,'queda1':1,'queda2':0,'falhas':1},
        'estado':'coletando_altura','entradas':{'I2':False},'saidas':{'O1':True}})
    assert 'emergencia' not in reading.payload['digital_signals']
    assert reading.payload['extra_signals']['mesa']['contadores']['total']==3
    gateway=Gateway(adapter,mac='AA:BB:CC:DD:EE:14')
    assert gateway.send(reading,gateway.payload_for(reading))['extra_signals']['mesa']['entradas_brutas']=={'I2':False}


def test_resync_and_malformed_frames():
    frames=Frames()
    assert frames.feed('CNC_CHUNK:CNC_JSON:{"truncated":') is None
    assert frames.feed('CNC_JSON:'+json.dumps(frame()))==frame()
    with pytest.raises(ValueError):reading_from({'protocol':2,'payload':{}})
    with pytest.raises(ValueError):reading_from({**frame(),'sequence':True})
    with pytest.raises(ValueError):frames.feed('CNC_JSON:{"value":NaN}')


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
        assert len(db.scalars(select(Telemetry)).all()) == 1
        assert saved['extra_signals']['mesa'] == expected['payload']['extra_signals']['mesa']
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
