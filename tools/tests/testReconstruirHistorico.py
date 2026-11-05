"""Reconstructed history must stay identifiable and preserve existing readings."""
import copy
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'backend'))
# Importing the backend must never read local configuration or open MySQL.
os.environ['ULTRON_SIMULATION'] = 'true'
os.environ['DATABASE_URL'] = 'sqlite://'
from reconstruirHistorico import apply_plan, build_plan, event_payload, parse_time
from main import app
from database.connection import get_db
from database.models import Base, MachineEvent

EXPECTED_SIGNALS = {'ativo', 'inativo', 'emergencia', 'motor_ligado', 'porta_aberta', 'alarme'}
START = datetime(2024, 1, 10, 10, tzinfo=timezone.utc)
END = START + timedelta(hours=4)
NAMES = ['Siemens S7-300', 'Siemens S7-1200']


@pytest.fixture
def plan():
    return build_plan(START, END, NAMES)


def test_four_hour_plan_has_exact_boundaries_short_pauses_and_continuous_coverage(plan):
    assert (parse_time(plan['end']) - parse_time(plan['start'])).total_seconds() == 14400
    assert plan['source'] == 'reconstructed'
    assert len(plan['machines']) == 2
    schedules = []
    for index, machine in enumerate(plan['machines']):
        events = [event_payload(plan, index, record, 'target-id') for record in machine['records']]
        times = [parse_time(event['timestamp']) for event in events]
        assert times[0] == START and times[-1] == END
        assert times == sorted(set(times))
        assert all(0 < (right - left).total_seconds() <= 30 for left, right in zip(times, times[1:]))
        pause_start = None
        observed_pauses = []
        active_seconds = 0
        for left, right in zip(events, events[1:]):
            left_time, right_time = parse_time(left['timestamp']), parse_time(right['timestamp'])
            if left['states']['ativo']:
                active_seconds += (right_time - left_time).total_seconds()
            elif pause_start is None:
                pause_start = left_time
            if pause_start is not None and right['states']['ativo']:
                observed_pauses.append((pause_start, right_time))
                pause_start = None
        assert pause_start is None
        assert observed_pauses
        assert all(4 <= (finish - begin).total_seconds() <= 12 for begin, finish in observed_pauses)
        idle_seconds = sum((finish - begin).total_seconds() for begin, finish in observed_pauses)
        assert active_seconds + idle_seconds == 14400
        assert active_seconds / 14400 > .98
        assert machine['active_seconds'] == active_seconds
        assert machine['idle_seconds'] == idle_seconds
        schedules.append(observed_pauses)
    assert schedules[0] != schedules[1]


def test_every_event_has_six_boolean_states_and_reconstruction_origin_without_current(plan):
    ids = []
    for index, machine in enumerate(plan['machines']):
        for record in machine['records']:
            event = event_payload(plan, index, record, f'machine-{index}')
            states = event['states']
            assert set(states) == EXPECTED_SIGNALS
            assert all(type(value) is bool for value in states.values())
            assert states['inativo'] is not states['ativo']
            assert states['motor_ligado'] is states['ativo']
            assert not any(states[key] for key in ('emergencia', 'porta_aberta', 'alarme'))
            assert event['machine_id'] == f'machine-{index}'
            assert event['analog_signals'] == {}
            assert event['extra_signals'] == {
                'source': 'reconstructed', 'batch_id': plan['batch_id'], 'scenario': 'history-restoration',
            }
            assert 'simulated' not in json.dumps(event)
            ids.append(event['event_id'])
    assert len(ids) == len(set(ids))


def test_same_configuration_is_deterministic_and_seed_changes_the_reconstruction(plan):
    assert json.loads(json.dumps(plan)) == json.loads(json.dumps(build_plan(START, END, NAMES)))
    shifted_zone = timezone(timedelta(hours=-3))
    assert build_plan(START.astimezone(shifted_zone), END.astimezone(shifted_zone), NAMES) == plan
    changed = build_plan(START, END, NAMES, seed=43)
    assert changed['batch_id'] != plan['batch_id']
    assert [machine['pauses'] for machine in changed['machines']] != [machine['pauses'] for machine in plan['machines']]


@pytest.mark.parametrize('corruption', ['source', 'state', 'time'])
def test_modified_plan_is_rejected_before_any_api_access(plan, corruption):
    modified = copy.deepcopy(plan)
    if corruption == 'source':
        modified['source'] = 'simulated'
    elif corruption == 'state':
        modified['machines'][0]['records'][0]['active'] = False
    else:
        modified['machines'][0]['records'][0]['offset'] = 1

    class NoApiAccess:
        def request(self, *args, **kwargs):
            pytest.fail('A modified plan must not access the API')

    with pytest.raises(ValueError, match='plano foi alterado'):
        apply_plan(NoApiAccess(), modified)


@pytest.fixture
def api(monkeypatch):
    monkeypatch.delenv('DEVICE_API_KEY', raising=False)
    monkeypatch.delenv('INGEST_API_KEY', raising=False)
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    previous_overrides = dict(app.dependency_overrides)
    try:
        with Session(engine) as db:
            app.dependency_overrides[get_db] = lambda: db
            # Deliberately omit the lifespan context: never run installation startup.
            client = TestClient(app)

            class ApiAdapter:
                def __init__(self):
                    self.requests = []

                def request(self, method, path, body=None):
                    self.requests.append((method, path))
                    response = client.request(method, '/api' + path, json=body)
                    assert response.status_code < 400, (method, path, response.status_code, response.text)
                    return response.json()

            try:
                yield ApiAdapter(), client, db
            finally:
                client.close()
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous_overrides)
        engine.dispose()


def all_history(adapter, machine_id):
    first = adapter.request('GET', f'/cncs/{machine_id}/history?limit=500')
    items = list(first['items'])
    for page in range(2, (first['total'] + 499) // 500 + 1):
        items.extend(adapter.request('GET', f'/cncs/{machine_id}/history?limit=500&page={page}')['items'])
    assert len(items) == first['total']
    return {item['id']: item for item in items}


def test_apply_plan_reuses_target_replays_idempotently_and_preserves_all_other_history(api, plan):
    adapter, client, db = api
    target = adapter.request('POST', '/cncs', {'name': NAMES[0]})
    unrelated = adapter.request('POST', '/cncs', {'name': 'Outra CNC com historico real'})

    def existing_event(machine_id, timestamp, suffix, emergency=False):
        states = dict.fromkeys(EXPECTED_SIGNALS, False)
        states.update(inativo=True, emergencia=emergency)
        return adapter.request('POST', '/events', {
            'machine_id': machine_id, 'states': states, 'timestamp': timestamp.isoformat(),
            'event_id': 'existing-' + suffix, 'analog_signals': {'current': 7.6},
            'extra_signals': {'source': 'received', 'preserve': suffix},
        })

    existing_event(target['id'], START - timedelta(hours=1), 'before')
    existing_event(target['id'], START + timedelta(minutes=20, seconds=1), 'inside')
    newer = existing_event(target['id'], END + timedelta(hours=1), 'newer', emergency=True)
    existing_event(unrelated['id'], START + timedelta(hours=1), 'unrelated')
    target_before = all_history(adapter, target['id'])
    unrelated_before = all_history(adapter, unrelated['id'])
    progress = []
    first = apply_plan(adapter, plan, lambda done, total: progress.append((done, total)))
    expected_total = sum(len(machine['records']) for machine in plan['machines'])
    assert progress[-1] == (expected_total, expected_total)
    assert first[0]['id'] == target['id'] and first[0]['created'] is False
    assert first[1]['created'] is True
    assert [item['window_count_before'] for item in first] == [1, 0]
    assert len(adapter.request('GET', '/cncs')) == 3
    stored_after_first = [all_history(adapter, machine['id']) for machine in first]
    for index, result in enumerate(first):
        assert result['verified_events'] == len(plan['machines'][index]['records'])
        assert result['window_count_after'] == result['verified_events'] + (1 if index == 0 else 0)
        assert result['active_seconds'] + result['idle_seconds'] == 14400
        assert result['idle_seconds'] == plan['machines'][index]['idle_seconds']
        reconstructed = [item for item in stored_after_first[index].values()
                         if item['extra_signals'].get('batch_id') == plan['batch_id']]
        assert len(reconstructed) == result['verified_events']
        assert all(item['extra_signals']['source'] == 'reconstructed' for item in reconstructed)
        assert all(item['analog_signals'] == {} for item in reconstructed)
        assert all(set(item['digital_signals']) == EXPECTED_SIGNALS for item in reconstructed)
    assert any('page=2' in path for method, path in adapter.requests if method == 'GET')
    assert db.scalar(select(func.count()).select_from(MachineEvent)) == expected_total + 4

    second = apply_plan(adapter, json.loads(json.dumps(plan)))
    assert [item['id'] for item in second] == [item['id'] for item in first]
    assert all(item['created'] is False for item in second)
    assert [item['window_count_before'] for item in second] == [item['window_count_after'] for item in first]
    assert [item['window_count_after'] for item in second] == [item['window_count_after'] for item in first]
    assert [all_history(adapter, item['id']) for item in second] == stored_after_first
    assert db.scalar(select(func.count()).select_from(MachineEvent)) == expected_total + 4
    for event_id, item in target_before.items():
        assert all_history(adapter, target['id'])[event_id] == item
    assert all_history(adapter, unrelated['id']) == unrelated_before
    status = client.get(f"/api/cncs/{target['id']}/status").json()
    assert status['telemetry_timestamp'] == newer['timestamp']
    assert status['last_known_status'] == 'EMERGENCIA'
