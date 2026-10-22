"""Verifica seleção e falhas de gravação sem acessar uma placa."""
import importlib.util
from pathlib import Path
import shutil
import subprocess

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / 'configurarTransmissao.py'
spec = importlib.util.spec_from_file_location('configurar_transmissao', SCRIPT)
selector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(selector)


@pytest.mark.parametrize(('transport', 'flag', 'directory'), [
    ('usb', '1', 'opta-usb'), ('http', '0', 'opta-wifi'),
])
def test_selected_firmware_is_built_before_upload(monkeypatch, transport, flag, directory):
    calls = []
    monkeypatch.setattr(selector.subprocess, 'run', lambda cmd, **kw: calls.append((cmd, kw)))
    assert selector.main(['--transporte', transport, '--porta', '/dev/serial/by-id/Opta']) == 0
    build, upload = (call[0] for call in calls)
    assert build[1] == 'compile' and upload[1] == 'upload'
    assert f'compiler.cpp.extra_flags=-DULTRON_TELEMETRY_USB_OVERRIDE={flag}' in build
    artifact = build[build.index('--output-dir') + 1]
    assert Path(artifact).name == directory
    assert upload[upload.index('--input-dir') + 1] == artifact
    assert upload[upload.index('--port') + 1] == '/dev/serial/by-id/Opta'
    assert all(kw == {'cwd': selector.ROOT, 'check': True} for _, kw in calls)


def test_compile_only_and_paths_with_spaces(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)
    calls = []
    monkeypatch.setattr(selector.subprocess, 'run', lambda cmd, **kw: calls.append(cmd))
    assert selector.main(['--transporte', 'usb', '--somente-compilar',
                          '--cli', './Arduino CLI/arduino-cli', '--config-file', 'config local.yaml']) == 0
    assert len(calls) == 1 and 'upload' not in calls[0]
    assert calls[0][0] == str(tmp_path / 'Arduino CLI/arduino-cli')
    assert calls[0][2] == str(tmp_path / 'config local.yaml')
    assert 'A placa não foi alterada' in capsys.readouterr().out


@pytest.mark.parametrize('arguments', [[], ['--transporte', 'bluetooth'], ['--transporte', 'usb']])
def test_invalid_arguments_do_not_access_cli(monkeypatch, arguments):
    def unexpected(*args, **kwargs):
        pytest.fail('Arduino CLI não deveria ser executado')
    monkeypatch.setattr(selector.subprocess, 'run', unexpected)
    with pytest.raises(SystemExit) as error:
        selector.main(arguments)
    assert error.value.code == 2


@pytest.mark.parametrize('failed_stage', ['compile', 'upload'])
def test_failure_never_reports_success(monkeypatch, failed_stage, capsys):
    calls = []
    def run(cmd, **kwargs):
        calls.append(cmd[1])
        if cmd[1] == failed_stage:
            raise subprocess.CalledProcessError(2, cmd)
    monkeypatch.setattr(selector.subprocess, 'run', run)
    assert selector.main(['--transporte', 'http', '--porta', 'COM4']) == 1
    assert calls == (['compile'] if failed_stage == 'compile' else ['compile', 'upload'])
    captured = capsys.readouterr()
    assert 'troca não confirmada' in captured.err
    assert 'gravado no Opta' not in captured.out


def test_missing_cli(monkeypatch, capsys):
    def missing(*args, **kwargs):
        raise FileNotFoundError
    monkeypatch.setattr(selector.subprocess, 'run', missing)
    assert selector.main(['--transporte', 'usb', '--somente-compilar']) == 1
    assert 'Arduino CLI não encontrado' in capsys.readouterr().err


@pytest.mark.parametrize('usb', [0, 1])
def test_terminal_selection_overrides_opposite_local_setting(tmp_path, usb):
    compiler = shutil.which('g++')
    if compiler is None:
        pytest.skip('Verificação do config.h exige g++')
    source = selector.ROOT / 'firmware/optaMesaMonitor/config.h'
    (tmp_path / 'config.h').write_text(source.read_text())
    (tmp_path / 'Arduino.h').write_text('#include <cstdint>\n#include <cstddef>\n')
    (tmp_path / 'optaSecrets.h').write_text(f'#define ULTRON_TELEMETRY_USB {1 - usb}\n')
    unit = tmp_path / 'check.cpp'
    unit.write_text(f'#include "config.h"\nstatic_assert(ULTRON_TELEMETRY_USB == {usb}, "transporte errado");\n')
    subprocess.run([compiler, '-std=c++17', '-Wall', '-Wextra', '-Werror', '-fsyntax-only',
                    f'-DULTRON_TELEMETRY_USB_OVERRIDE={usb}', '-I', str(tmp_path), str(unit)], check=True)
