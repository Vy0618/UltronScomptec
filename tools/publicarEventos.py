"""Lê JSON Lines de stdin e publica em /api/events; respostas em stdout, erros em stderr."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--api', default='http://127.0.0.1:8000/api')
    parser.add_argument('--key', default=os.getenv('INGEST_API_KEY') or os.getenv('DEVICE_API_KEY', ''))
    parser.add_argument('--timeout', type=float, default=10)
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error('--timeout deve ser positivo')
    for number, line in enumerate(sys.stdin, 1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
            if not isinstance(payload, dict):
                raise ValueError('evento deve ser objeto JSON')
            headers = {'Content-Type': 'application/json'}
            if args.key:
                headers['X-API-Key'] = args.key
            request = urllib.request.Request(
                args.api.rstrip('/') + '/events',
                data=json.dumps(payload, allow_nan=False).encode(), headers=headers,
            )
            with urllib.request.urlopen(request, timeout=args.timeout) as response:
                print(json.dumps(json.load(response), ensure_ascii=False), flush=True)
        except (ValueError, OSError, urllib.error.URLError) as error:
            detail = error.read().decode(errors='replace') if isinstance(error, urllib.error.HTTPError) else str(error)
            print(f'Linha {number}: {detail}', file=sys.stderr)
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
