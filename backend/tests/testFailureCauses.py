"""Fault occurrences are parameter activations, independent of sample frequency."""
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services.machineState import IHM_SIGNALS
from services.utilization import calculate_utilization

NOW = datetime(2026, 11, 5, 15)


def reading(seconds_ago, *, voltage=None, **states):
    return SimpleNamespace(timestamp=NOW - timedelta(seconds=seconds_ago),
                           machine_active=False, voltage_24v=voltage, digital_signals=states)


def totals(result):
    return {key: sum(bucket['failure_causes'][key] for bucket in result['buckets']) for key in IHM_SIGNALS}


def test_repeated_readings_do_not_multiply_occurrences_and_simultaneous_causes_count_separately():
    readings = [reading(60, porta_aberta=True), reading(50, porta_aberta=True),
                reading(40, porta_aberta=True, inativo=True), reading(30, porta_aberta=False),
                reading(20, porta_aberta=True)]
    result = calculate_utilization(readings, NOW, timeout=90)
    assert totals(result) == {**dict.fromkeys(IHM_SIGNALS, 0), 'porta_aberta': 2, 'inativo': 1}
    assert sum(bucket['samples'] for bucket in result['buckets']) == 5
    assert sum(bucket['seconds']['EMERGENCIA'] for bucket in result['buckets']) == 50


def test_same_timestamp_uses_final_ingested_snapshot_for_occurrences():
    result = calculate_utilization([reading(30, ativo=True), reading(30, inativo=True),
                                    reading(20, inativo=True)], NOW, timeout=90)
    assert totals(result) == {**dict.fromkeys(IHM_SIGNALS, 0), 'inativo': 1}


def test_continuity_before_window_and_timeout_do_not_invent_known_transitions():
    result = calculate_utilization([reading(86410, porta_aberta=True), reading(86390, porta_aberta=True),
                                    reading(86380, porta_aberta=False), reading(86370, porta_aberta=True),
                                    reading(30, porta_aberta=True)], NOW, timeout=90)
    assert totals(result)['porta_aberta'] == 2
    assert result['buckets'][0]['failure_causes']['porta_aberta'] == 1
    assert result['buckets'][-1]['failure_causes']['porta_aberta'] == 1


def test_all_causes_and_legacy_aliases_keep_power_off_priority():
    result = calculate_utilization([
        reading(40, voltage=False, **dict.fromkeys(IHM_SIGNALS, True)),
        reading(30, **dict.fromkeys(IHM_SIGNALS, True)),
        reading(20, **dict.fromkeys(IHM_SIGNALS, False)),
        reading(10, emergencia=False, emergency=True, alarme=False, alarm=True),
    ], NOW, timeout=90)
    assert totals(result) == {**dict.fromkeys(IHM_SIGNALS, 1), 'emergencia': 2, 'alarme': 2}
    assert sum(bucket['seconds']['DESLIGADA'] for bucket in result['buckets']) == 10


def test_empty_and_unknown_states_do_not_invent_failure_causes():
    for readings in ([], [reading(30)], [reading(20, ciclo=True)],
                     [reading(10, **dict.fromkeys(IHM_SIGNALS, False))]):
        assert totals(calculate_utilization(readings, NOW)) == dict.fromkeys(IHM_SIGNALS, 0)
