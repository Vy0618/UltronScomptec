"""Native compiler stderr must be logged without hiding the actual exit status."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


@pytest.mark.skipif(os.name != 'nt', reason='Windows PowerShell native stderr handling')
@pytest.mark.parametrize('compiler_exit', [0, 5])
def test_firmware_runner_uses_exit_code_instead_of_treating_warnings_as_failure(tmp_path, compiler_exit):
    shell = shutil.which('powershell.exe')
    if not shell:
        pytest.skip('Windows PowerShell is not installed')
    source = Path(__file__).resolve().parents[2] / 'firmware/testarFirmware.ps1'
    harness = tmp_path / 'runner.ps1'
    log = tmp_path / 'compiler.log'
    harness.write_text('''param([string]$Source, [string]$Python, [string]$Log, [int]$Expected)
$ErrorActionPreference = 'Stop'
$tokens = $null
$errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($Source, [ref]$tokens, [ref]$errors)
if ($errors.Count) { throw 'Firmware script has syntax errors' }
$definition = $ast.Find({ param($node)
    $node -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq 'Run-Checked'
}, $true)
. ([scriptblock]::Create($definition.Extent.Text))
$failed = $false
try {
    Run-Checked $Python @('-c', "import sys; print('compiler warning', file=sys.stderr); sys.exit($Expected)") $Log
} catch { $failed = $true }
if ($failed -ne ($Expected -ne 0)) { throw 'Compiler exit status was not respected' }
if ($ErrorActionPreference -ne 'Stop') { throw 'Caller error preference was not restored' }
if (-not (Get-Content -LiteralPath $Log -Raw).Contains('compiler warning')) { throw 'Compiler stderr was not logged' }
''', encoding='utf-8')
    result = subprocess.run([
        shell, '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
        '-File', str(harness), '-Source', str(source), '-Python', sys.executable,
        '-Log', str(log), '-Expected', str(compiler_exit),
    ], capture_output=True, text=True, errors='replace', timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
