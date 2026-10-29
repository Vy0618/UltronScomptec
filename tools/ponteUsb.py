"""Opta USB serial -> API SCOMPTEC. Linux: use /dev/serial/by-id/ ou /dev/ttyACM0."""
import argparse
import copy
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import queue
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from uuid import UUID, uuid4

MAX_FRAME_BYTES = 16384
MAX_PENDING_SECONDS = 15


class Frames:
    """Remonta quadros JSON da aquisição CNC pela serial."""
    def __init__(self):
        self.buffer = ''

    def feed(self, line):
        if line.startswith('CNC_JSON:'):
            self.buffer = line[9:]
        elif line.startswith('CNC_CHUNK:'):
            fragment = line[10:]
            self.buffer = fragment[9:] if fragment.startswith('CNC_JSON:') else self.buffer + fragment
        else:
            return None
        if len(self.buffer) > MAX_FRAME_BYTES:
            self.buffer = ''
            raise ValueError('frame excede o limite')
        try:
            frame = json.loads(self.buffer, parse_constant=lambda value: (_ for _ in ()).throw(ValueError('número não finito')))
        except json.JSONDecodeError:
            return None
        finally:
            if len(self.buffer) > MAX_FRAME_BYTES:
                self.buffer = ''
        self.buffer = ''
        return frame


def integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f'{name} inválido')
    return value


@dataclass
class Reading:
    payload: dict
    sequence: int
    uptime_ms: int
    firmware: str
    captured_at: str
    arrived: float
    machine_id: str | None = None


def reading_from(frame):
    if not isinstance(frame, dict):
        raise ValueError('frame deve ser objeto')
    if frame.get('protocol') != 1 or 'payload' not in frame:
        raise ValueError('protocolo USB incompatível')
    identity = frame.get('machine_id')
    if identity is not None:
        if isinstance(identity, bool) or not isinstance(identity, (str, int)) or not str(identity).strip() or len(str(identity).strip()) > 36:
            raise ValueError('machine_id inválido')
        identity = str(identity).strip()
    payload = copy.deepcopy(frame['payload'])
    sequence = integer(frame.get('sequence'), 'sequence')
    uptime = integer(frame.get('uptime_ms'), 'uptime_ms')
    if not isinstance(payload, dict) or not isinstance(payload.get('machine_active'), bool):
        raise ValueError('machine_active deve ser booleano')
    if payload.get('voltage_24v') is not None and not isinstance(payload['voltage_24v'], bool):
        raise ValueError('voltage_24v inválido')
    for key in ('digital_signals', 'analog_signals', 'extra_signals'):
        if key in payload and not isinstance(payload[key], dict):
            raise ValueError(f'{key} deve ser objeto')
    if any(not isinstance(v, bool) for v in payload.get('digital_signals', {}).values()):
        raise ValueError('digital_signals deve conter booleanos')
    extra = payload.setdefault('extra_signals', {})
    extra['transport'] = 'usb_serial'
    extra['timestamp_source'] = 'usb_host_receive'
    extra['uptime_seconds'] = uptime // 1000
    return Reading(payload, sequence, uptime, str(frame.get('firmware_version', 'opta-monitor-usb-2.0.0'))[:50],
                   datetime.now(timezone.utc).isoformat(), time.monotonic(), identity)


class HttpApi:
    def __init__(self, base_url, key=''):
        self.base_url, self.key = base_url.rstrip('/'), key

    def post(self, path, body):
        headers = {'Content-Type':'application/json'}
        if self.key:
            headers['X-Device-Key'] = self.key
        req = urllib.request.Request(self.base_url + path, json.dumps(body, allow_nan=False).encode(), headers)
        with urllib.request.urlopen(req, timeout=3) as response:
            return json.load(response)


class StdoutEvents:
    def post(self, path, payload):
        print(json.dumps(payload, ensure_ascii=False, allow_nan=False), flush=True)
        return {'id': payload.get('event_id', 'stdout')}


class Gateway:
    """Adapta a aquisição para eventos de máquina; cadastro por MAC é compatibilidade."""
    def __init__(self, api, mac=None, device_id=None, machine_id=None):
        self.api, self.mac, self.device_id = api, mac, device_id
        self.machine_id = machine_id
        self.use_frame_machine = not (machine_id or mac or device_id)
        self.session = str(uuid4())
        self.previous = None
        self.previous_payload = None

    def payload_for(self, reading):
        current = (reading.sequence, reading.uptime_ms)
        if current == self.previous:
            return copy.deepcopy(self.previous_payload)
        if self.previous and (current[0] < self.previous[0] or current[1] < self.previous[1]):
            self.session = str(uuid4())  # Reboot do Opta: não reutilizar event_id.
        self.previous = current
        data = copy.deepcopy(reading.payload)
        data['event_id'] = f'{self.session}:{reading.sequence}'
        data['timestamp'] = reading.captured_at  # Recepção USB UTC, preservada nos retries.
        data['extra_signals']['boot_id'] = self.session
        if self.machine_id or self.use_frame_machine:
            data = {'machine_id': self.machine_id or reading.machine_id or '1', 'states': data.get('digital_signals', {}),
                    'event_id': data['event_id'], 'timestamp': data['timestamp']}
        self.previous_payload = copy.deepcopy(data)
        return data

    def send(self, reading, payload):
        if 'machine_id' in payload:
            return self.api.post('/events', payload)
        if not self.device_id:
            result = self.api.post('/devices/register', {'mac_address':self.mac, 'ip_address':None,
                                                        'firmware_version':reading.firmware})
            self.device_id = str(UUID(result['device']['id']))
            print('Coletor cadastrado:', self.device_id, file=sys.stderr, flush=True)
        return self.api.post(f'/devices/{self.device_id}/telemetry', payload)


def sender(gateway, pending, stop):
    while not stop.is_set():
        try:
            reading = pending.get(timeout=1)
        except queue.Empty:
            continue
        payload = gateway.payload_for(reading)
        backoff = 1
        while not stop.is_set() and time.monotonic() - reading.arrived < MAX_PENDING_SECONDS:
            try:
                result = gateway.send(reading, payload)
                label = 'Evento emitido' if isinstance(getattr(gateway, 'api', None), StdoutEvents) else 'HTTP confirmado'
                print(f'{label} | seq={reading.sequence} | leitura={result.get("id", "ok")}', file=sys.stderr, flush=True)
                break
            except BrokenPipeError:
                stop.set()
                return
            except urllib.error.HTTPError as error:
                print(f'API HTTP {error.code}; confira cadastro/chave/contrato.', file=sys.stderr, flush=True)
                if error.code == 404 and gateway.mac:
                    gateway.device_id = None
                elif error.code < 500 and error.code not in (404, 408, 429):
                    break
            except (OSError, ValueError, KeyError, urllib.error.URLError):
                print('API indisponível ou resposta inválida; repetindo a mesma leitura.', file=sys.stderr, flush=True)
            stop.wait(backoff)
            backoff = min(backoff * 2, 4)


def receive(port, pending, stop):
    """Read serial independently from HTTP; keep the latest waiting frame."""
    frames, line = Frames(), bytearray()
    last_frame = time.monotonic()
    while not stop.is_set():
        for byte in port.read(256):
            if byte == 10:
                text = line.decode('utf-8', errors='replace').rstrip('\r')
                line.clear()
                try:
                    frame = frames.feed(text)
                    if frame is None:
                        continue
                    reading = reading_from(frame)
                except (ValueError, TypeError, AttributeError):
                    frames.buffer = ''
                    print('Frame USB inválido; aguardando próximo.', file=sys.stderr, flush=True)
                    continue
                last_frame = time.monotonic()
                try:
                    pending.get_nowait()
                except queue.Empty:
                    pass
                pending.put_nowait(reading)
            elif len(line) < MAX_FRAME_BYTES:
                line.append(byte)
            else:
                line.clear(); frames.buffer = ''
        if time.monotonic() - last_frame >= 10:
            print('Sem telemetria USB há 10s; confira firmware/cabo/porta.', file=sys.stderr, flush=True)
            last_frame = time.monotonic()


def main():
    import serial
    from dotenv import load_dotenv
    root = Path(__file__).resolve().parents[1]
    load_dotenv(root / 'backend' / '.env', override=False)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--porta', '--port', help='/dev/serial/by-id/... ou /dev/ttyACM0 (Windows: COM4)')
    parser.add_argument('--listar-portas', action='store_true', help='Lista portas USB/serial e encerra')
    parser.add_argument('--api', default='http://127.0.0.1:8000/api')
    parser.add_argument('--stdout', action='store_true', help='Emite eventos JSON Lines sem rede; usa o ID do firmware (padrão 1) ou --machine-id')
    identity = parser.add_mutually_exclusive_group()
    identity.add_argument('--machine-id', help='Substitui o ID enviado no firmware; omitido usa o ID serial (padrão 1)')
    identity.add_argument('--mac', help='MAC real do Opta usado no cadastro existente')
    identity.add_argument('--device-id', help='UUID existente do Opta (preserva o vínculo com a CNC)')
    args = parser.parse_args()
    if args.listar_portas:
        from serial.tools import list_ports
        for port in sorted(list_ports.comports(), key=lambda port: port.device):
            print(f'{port.device} | {port.description} | serial={port.serial_number or "não informado"}')
        return
    if not args.porta:
        parser.error('Informe --porta; ou use --listar-portas')
    if args.stdout and (args.mac or args.device_id):
        parser.error('--stdout usa o ID do firmware ou --machine-id, sem cadastro de coletor')
    if args.machine_id and (not args.machine_id.strip() or len(args.machine_id.strip()) > 36):
        parser.error('--machine-id deve conter entre 1 e 36 caracteres')
    if args.mac and not re.fullmatch(r'[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}', args.mac):
        parser.error('--mac inválido')
    if args.device_id:
        try:
            args.device_id = str(UUID(args.device_id))
        except ValueError:
            parser.error('--device-id deve ser UUID')
    pending, stop = queue.Queue(maxsize=1), threading.Event()
    api = StdoutEvents() if args.stdout else HttpApi(args.api, os.getenv('INGEST_API_KEY') or os.getenv('DEVICE_API_KEY', ''))
    gateway = Gateway(api, args.mac, args.device_id, args.machine_id)
    worker = threading.Thread(target=sender, args=(gateway, pending, stop), daemon=True)
    worker.start()
    try:
        while not stop.is_set():
            try:
                with serial.Serial(args.porta, 115200, timeout=1,
                                   **({'exclusive': True} if os.name == 'posix' else {})) as port:
                    print(f'USB {args.porta} -> {args.api}', file=sys.stderr, flush=True)
                    receive(port, pending, stop)
            except serial.SerialException:
                print('Porta USB indisponível; confira cabo, caminho, permissões (grupo dialout no Linux) e feche outros leitores.', file=sys.stderr, flush=True)
                stop.wait(2)
    except KeyboardInterrupt:
        print('\nPonte encerrada.', file=sys.stderr)
    finally:
        stop.set()
        worker.join(timeout=4)


if __name__ == '__main__':
    main()
