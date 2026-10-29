"""Machine events work with no device, hardware metadata or hardware service."""
from datetime import datetime, timedelta
from pathlib import Path
import sys
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import app
from database.connection import get_db
from database.models import Base, CNC, Device, MachineEvent, Telemetry
from services import clock, cncService, events, telemetry


@pytest.fixture
def event_api(monkeypatch):
    monkeypatch.delenv('DEVICE_API_KEY', raising=False)
    monkeypatch.delenv('INGEST_API_KEY', raising=False)
    current = [datetime(2026, 10, 29, 12, 0, 0)]
    for module in (clock, cncService, events, telemetry):
        monkeypatch.setattr(module, 'utcnow', lambda: current[0])
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        app.dependency_overrides[get_db] = lambda: db
        client = TestClient(app)
        machine = client.post('/api/cncs', json={'name': 'Máquina de teste'}).json()
        yield client, db, machine, current
        client.close()
    app.dependency_overrides.clear()
    engine.dispose()


def send(client, machine, states, **options):
    return client.post('/api/events', json={'machine_id': machine['id'], 'states': states, **options})


def test_minimal_event_updates_dashboard_history_and_utilization_without_a_device(event_api):
    client, db, machine, _ = event_api
    response = send(client, machine, {'em_execucao': True, 'alarme': False})
    assert response.status_code == 201, response.text
    result = response.json()
    assert result['machine_id'] == machine['id']
    assert result['states'] == {'em_execucao': True, 'alarme': False}
    assert 'device_id' not in result
    assert db.scalar(select(func.count()).select_from(Device)) == 0
    assert db.scalar(select(func.count()).select_from(Telemetry)) == 0
    status = client.get(f"/api/cncs/{machine['id']}/status").json()
    assert status['online'] is True and status['status'] == 'OPERANDO'
    assert status['states'] == result['states']
    history = client.get(f"/api/cncs/{machine['id']}/history").json()
    assert history['total'] == 1 and history['items'][0]['machine_id'] == machine['id']
    assert history['items'][0]['states'] == result['states']
    assert client.get(f"/api/cncs/{machine['id']}/utilization").status_code == 200


def test_default_arduino_id_one_resolves_to_first_machine(event_api):
    client, _, machine, _ = event_api
    response = client.post('/api/events', json={'machine_id': '1', 'states': {'em_execucao': True}})
    assert response.status_code == 201
    assert response.json()['machine_id'] == machine['id']


@pytest.mark.parametrize(('state', 'expected'), [
    ('em_execucao', 'OPERANDO'), ('pausa', 'PARADA'), ('parada', 'PARADA'),
    ('emergencia', 'EMERGENCIA'), ('motor_ligado', 'PARADA'), ('automatico', 'PARADA'),
    ('manual', 'PARADA'), ('alarme', 'ALARME'),
])
def test_each_observed_state_is_preserved_without_pin_mapping(event_api, state, expected):
    client, _, machine, _ = event_api
    result = client.post('/api/events', json={'machine_id': machine['code'], 'states': {state: True}})
    assert result.status_code == 201
    assert result.json()['machine_id'] == machine['id']
    status = client.get(f"/api/cncs/{machine['id']}/status").json()
    assert status['states'] == {state: True}
    assert status['status'] == expected


def test_new_snapshot_does_not_invent_or_merge_missing_states(event_api):
    client, _, machine, _ = event_api
    assert send(client, machine, {'emergencia': True, 'alarme': True}).status_code == 201
    assert send(client, machine, {'porta_aberta': False}).status_code == 201
    status = client.get(f"/api/cncs/{machine['id']}/status").json()
    assert status['states'] == {'porta_aberta': False}


def test_idempotency_is_machine_scoped_and_retries_do_not_keep_machine_online(event_api):
    client, db, machine, current = event_api
    second = client.post('/api/cncs', json={'name': 'Outra máquina'}).json()
    first = send(client, machine, {'alarme': True}, event_id='test-1')
    current[0] += timedelta(seconds=clock.OFFLINE_TIMEOUT_SECONDS + 1)
    retry = send(client, machine, {'alarme': True}, event_id='test-1')
    assert first.json()['id'] == retry.json()['id']
    assert client.get(f"/api/cncs/{machine['id']}/status").json()['status'] == 'SEM_COMUNICACAO'
    assert send(client, machine, {'alarme': False}, event_id='test-1').status_code == 409
    different = send(client, second, {'alarme': True}, event_id='test-1')
    assert different.status_code == 201 and different.json()['id'] != first.json()['id']
    assert db.scalar(select(func.count()).select_from(MachineEvent)) == 2


def test_same_second_events_follow_arrival_order_and_historical_delivery_does_not_revert(event_api):
    client, _, machine, current = event_api
    for index in range(6):
        states = {'em_execucao': index % 2 == 0, 'alarme': index % 2 == 1}
        result = send(client, machine, states, event_id=f'order-{index}')
        assert result.status_code == 201
        status = client.get(f"/api/cncs/{machine['id']}/status").json()
        assert status['states'] == states
        latest = client.get(f"/api/cncs/{machine['id']}/history?limit=1").json()['items'][0]
        assert latest['id'] == result.json()['id']
    send(client, machine, {'alarme': False}, timestamp=(current[0] - timedelta(hours=2)).isoformat() + 'Z')
    assert client.get(f"/api/cncs/{machine['id']}/status").json()['status'] == 'ALARME'


def test_stale_collection_and_offline_recover_without_a_collector(event_api):
    client, _, machine, current = event_api
    send(client, machine, {'emergencia': True}, timestamp=(current[0] - timedelta(hours=1)).isoformat() + 'Z')
    status = client.get(f"/api/cncs/{machine['id']}/status").json()
    assert status['online'] is True and status['status'] == 'DADOS_DESATUALIZADOS'
    current[0] += timedelta(seconds=clock.OFFLINE_TIMEOUT_SECONDS + 1)
    assert client.get(f"/api/cncs/{machine['id']}/status").json()['status'] == 'SEM_COMUNICACAO'
    resumed = send(client, machine, {'emergencia': True})
    status = client.get(f"/api/cncs/{machine['id']}/status").json()
    assert status['status'] == 'EMERGENCIA' and status['status_since'] == resumed.json()['timestamp']


@pytest.mark.parametrize('changes', [
    {'states': {}}, {'states': {'alarme': 'false'}}, {'states': {'alarme': 1}},
    {'states': {'alarme': None}}, {'states': []}, {'states': None},
    {'machine_id': ''}, {'machine_id': None}, {'unexpected': 'field'},
])
def test_invalid_contract_is_rejected_without_persistence(event_api, changes):
    client, db, machine, _ = event_api
    result = client.post('/api/events', json={'machine_id': machine['id'], 'states': {'alarme': True}, **changes})
    assert result.status_code == 422
    assert db.scalar(select(func.count()).select_from(MachineEvent)) == 0


def test_unknown_machine_future_timestamp_and_optional_key(event_api, monkeypatch):
    client, _, machine, current = event_api
    assert send(client, {'id': str(uuid4())}, {'alarme': True}).status_code == 404
    assert send(client, machine, {'alarme': True}, timestamp=(current[0] + timedelta(seconds=61)).isoformat() + 'Z').status_code == 422
    monkeypatch.setenv('INGEST_API_KEY', 'test-events')
    assert send(client, machine, {'alarme': True}).status_code == 401
    result = client.post('/api/events', headers={'X-API-Key': 'test-events'}, json={'machine_id': machine['code'], 'states': {'alarme': True}})
    assert result.status_code == 201


def test_removing_collector_preserves_machine_history_and_machine_keeps_receiving(event_api):
    client, _, machine, _ = event_api
    device = client.post('/api/devices', json={'name': 'Coletor opcional', 'mac_address': '02:00:00:00:00:01', 'cnc_id': machine['id']}).json()
    assert client.post(f"/api/devices/{device['id']}/telemetry", json={'machine_active': True}).status_code == 201
    assert client.delete(f"/api/devices/{device['id']}").status_code == 204
    assert send(client, machine, {'alarme': True}).status_code == 201
    assert client.get(f"/api/cncs/{machine['id']}/history").json()['total'] == 2
    assert client.get(f"/api/cncs/{machine['id']}/status").json()['status'] == 'ALARME'
    assert client.delete(f"/api/cncs/{machine['id']}").status_code == 204
    assert client.get('/api/cncs').json() == []


def test_existing_telemetry_is_readable_and_preserved_when_its_collector_is_deleted(event_api):
    client, db, machine, current = event_api
    device = client.post('/api/devices', json={'name': 'Coletor antigo', 'mac_address': '02:00:00:00:00:02', 'cnc_id': machine['id']}).json()
    legacy = Telemetry(device_id=device['id'], timestamp=current[0], received_at=current[0], machine_active=True, digital_signals={'ciclo': True}, analog_signals={}, extra_signals={})
    db.add(legacy)
    db.commit()
    original_id = legacy.id
    assert client.get(f"/api/cncs/{machine['id']}/history").json()['total'] == 1
    # Same-second migration must not put the old observation ahead of a new one.
    assert send(client, machine, {'em_execucao': False}).status_code == 201
    assert client.delete(f"/api/devices/{device['id']}").status_code == 204
    history = client.get(f"/api/cncs/{machine['id']}/history").json()
    assert history['total'] == 2 and history['items'][1]['id'] == original_id
    assert client.get(f"/api/cncs/{machine['id']}/status").json()['states'] == {'em_execucao': False}
    assert send(client, machine, {'alarme': True}).status_code == 201
    assert client.get(f"/api/cncs/{machine['id']}/history").json()['total'] == 3
