"""Produz eventos JSON Lines de máquinas em stdout; não acessa rede nem hardware."""
import argparse
from datetime import datetime, timezone
import json
import math
import sys
import time
from uuid import uuid4

SIGNALS = ("ativo", "inativo", "emergencia", "motor_ligado", "alarme", "porta_aberta")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--machine-id', required=True, help='UUID ou código da máquina cadastrada')
    parser.add_argument('--state', choices=('cycle', *SIGNALS), default='ativo')
    parser.add_argument('--also', action='append', choices=SIGNALS, default=[],
                        help='Sinal adicional simultâneo; repetível (ex.: --state porta_aberta --also emergencia)')
    parser.add_argument('--count', type=int, default=1, help='Quantidade de eventos; -1 até Ctrl+C')
    parser.add_argument('--interval', type=float, default=1, help='Intervalo entre eventos em segundos')
    parser.add_argument('--current', type=float, help='Corrente simulada em A para a entrada reservada I8; omitida significa não informado')
    args = parser.parse_args(argv)
    if not args.machine_id.strip() or len(args.machine_id.strip()) > 36:
        parser.error('--machine-id deve conter entre 1 e 36 caracteres')
    if args.count < -1 or args.interval < 0:
        parser.error('--count deve ser -1 ou não negativo; --interval não pode ser negativo')
    if args.current is not None and (not math.isfinite(args.current) or args.current < 0):
        parser.error('--current deve ser finita e não negativa, em A')
    index = 0
    try:
        while args.count == -1 or index < args.count:
            selected = SIGNALS[index % len(SIGNALS)] if args.state == 'cycle' else args.state
            event = {
                'machine_id': args.machine_id.strip(),
                'states': {name: name == selected or name in args.also for name in SIGNALS},
                'event_id': str(uuid4()),
                'timestamp': datetime.now(timezone.utc).isoformat(),
            }
            if args.current is not None:
                event['analog_signals'] = {'current': args.current}
                event['extra_signals'] = {'current_input': {
                    'input': 'I8', 'physical_enabled': False, 'unit': 'A', 'source': 'simulated'}}
            print(json.dumps(event, ensure_ascii=False), flush=True)
            index += 1
            if args.count == -1 or index < args.count:
                time.sleep(args.interval)
    except (KeyboardInterrupt, BrokenPipeError):
        return 0
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
