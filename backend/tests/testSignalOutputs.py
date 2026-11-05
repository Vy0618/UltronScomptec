"""Output coverage for the report's combinations and incomplete observations."""
from copy import deepcopy
from itertools import product
from pathlib import Path
from types import SimpleNamespace
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from schemas.signalOutput import SignalOutput
from services.machineState import derive_status, derive_diagnostics
from services.signalOutputs import derive_signal_outputs, SIGNALS, LEVEL_ORDER


def reading(enabled=(), *, states=None, current=None):
    return SimpleNamespace(digital_signals=states if states is not None else {signal: signal in enabled for signal in SIGNALS},
                           machine_active='ativo' in enabled, voltage_24v=None,
                           analog_signals={} if current is None else {'current': current},
                           extra_signals={'current_input': {'source': 'simulated'}})


@pytest.mark.parametrize('enabled,status,code', [
    (('ativo',), 'EMERGENCIA', 'ATIVIDADE_INFORMADA'),
    (('inativo',), 'EMERGENCIA', 'INATIVIDADE_INFORMADA'),
    (('ativo', 'inativo'), 'EMERGENCIA', 'ATIVIDADE_CONFLITANTE'),
    ((), 'OPERANDO', 'SEM_SINAIS_ACIONADOS'),
    (('motor_ligado',), 'EMERGENCIA', 'MOTOR_SEM_ATIVIDADE_CONFIRMADA'),
    (('ativo', 'motor_ligado'), 'EMERGENCIA', 'ATIVIDADE_COM_MOTOR'),
    (('inativo', 'motor_ligado'), 'EMERGENCIA', 'INATIVIDADE_COM_MOTOR'),
    (('porta_aberta',), 'EMERGENCIA', 'PORTA_ABERTA'),
    (('ativo', 'porta_aberta'), 'EMERGENCIA', 'ATIVIDADE_COM_PORTA_ABERTA'),
    (('inativo', 'porta_aberta'), 'EMERGENCIA', 'INATIVIDADE_COM_PORTA_ABERTA'),
    (('emergencia',), 'EMERGENCIA', 'EMERGENCIA_ACIONADA'),
    (('ativo', 'emergencia'), 'EMERGENCIA', 'EMERGENCIA_COM_ATIVIDADE'),
    (('porta_aberta', 'emergencia'), 'EMERGENCIA', 'PORTA_ABERTA_EMERGENCIA'),
    (('ativo', 'porta_aberta', 'emergencia'), 'EMERGENCIA', 'PORTA_ABERTA_EMERGENCIA'),
    (('ativo', 'alarme'), 'EMERGENCIA', 'ALARME_COM_ATIVIDADE'),
    (('inativo', 'alarme'), 'EMERGENCIA', 'ALARME_COM_INATIVIDADE'),
    (('porta_aberta', 'alarme'), 'EMERGENCIA', 'PORTA_ABERTA_COM_ALARME'),
    (('alarme', 'emergencia'), 'EMERGENCIA', 'EMERGENCIA_COM_ALARME'),
    (('ativo', 'inativo', 'alarme'), 'EMERGENCIA', 'ATIVIDADE_CONFLITANTE'),
    (SIGNALS, 'EMERGENCIA', 'PORTA_ABERTA_EMERGENCIA'),
])
def test_boolean_interactions_preserve_outputs_and_observed_signals(enabled, status, code):
    observation = reading(enabled)
    before = deepcopy(vars(observation))
    outputs = derive_signal_outputs(observation)
    assert code in {output['code'] for output in outputs}
    assert derive_status(observation) == status
    assert vars(observation) == before
    for output in outputs:
        SignalOutput.model_validate(output)


def test_all_64_snapshots_are_covered_and_preserve_all_diagnostics():
    expected_faults = {
        'ativo': 'Falha na execução', 'inativo': 'Falha na parada',
        'emergencia': 'Falha na emergência', 'motor_ligado': 'Falha no motor',
        'alarme': 'Falha no alarme / erro', 'porta_aberta': 'Falha na porta',
    }
    for bits in product((False, True), repeat=6):
        states = dict(zip(SIGNALS, bits))
        outputs = derive_signal_outputs(reading(states=states))
        codes = [output['code'] for output in outputs]
        assert codes and len(codes) == len(set(codes))
        levels = [LEVEL_ORDER[output['level']] for output in outputs]
        assert levels == sorted(levels)
        assert {item['code'] for item in derive_diagnostics(states)} <= set(codes)
        observation = reading(states=states)
        for active in (False, True):
            observation.machine_active = active
            assert derive_status(observation) == ('EMERGENCIA' if any(bits) else 'OPERANDO')
        if any(bits):
            fault = outputs[0]
            assert fault['code'] == 'PARAMETROS_IHM_ACIONADOS'
            assert fault['level'] == 'critical'
            assert fault['signals'] == [signal for signal in SIGNALS if states[signal]]
            assert fault['title'] == '; '.join(expected_faults[signal] for signal in fault['signals'])
            for signal in fault['signals']:
                assert f'({signal})' in fault['message']
        else:
            assert 'operando' in outputs[0]['title']
        assert observation.digital_signals == states
    all_active = derive_signal_outputs(reading(SIGNALS))
    assert {'PORTA_ABERTA_EMERGENCIA', 'ATIVIDADE_CONFLITANTE'} <= {item['code'] for item in all_active}


@pytest.mark.parametrize('enabled,code,status', [
    (('ativo',), 'CORRENTE_COM_ATIVIDADE', 'EMERGENCIA'),
    (('inativo',), 'CORRENTE_COM_INATIVIDADE', 'EMERGENCIA'),
])
@pytest.mark.parametrize('current', [0, 12.5])
def test_current_interactions_have_simulation_origin_and_preserve_zero(enabled, code, status, current):
    observation = reading(enabled, current=current)
    output = next(item for item in derive_signal_outputs(observation) if item['code'] == code)
    assert f'{current:g} A (simulada)' in output['message']
    assert output['level'] == 'info'
    assert derive_status(observation) == status
    observation.analog_signals = {}
    assert not any('current' in item['signals'] for item in derive_signal_outputs(observation))


def test_partial_and_legacy_signals_do_not_become_false_or_confirm_normal_operation():
    observation = reading(states={'porta_aberta': True})
    outputs = derive_signal_outputs(observation)
    assert {item['code'] for item in outputs} == {'PARAMETROS_IHM_ACIONADOS', 'PORTA_ABERTA', 'SINAIS_NAO_INFORMADOS'}
    assert observation.digital_signals == {'porta_aberta': True}
    observation = reading(states={'em_execucao': True})
    assert 'ATIVIDADE_LEGADA' in {item['code'] for item in derive_signal_outputs(observation)}
    assert 'ativo' not in observation.digital_signals
    assert derive_signal_outputs(None) == []


@pytest.mark.parametrize('states,status,code', [
    ({'emergencia': False, 'emergency': True}, 'EMERGENCIA', 'EMERGENCIA_ACIONADA'),
    ({'alarme': False, 'alarm': True}, 'EMERGENCIA', 'ALARME_ACIONADO'),
    ({'porta_aberta': True, 'emergencia': False, 'emergency': True}, 'EMERGENCIA', 'PORTA_ABERTA_EMERGENCIA'),
])
def test_asserted_legacy_aliases_keep_outputs_consistent_with_status(states, status, code):
    observation = reading(states=states)
    before = deepcopy(vars(observation))
    assert derive_status(observation) == status
    assert code in {item['code'] for item in derive_signal_outputs(observation)}
    assert vars(observation) == before
