"""Optional fixed current must never replace the real IHM digital snapshot."""
import copy
from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from ponteUsb import Gateway, reading_from


def sample():
    payload = json.loads((ROOT / 'firmware/optaCncMonitor/monitorSample.json').read_text(encoding='utf-8'))
    return reading_from({'protocol': 1, 'machine_id': '1', 'sequence': 1,
                         'uptime_ms': 1000, 'payload': payload})


def test_current_stays_absent_when_virtual_mode_is_not_requested():
    reading = sample()
    original = copy.deepcopy(reading.payload)
    event = Gateway(None).payload_for(reading)
    assert event.get('analog_signals', {}) == {}
    assert event['extra_signals']['current_input']['source'] == 'unavailable'
    assert reading.payload == original


@pytest.mark.parametrize('amps', [0, 24.0, 18.2])
@pytest.mark.parametrize('legacy', [False, True])
def test_fixed_virtual_current_preserves_digital_signals_and_other_measurements(amps, legacy):
    reading = sample()
    reading.payload['analog_signals']['temperature'] = -5.5
    original = copy.deepcopy(reading.payload)
    gateway = Gateway(None, device_id='legacy' if legacy else None, simulated_current=amps)
    event = gateway.payload_for(reading)
    assert event['analog_signals'] == {'temperature': -5.5, 'current': amps}
    assert event['extra_signals']['current_input'] == {
        'input': 'I8', 'unit': 'A', 'source': 'simulated', 'physical_enabled': False,
    }
    assert event['digital_signals' if legacy else 'states'] == original['digital_signals']
    for key in ('profile', 'entradas_brutas', 'transport', 'timestamp_source'):
        assert event['extra_signals'][key] == original['extra_signals'][key]
    assert reading.payload == original


@pytest.mark.parametrize('key', ['current', 'corrente'])
@pytest.mark.parametrize('value', [0, 7.6, -1, None, True, 'invalid'])
def test_any_received_current_is_preserved_instead_of_hidden_by_a_virtual_value(key, value):
    reading = sample()
    reading.payload['analog_signals'] = {key: value}
    reading.payload['extra_signals']['current_input']['source'] = 'received'
    event = Gateway(None, simulated_current=12.5).payload_for(reading)
    assert event['analog_signals'] == {key: value}
    assert event['extra_signals']['current_input']['source'] == 'received'


def test_enabled_physical_sensor_with_missing_measurement_is_not_filled_with_virtual_current():
    reading = sample()
    reading.payload['extra_signals']['current_input']['physical_enabled'] = True
    event = Gateway(None, simulated_current=12.5).payload_for(reading)
    assert event.get('analog_signals', {}) == {}
    assert event['extra_signals']['current_input']['physical_enabled'] is True


def test_retry_keeps_original_current_event_and_timestamp():
    reading = sample()
    gateway = Gateway(None, simulated_current=12.5)
    first = gateway.payload_for(reading)
    gateway.simulated_current = 18.2
    duplicate = replace(reading, arrived=reading.arrived + 10, captured_at='2030-01-01T00:00:00Z')
    assert gateway.payload_for(duplicate) == first
    next_reading = replace(reading, sequence=2, uptime_ms=2000)
    next_event = gateway.payload_for(next_reading)
    assert next_event['analog_signals']['current'] == 18.2
    assert next_event['event_id'] != first['event_id']


@pytest.mark.parametrize('amps', [-1, float('nan'), float('inf'), True, None, 'bad'])
def test_gateway_rejects_invalid_configured_current_but_none_disables_it(amps):
    if amps is None:
        assert Gateway(None, simulated_current=None).simulated_current is None
    else:
        with pytest.raises(ValueError, match='corrente simulada'):
            Gateway(None, simulated_current=amps)


@pytest.mark.parametrize(('arguments', 'expected'), [
    ([], None), (['--simular-corrente'], 24.0),
    (['--corrente', '18.2'], 18.2),
    (['--simular-corrente', '--corrente', '0'], 0),
])
def test_cli_selects_default_custom_or_disabled_virtual_current_without_opening_serial(monkeypatch, arguments, expected):
    import dotenv
    import ponteUsb
    captured = {}

    class Configured(Exception):
        pass

    def gateway(*args, **kwargs):
        captured.update(kwargs)
        raise Configured

    monkeypatch.setattr(dotenv, 'load_dotenv', lambda *args, **kwargs: None)
    monkeypatch.setattr(ponteUsb, 'Gateway', gateway)
    monkeypatch.setattr(sys, 'argv', ['ponteUsb.py', '--porta', 'TEST', *arguments])
    with pytest.raises(Configured):
        ponteUsb.main()
    assert captured['simulated_current'] == expected


@pytest.mark.parametrize('value', ['-1', 'nan', 'inf', '-inf', 'invalid'])
def test_cli_rejects_invalid_current_before_opening_the_port(monkeypatch, capsys, value):
    import dotenv
    import ponteUsb
    import serial

    def unexpected_port(*args, **kwargs):
        pytest.fail('Invalid current must not access the serial port')

    monkeypatch.setattr(dotenv, 'load_dotenv', lambda *args, **kwargs: None)
    monkeypatch.setattr(serial, 'Serial', unexpected_port)
    monkeypatch.setattr(sys, 'argv', ['ponteUsb.py', '--porta', 'TEST', f'--corrente={value}'])
    with pytest.raises(SystemExit) as error:
        ponteUsb.main()
    assert error.value.code == 2
    assert capsys.readouterr().out == ''
