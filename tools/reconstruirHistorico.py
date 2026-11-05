"""Recria historico de demonstracao pela API, sem modificar leituras existentes.

Sem --aplicar, apenas prepara um plano local. Reutilize --plano para retomar o
mesmo lote sem duplicar eventos. A origem fica identificada como reconstructed.
"""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import random
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SIGNALS = ('ativo', 'inativo', 'emergencia', 'motor_ligado', 'porta_aberta', 'alarme')


def utc_text(value):
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def parse_time(value):
    timestamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if timestamp.tzinfo is None:
        raise ValueError('Informe o fuso no horario, por exemplo 2026-11-04T22:00:00-03:00.')
    return timestamp.astimezone(timezone.utc).replace(microsecond=0)


def build_plan(start, end, names, *, seed=42, interval=30):
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError('Os horarios devem incluir fuso.')
    start, end = parse_time(utc_text(start)), parse_time(utc_text(end))
    seconds = int((end - start).total_seconds())
    if not 60 <= seconds <= 86400:
        raise ValueError('O periodo deve estar entre um minuto e 24 horas.')
    if not isinstance(interval, int) or not 1 <= interval <= 60:
        raise ValueError('O intervalo deve estar entre 1 e 60 segundos.')
    names = [name.strip() for name in names]
    if len(names) != 2 or any(not name or len(name) > 255 for name in names) or len({name.casefold() for name in names}) != 2:
        raise ValueError('Informe exatamente dois nomes distintos de maquinas.')
    config = {'version': 1, 'start': utc_text(start), 'end': utc_text(end),
              'names': names, 'seed': seed, 'interval_seconds': interval}
    batch = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()[:24]
    machines = []
    for index, name in enumerate(names):
        rng = random.Random(f'{seed}:{index}:{name}')
        pauses = []
        cursor = rng.randint(600, 1200)
        while cursor + 12 < seconds:
            stop = rng.randint(4, 12)
            pauses.append((cursor, cursor + stop))
            cursor += stop + rng.randint(600, 1200)
        offsets = set(range(0, seconds + 1, interval)) | {seconds}
        for begin, finish in pauses:
            offsets.update((begin, finish))
        records = [{'offset': offset, 'active': not any(begin <= offset < finish for begin, finish in pauses)}
                   for offset in sorted(offsets)]
        idle = sum(finish - begin for begin, finish in pauses)
        machines.append({'name': name, 'records': records, 'pauses': pauses,
                         'active_seconds': seconds - idle, 'idle_seconds': idle})
    return {**config, 'batch_id': batch, 'source': 'reconstructed', 'machines': machines}


def event_payload(plan, index, record, machine_id):
    active = record['active']
    states = dict.fromkeys(SIGNALS, False)
    states.update(ativo=active, inativo=not active, motor_ligado=active)
    return {'machine_id': machine_id, 'states': states, 'analog_signals': {},
            'timestamp': utc_text(parse_time(plan['start']) + timedelta(seconds=record['offset'])),
            'event_id': f"rebuild-{plan['batch_id']}-{index}-{record['offset']}",
            'extra_signals': {'source': 'reconstructed', 'batch_id': plan['batch_id'],
                              'scenario': 'history-restoration'}}


class Api:
    def __init__(self, base, key=''):
        self.base = base.rstrip('/')
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}
        if key:
            self.headers['X-API-Key'] = key

    def request(self, method, path, body=None):
        payload = None if body is None else json.dumps(body, allow_nan=False).encode('utf-8')
        request = urllib.request.Request(self.base + path, payload, self.headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            raise RuntimeError(f'API recusou {method} {path.split("?")[0]} (HTTP {error.code}).') from None
        except urllib.error.URLError:
            raise RuntimeError('Nao foi possivel acessar a API local; confira se o backend esta aberto.') from None


def history(api, machine_id, plan, *, limit=500, page=1):
    query = urllib.parse.urlencode({'start': plan['start'], 'end': plan['end'], 'limit': limit, 'page': page})
    return api.request('GET', f'/cncs/{machine_id}/history?{query}')


def apply_plan(api, plan, progress=None):
    # Reject modified/corrupt plans before any database mutation.
    rebuilt = build_plan(parse_time(plan['start']), parse_time(plan['end']), plan['names'],
                         seed=plan['seed'], interval=plan['interval_seconds'])
    if json.loads(json.dumps(plan)) != json.loads(json.dumps(rebuilt)):
        raise ValueError('O plano foi alterado ou pertence a outra versao do gerador.')
    if parse_time(plan['end']) > datetime.now(timezone.utc):
        raise ValueError('O periodo nao pode terminar no futuro.')
    existing = api.request('GET', '/cncs')
    if not isinstance(existing, list):
        raise ValueError('Resposta inesperada da listagem de maquinas.')
    matches = []
    for name in plan['names']:
        found = [item for item in existing if item['name'].strip().casefold() == name.casefold()]
        if len(found) > 1:
            raise ValueError(f'Mais de uma maquina tem o nome {name}; escolha nomes unicos.')
        matches.append(found[0] if found else None)
    results = []
    for index, machine in enumerate(matches):
        created = machine is None
        if created:
            machine = api.request('POST', '/cncs', {'name': plan['names'][index],
                                  'description': 'Maquina utilizada na integracao com CLP/IHM e Arduino Opta.'})
        before = history(api, machine['id'], plan, limit=1)['total']
        results.append({'id': machine['id'], 'code': machine['code'], 'name': machine['name'],
                        'created': created, 'window_count_before': before, 'event_ids': []})
    pending = sorted((record['offset'], index, record)
                     for index, machine in enumerate(plan['machines']) for record in machine['records'])
    for position, (_, index, record) in enumerate(pending, 1):
        body = event_payload(plan, index, record, results[index]['id'])
        response = api.request('POST', '/events', body)
        if response.get('states') != body['states'] or response.get('extra_signals') != body['extra_signals']:
            raise RuntimeError('A API retornou um evento diferente do enviado.')
        if parse_time(response['timestamp']) != parse_time(body['timestamp']):
            raise RuntimeError('A API retornou um horario diferente do enviado.')
        results[index]['event_ids'].append(response['id'])
        if progress and (position % 100 == 0 or position == len(pending)):
            progress(position, len(pending))
    for index, machine in enumerate(results):
        first = history(api, machine['id'], plan)
        items = list(first['items'])
        pages = math.ceil(first['total'] / 500)
        for page in range(2, pages + 1):
            items.extend(history(api, machine['id'], plan, page=page)['items'])
        expected_ids = set(machine['event_ids'])
        stored = [item for item in items if item['id'] in expected_ids]
        if len(stored) != len(expected_ids) or len(expected_ids) != len(plan['machines'][index]['records']):
            raise RuntimeError('A conferencia do historico encontrou eventos ausentes ou duplicados.')
        ordered = sorted(stored, key=lambda item: parse_time(item['timestamp']))
        idle = sum(int((parse_time(right['timestamp']) - parse_time(left['timestamp'])).total_seconds())
                   for left, right in zip(ordered, ordered[1:]) if left['digital_signals']['inativo'])
        if idle != plan['machines'][index]['idle_seconds']:
            raise RuntimeError('O tempo parado gravado nao corresponde ao plano.')
        machine.update(window_count_after=first['total'], verified_events=len(stored), idle_seconds=idle,
                       active_seconds=plan['machines'][index]['active_seconds'],
                       pause_count=len(plan['machines'][index]['pauses']))
        del machine['event_ids']
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--api', default='http://127.0.0.1:8000/api')
    parser.add_argument('--maquinas', nargs=2, default=['Siemens S7-300', 'Siemens S7-1200'])
    parser.add_argument('--horas', type=float, default=4)
    parser.add_argument('--fim', help='Fim com fuso, por exemplo 2026-11-04T22:00:00-03:00; omitido usa agora')
    parser.add_argument('--intervalo-segundos', type=int, default=30)
    parser.add_argument('--semente', type=int, default=42)
    parser.add_argument('--plano', type=Path, help='Retoma um plano JSON ja preparado, sem duplicar seus eventos')
    parser.add_argument('--aplicar', action='store_true', help='Grava o plano pela API; omitido apenas prepara o arquivo')
    args = parser.parse_args(argv)
    try:
        if args.plano:
            path = args.plano.resolve()
            plan = json.loads(path.read_text(encoding='utf-8'))
        else:
            if not math.isfinite(args.horas) or not 1 / 60 <= args.horas <= 24:
                raise ValueError('--horas deve estar entre 1/60 e 24.')
            end = parse_time(args.fim) if args.fim else datetime.now(timezone.utc).replace(microsecond=0)
            plan = build_plan(end - timedelta(seconds=round(args.horas * 3600)), end, args.maquinas,
                              seed=args.semente, interval=args.intervalo_segundos)
            path = ROOT / '.local/historicoReconstruido' / (plan['batch_id'] + '.json')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
        start, end = parse_time(plan['start']), parse_time(plan['end'])
        print(f"Periodo local: {start.astimezone():%d/%m/%Y %H:%M:%S} ate {end.astimezone():%d/%m/%Y %H:%M:%S}")
        print(f"Lote: {plan['batch_id']}; origem: reconstructed")
        for machine in plan['machines']:
            print(f"{machine['name']}: {len(machine['records'])} registros, {machine['active_seconds']}s ativa, "
                  f"{machine['idle_seconds']}s parada, {len(machine['pauses'])} pausas.")
        print(f'Plano: {path}')
        if not args.aplicar:
            print('Nenhum dado gravado. Use --plano CAMINHO --aplicar para executar este lote.')
            return 0
        # Use the same local configuration loader as the backend; never print credentials.
        sys.path.insert(0, str(ROOT / 'backend'))
        import config  # noqa: F401
        key = os.getenv('INGEST_API_KEY') or os.getenv('DEVICE_API_KEY', '')
        api = Api(args.api, key)
        results = apply_plan(api, plan, lambda done, total: print(f'Gravados/conferidos: {done}/{total}', flush=True))
        output = path.with_name(path.stem + '-resultado.json')
        output.write_text(json.dumps({'batch_id': plan['batch_id'], 'start': plan['start'], 'end': plan['end'],
                                     'source': 'reconstructed', 'machines': results}, ensure_ascii=False, indent=2), encoding='utf-8')
        for machine in results:
            print(f"OK {machine['code']} | {machine['name']} | {machine['verified_events']} eventos conferidos")
        print(f'Resultado: {output}')
        return 0
    except (ValueError, KeyError, OSError, RuntimeError) as error:
        print(f'Falha: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
