"""Seleciona HTTP/Wi-Fi ou USB compilando e gravando o firmware do Opta."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FQBN = 'arduino:mbed_opta:opta'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--transporte', required=True, choices=('http', 'usb'),
                        help='http: Opta -> Wi-Fi -> API; usb: Opta -> ponte USB -> API')
    parser.add_argument('--porta', help='Porta de gravação: /dev/ttyACM0, /dev/serial/by-id/... ou COM4')
    parser.add_argument('--somente-compilar', action='store_true',
                        help='Gera o firmware sem gravar nem alterar o transporte da placa')
    parser.add_argument('--cli', default='arduino-cli', help='Executável Arduino CLI (padrão: PATH)')
    parser.add_argument('--config-file', type=Path, help='Configuração opcional do Arduino CLI')
    args = parser.parse_args(argv)
    if not args.somente_compilar and not args.porta:
        parser.error('--porta é obrigatória para gravar; ou use --somente-compilar')

    # Resolve caminhos informados antes de executar os comandos na raiz do projeto.
    cli = args.cli
    if '/' in cli or '\\' in cli:
        cli = str(Path(cli).resolve())
    common = [cli]
    if args.config_file:
        common += ['--config-file', str(args.config_file.resolve())]
    output = ROOT / '.build' / 'firmware' / ('opta-usb' if args.transporte == 'usb' else 'opta-wifi')
    usb = int(args.transporte == 'usb')
    compile_command = common + [
        'compile', '--fqbn', FQBN,
        '--build-property', f'compiler.cpp.extra_flags=-DULTRON_TELEMETRY_USB_OVERRIDE={usb}',
        '--output-dir', str(output), str(ROOT / 'firmware' / 'optaCncMonitor'),
    ]
    try:
        # --output-dir keeps older sketches' binaries. The uploader rejects a
        # directory with multiple sketches, so always prepare a clean export.
        if output.exists():
            shutil.rmtree(output)
        output.mkdir(parents=True, exist_ok=True)
        print(f'Compilando transporte {args.transporte.upper()}...', flush=True)
        subprocess.run(compile_command, cwd=ROOT, check=True)
        if args.somente_compilar:
            print(f'Firmware gerado em {output}. A placa não foi alterada.')
            return 0
        print(f'Gravando em {args.porta}; a placa será reiniciada.', flush=True)
        subprocess.run(common + [
            'upload', '--fqbn', FQBN, '--port', args.porta, '--input-dir', str(output),
        ], cwd=ROOT, check=True)
    except FileNotFoundError:
        print('Arduino CLI não encontrado. Instale-o ou informe --cli CAMINHO.', file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        print(f'Falha no Arduino CLI (código {error.returncode}); troca não confirmada.', file=sys.stderr)
        return 1
    except OSError as error:
        print(f'Não foi possível executar Arduino CLI: {error}', file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print('\nOperação interrompida; confira o firmware da placa antes de usar.', file=sys.stderr)
        return 130

    print(f'Transporte {args.transporte.upper()} gravado no Opta.')
    if args.transporte == 'usb':
        print('Inicie tools/ponteUsb.py com --porta; o ID da máquina vem do firmware. '
              'A porta pode mudar após a gravação.')
    else:
        print('O Opta enviará por Wi-Fi/HTTP usando a rede e o host de optaSecrets.h. '
              'Mantenha a API acessível e a ponte USB encerrada.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
