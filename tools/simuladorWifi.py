"""Simulação HTTP do contrato Opta WiFi; não emula eletrônica nem rádio.

Use com o backend de teste/SQLite iniciado por iniciarLocal.ps1 -Simular.
Nenhum dispositivo/CNC existente é excluído pelo cenário de recuperação.
"""
import argparse
import copy
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request
from uuid import uuid4

MESA_STATES = ("aguardando_peca", "coletando_altura", "aguardando_metal", "acionando_queda1",
               "acionando_queda2", "aguardando_reto", "falha")


@dataclass
class Response:
    status: int
    body: object


class HttpApi:
    def __init__(self, base_url, device_key="", timeout=10):
        parsed = urllib.parse.urlparse(base_url)
        if parsed.scheme != "http" or parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise ValueError("O simulador deve apontar para um backend HTTP local de teste")
        self.base_url = base_url.rstrip("/")
        self.device_key = device_key
        self.timeout = timeout

    def request(self, method, path, payload=None):
        body = json.dumps(payload, allow_nan=False).encode("utf-8") if payload is not None else None
        headers = {"Content-Type": "application/json", "X-Device-Key": self.device_key}
        request = urllib.request.Request(self.base_url + path, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return Response(response.status, json.loads(response.read()))
        except urllib.error.HTTPError as error:
            return Response(error.code, json.loads(error.read()))


class OptaSimulator:
    """Preserves a prepared payload across reconnects; only reboot changes boot_id."""
    def __init__(self, api, mac=None, now=None):
        self.api = api
        self.mac = mac or "02:" + ":".join(f"{byte:02X}" for byte in uuid4().bytes[:5])
        self.now = now or (lambda: datetime.now(timezone.utc))
        self.started_at = self.now() - timedelta(seconds=60)
        self.clock_offset = timedelta(0)
        self.device_id = None
        self.cnc_id = None
        self.boot_id = None
        self.sequence = 0

    def register(self):
        response = self.api.request("POST", "/devices/register", {
            "mac_address": self.mac, "ip_address": "127.0.0.1", "firmware_version": "SIMULACAO-wifi-2.0",
        })
        require(response.status == 201, f"Cadastro retornou {response.status}: {response.body}")
        data = response.body
        self.device_id, self.cnc_id = data["device"]["id"], data["cnc"]["id"]
        for path, name in ((f"/cncs/{self.cnc_id}", "SIMULADO — Mesa Opta"),
                           (f"/devices/{self.device_id}", "SIMULADO — Opta WiFi")):
            labeled = self.api.request("PUT", path, {"name": name})
            require(labeled.status == 200, f"Não foi possível identificar os dados simulados: {labeled.body}")
        if self.boot_id is None:
            self.boot_id = data["telemetry_session_id"]
        server_time = datetime.fromtimestamp(data["server_time_unix"], timezone.utc)
        self.clock_offset = server_time - self.now().replace(microsecond=0)
        return data

    def prepare(self, state="aguardando_peca", *, delay_seconds=0, ramp_full=False):
        require(bool(self.boot_id), "Cadastre o Opta antes de preparar uma leitura")
        self.sequence += 1
        fault = state == "falha"
        active = state not in {"aguardando_peca", "falha"}
        captured_at = self.now() + self.clock_offset - timedelta(seconds=delay_seconds)
        uptime_ms = max(0, int((self.now() - self.started_at).total_seconds() * 1000))
        return {
            "event_id": f"{self.boot_id}:{self.sequence}",
            "timestamp": captured_at.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "machine_active": active, "voltage_24v": None,
            "digital_signals": {
                "ciclo": active, "alarme": fault, "altura_media_bloqueada": False,
                "altura_pequena_bloqueada": True, "altura_grande_bloqueada": False,
                "metal_presente": True, "queda1_ocupada": state == "acionando_queda1",
                "queda2_ocupada": state == "acionando_queda2",
                "rampa1_cheia": ramp_full, "rampa2_cheia": False,
            },
            "analog_signals": {},
            "extra_signals": {
                "transport": "wifi_http", "simulated": True, "uptime_seconds": uptime_ms // 1000,
                "boot_id": self.boot_id, "amostras_descartadas": 0,
                "timestamp_source": "server_registration_estimate",
                "mesa": {
                    "estado": state, "altura": "pequena", "metal_memorizado": True,
                    "rampa1_cheia": ramp_full, "rampa2_cheia": False,
                    "capturado_millis": max(0, uptime_ms - int(delay_seconds * 1000)),
                    "entradas_brutas": {"I1": False, "I2": True, "I3": False, "I4": True,
                                        "I5": True, "I6": state == "acionando_queda1", "I7": state == "acionando_queda2"},
                    "saidas_comandadas": {"O1": True, "O2": state == "acionando_queda1", "O3": state == "acionando_queda2"},
                    "contadores": {"total": 3, "reto": 1, "queda1": 1, "queda2": 1, "falhas": int(fault)},
                },
            },
        }

    def send(self, payload):
        response = self.api.request("POST", f"/devices/{self.device_id}/telemetry", payload)
        if response.status == 404:
            self.register()
            # Keep every field, including event_id and collection timestamp.
            response = self.api.request("POST", f"/devices/{self.device_id}/telemetry", payload)
        require(response.status == 201, f"Telemetria retornou {response.status}: {response.body}")
        return response.body

    def status(self):
        response = self.api.request("GET", f"/cncs/{self.cnc_id}/status")
        require(response.status == 200, f"Consulta de estado falhou: {response.body}")
        return response.body

    def history(self):
        response = self.api.request("GET", f"/cncs/{self.cnc_id}/history?limit=500")
        require(response.status == 200, f"Consulta de histórico falhou: {response.body}")
        return response.body


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def run_scenario(api, *, mac=None, offline_timeout=90, sleep=time.sleep, now=None, progress=None):
    """Runs real HTTP/DB operations with synthetic sensor data and a timed outage."""
    require(offline_timeout >= 10, "O timeout do backend deve ser pelo menos 10 segundos")
    checks = []
    def check(name, condition, detail=""):
        require(condition, f"{name}: {detail}")
        checks.append({"name": name, "passed": True, "detail": detail})
        if progress:
            progress(f"OK: {name}")

    simulator = OptaSimulator(api, mac=mac, now=now)
    registration = simulator.register()
    original_device = simulator.device_id
    check("cadastro_e_vinculo", bool(registration["cnc"]["id"] and simulator.boot_id))

    delayed = simulator.prepare(delay_seconds=3)
    accepted = simulator.send(delayed)
    collection = datetime.fromisoformat(accepted["timestamp"].replace("Z", "+00:00"))
    reception = datetime.fromisoformat(accepted["received_at"].replace("Z", "+00:00"))
    check("horario_de_captura_preservado", (reception - collection).total_seconds() >= 2)
    check("sensores_ausentes_sem_dados_inventados", accepted["voltage_24v"] is None and accepted["analog_signals"] == {})

    for state in MESA_STATES:
        payload = simulator.prepare(state)
        simulator.send(payload)
        snapshot = simulator.status()
        expected = "ALARME" if state == "falha" else ("PARADA" if state == "aguardando_peca" else "OPERANDO")
        check(f"estado_{state}", snapshot["status"] == expected and snapshot["extra_signals"]["mesa"]["estado"] == state)

    full_ramp = simulator.prepare("aguardando_peca", ramp_full=True)
    simulator.send(full_ramp)
    check("rampa_cheia_preservada", simulator.status()["digital_signals"]["rampa1_cheia"] is True)

    pending = simulator.prepare("aguardando_reto")
    frozen_pending = copy.deepcopy(pending)
    first = simulator.send(pending)  # Deliberately discard this acknowledgement.
    before_count = simulator.history()["total"]
    before_boot = simulator.boot_id
    simulator.register()  # WiFi reconnect, same physical boot.
    retried = simulator.send(pending)
    check("resposta_perdida_reenvio_idempotente", first["id"] == retried["id"] and simulator.history()["total"] == before_count)
    check("reconexao_preserva_identidade_e_payload", simulator.boot_id == before_boot and pending == frozen_pending and simulator.device_id == original_device)

    simulator.device_id = str(uuid4())  # Induce a stale UUID without deleting any historical data.
    recovered = simulator.send(pending)
    check("404_recadastra_sem_duplicar", recovered["id"] == first["id"] and simulator.device_id == original_device and simulator.history()["total"] == before_count)

    rebooted = OptaSimulator(api, mac=simulator.mac, now=now)
    rebooted.register()
    reboot_payload = rebooted.prepare("aguardando_reto")
    rebooted.send(reboot_payload)
    check("reboot_nova_sessao_mesma_cnc", rebooted.boot_id != before_boot and rebooted.device_id == original_device and rebooted.cnc_id == simulator.cnc_id and reboot_payload["event_id"] != pending["event_id"])
    simulator = rebooted

    # Historical delivery must not revert the latest operational state.
    simulator.send(simulator.prepare("falha", delay_seconds=offline_timeout + 5))
    check("atraso_nao_reverte_estado", simulator.status()["status"] == "OPERANDO")
    if progress:
        progress(f"Pausa simulada de {offline_timeout + 1}s; aguardando SEM_COMUNICACAO...")
    before_since = simulator.status()["status_since"]
    sleep(offline_timeout + 1)
    check("pausa_detecta_sem_comunicacao", simulator.status()["status"] == "SEM_COMUNICACAO")
    resumed = simulator.send(simulator.prepare("aguardando_reto"))
    snapshot = simulator.status()
    check("retomada_restabelece_estado_e_duracao", snapshot["status"] == "OPERANDO" and snapshot["status_since"] == resumed["timestamp"] and snapshot["status_since"] != before_since)

    history = simulator.history()
    utilization = api.request("GET", f"/cncs/{simulator.cnc_id}/utilization")
    check("historico_e_utilizacao_disponiveis", history["total"] >= 13 and utilization.status == 200 and len(utilization.body["buckets"]) == 24)
    check("sinais_da_mesa_preservados", all(key in snapshot["extra_signals"]["mesa"] for key in ("entradas_brutas", "saidas_comandadas", "contadores", "capturado_millis")))
    return simulator, {
        "simulation": True, "passed": True, "hardware_verified": False, "transport": "wifi_http_contract",
        "mac_address": simulator.mac, "device_id": simulator.device_id, "cnc_id": simulator.cnc_id,
        "offline_timeout_seconds": offline_timeout, "samples": history["total"], "checks": checks,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api", default="http://127.0.0.1:8000/api")
    parser.add_argument("--device-key", default=os.getenv("DEVICE_API_KEY", ""))
    parser.add_argument("--mac", help="MAC exclusivo da simulação; omitido gera MAC local aleatório")
    parser.add_argument("--offline-timeout", type=int, default=90, help="Mesmo DEVICE_OFFLINE_TIMEOUT_SECONDS do backend")
    parser.add_argument("--apenas-stream", "--stream-only", action="store_true", help="Publica leituras sem repetir o cenário de testes")
    parser.add_argument("--stream-seconds", type=int, default=0, help="Heartbeat por N segundos; -1 mantém até Ctrl+C")
    parser.add_argument("--stream-state", choices=("cycle", *MESA_STATES), default="cycle", help="cycle alterna os sete estados da mesa a cada 5 segundos")
    parser.add_argument("--report", type=Path, help="Salva o resultado JSON neste arquivo antes do streaming")
    args = parser.parse_args()
    try:
        api = HttpApi(args.api, args.device_key)
        print("SIMULAÇÃO: sensores sintéticos; rádio, relés e Opta físico não são exercitados.", flush=True)
        if args.apenas_stream:
            simulator = OptaSimulator(api, mac=args.mac)
            simulator.register()
            report = {"simulation": True, "hardware_verified": False, "mode": "stream",
                      "device_id": simulator.device_id, "cnc_id": simulator.cnc_id, "mac_address": simulator.mac,
                      "stream_state": args.stream_state}
        else:
            simulator, report = run_scenario(api, mac=args.mac, offline_timeout=args.offline_timeout, progress=lambda message: print(message, flush=True))
        report["generated_at"] = datetime.now(timezone.utc).isoformat()
        report["api_base_url"] = api.base_url
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
        stream_started = time.monotonic()
        deadline = time.monotonic() + max(0, args.stream_seconds)
        while args.stream_seconds < 0 or time.monotonic() < deadline:
            state = MESA_STATES[int((time.monotonic() - stream_started) // 5) % len(MESA_STATES)] if args.stream_state == "cycle" else args.stream_state
            simulator.send(simulator.prepare(state))
            time.sleep(1)
    except KeyboardInterrupt:
        print("Simulação encerrada.", flush=True)
        return 0
    except (AssertionError, ValueError, OSError, urllib.error.URLError, json.JSONDecodeError) as error:
        print(f"FALHA NA SIMULAÇÃO: {error}", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
