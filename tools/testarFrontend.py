"""Browser regression checks against a production preview and an isolated API.

Usage: python tools/testarFrontend.py --url http://127.0.0.1:5174
Requires Playwright and a Chromium installation; see docs/guides/testesResponsividade.md.
No requests reach the installation's database or hardware.
"""
import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from types import SimpleNamespace
import sys
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from services.signalOutputs import derive_signal_outputs


def run(url, output, executable=None):
    output.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    timestamp = lambda seconds=0: (now - timedelta(seconds=seconds)).isoformat()
    states = ["OPERANDO", "PARADA", "ALARME", "EMERGENCIA", "SEM_COMUNICACAO", "DADOS_DESATUALIZADOS", "MANUTENCAO", "DESLIGADA"]
    machines = [{"id": f"test-{i}", "code": f"CNC-{i+1:03d}", "name": f"Centro de usinagem {i+1}", "description": "API isolada de teste"} for i in range(40)]
    user = {"id": "test-user", "name": "Operador de Teste", "email": "teste@example.invalid", "role": "admin", "active": True}
    calls = Counter()
    unavailable = set()

    def signals(index):
        status = states[index % len(states)]
        return {"ativo": status == "OPERANDO", "inativo": status == "PARADA", "emergencia": status == "EMERGENCIA", "motor_ligado": True, "alarme": status == "ALARME", "porta_aberta": status == "EMERGENCIA"}

    def reading(index, sample):
        data = {"id": f"reading-{index}-{sample}", "machine_id": f"test-{index}", "timestamp": timestamp(sample), "states": signals(index), "analog_signals": {"current": 12.5} if index == 0 else {}, "voltage_24v": None}
        data["signal_outputs"] = outputs(data)
        return data

    def outputs(data):
        return derive_signal_outputs(SimpleNamespace(digital_signals=data["states"],
            machine_active=data["states"].get("ativo", False), analog_signals=data.get("analog_signals", {}), extra_signals=data.get("extra_signals", {})))

    def mock(route):
        parsed = urlparse(route.request.url)
        assert parsed.netloc == urlparse(url).netloc, "Gere o build de teste com VITE_API_BASE_URL=/api para conferir o acesso pela mesma origem."
        path = parsed.path
        params = parse_qs(parsed.query)
        calls[path] += 1
        if path in unavailable:
            route.fulfill(status=503, json={"detail": "Falha simulada"})
            return
        if path == "/api/cncs/statuses":
            data = [{**machine, "status": states[i % len(states)], "online": i % len(states) not in (4, 5), "states": signals(i), "analog_signals": {}, "last_seen": timestamp(2), "telemetry_timestamp": timestamp(2), "status_since": timestamp(300), "last_known_status": "OPERANDO"} for i, machine in enumerate(machines)]
            for i, item in enumerate(data):
                item["diagnostics"] = [{"code": "PORTA_ABERTA_EMERGENCIA", "severity": "EMERGENCIA", "title": "Operação falha", "message": "Porta aberta e emergência acionada na mesma leitura.", "signals": ["porta_aberta", "emergencia"]}] if item["status"] == "EMERGENCIA" else []
                if i == 0:
                    item["analog_signals"] = {"current": 12.5}
                    item["extra_signals"] = {"current_input": {"input": "I8", "physical_enabled": False, "unit": "A", "source": "simulated"}}
                item["signal_outputs"] = outputs(item)
        elif path == "/api/cncs/history":
            page = int(params.get("page", [1])[0]); limit = int(params.get("limit", [30])[0])
            machine_id = params.get("machine_id", [None])[0]
            rows = [reading(i, sample) for sample in range(4) for i in range(len(machines)) if not machine_id or machines[i]["id"] == machine_id]
            data = {"items": rows[(page-1)*limit:page*limit], "total": len(rows), "page": page, "limit": limit}
        elif path.endswith("/history"):
            index = int(path.split("/")[3].split("-")[-1])
            data = {"items": [reading(index, sample) for sample in range(100)], "total": 100, "page": 1, "limit": 100}
        elif path.endswith("/utilization"):
            data = {"buckets": [{"timestamp": timestamp((24-i)*3600), "duration_seconds": 3600, "samples": 100, "seconds": {"OPERANDO": 3000, "PARADA": 300, "ALARME": 200, "EMERGENCIA": 100, "MANUTENCAO": 0, "DESLIGADA": 0}} for i in range(24)]}
        elif path == "/api/auth/me":
            data = user
        elif path == "/api/admin/state":
            data = {"users": [user], "audit": [], "incidents": [], "rules": {"current": 22, "temperature": 65, "voltageMin": 200, "voltageMax": 240}}
        elif path == "/api/devices" or path.endswith("/incidents"):
            data = []
        else:
            raise AssertionError(f"Consulta inesperada: {route.request.method} {path}")
        route.fulfill(status=200, json=data)

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(**({"executable_path": executable} if executable else {}))
        for width, height in [(320, 568), (390, 844), (640, 900), (768, 1024), (1024, 768), (1366, 768), (1920, 1080)]:
            context = browser.new_context(viewport={"width": width, "height": height}, is_mobile=width < 768, has_touch=width < 768, locale="pt-BR", reduced_motion="reduce")
            context.route("**/api/**", mock)
            context.route("https://fonts.googleapis.com/**", lambda route: route.fulfill(status=200, body="", content_type="text/css"))
            context.add_init_script("localStorage.setItem('scomptec_user', " + json.dumps(json.dumps(user)) + "); localStorage.setItem('scomptec_access_token', 'test-token');")
            # Test failures are collected from both console and uncaught exceptions.
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("console", lambda message: errors.append(message.text) if message.type == "error" and "fonts." not in message.text else None)
            routes = [("/login", "Autenticação de Operador"), ("/maquinas", "Máquinas CNC"), ("/dashboard", "Status da Operação CNC:"), ("/maquinas/CNC-001", "Centro de usinagem 1"), ("/historico", "Histórico de Leituras"), ("/configuracoes", "Configurações da Conta"), ("/admin", "Central de controle"), ("/tv", "Monitoramento de máquinas")]
            if width in (320, 1366):
                routes += [("/inicio", "Monitoramento inteligente de máquinas CNC, em tempo real."), ("/registro", "Criar Conta Operacional"), ("/recuperar-senha", "Recuperar acesso"), ("/selecionar-empresa", "Bem-vindo, Operador."), ("/clientes", "Clientes Industriais"), ("/unidades", "Unidades e Plantas Fabris"), ("/dispositivos", "Coletores opcionais")]
            for path, label in routes:
                errors.clear(); calls.clear()
                page.goto(url.rstrip("/") + path, wait_until="domcontentloaded")
                if path == "/maquinas/CNC-001":
                    page.get_by_role("heading", name=label, exact=True).wait_for()
                    page.get_by_text("Últimas 100 leituras", exact=False).wait_for()
                    page.get_by_role("heading", name="Corrente · I8 reservada", exact=True).wait_for()
                    page.get_by_text("Valor simulado recebido por comando; não é uma medição física.", exact=True).wait_for()
                    for signal_label in ("Ativo", "Inativo", "Emergência", "Motor ligado", "Alarme / erro", "Porta aberta"):
                        assert page.get_by_text(signal_label, exact=True).count() > 0
                else:
                    if path == "/dashboard":
                        page.get_by_text(label, exact=True).wait_for()
                    else:
                        page.get_by_role("heading", name=label, exact=True).wait_for()
                if path == "/maquinas":
                    page.get_by_role("button", name="Próxima", exact=True).wait_for()
                if path == "/dashboard":
                    page.get_by_text("Atenção Imediata", exact=True).wait_for()
                    page.get_by_role("heading", name="Interações entre sinais", exact=True).wait_for()
                dimensions = page.evaluate("""() => ({width: document.documentElement.clientWidth, content: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth)})""")
                if dimensions["content"] > dimensions["width"] + 1:
                    page.screenshot(path=str(output / f"falha-{width}-{path.replace('/', '_')}.png"), full_page=True)
                    print(page.evaluate("""() => [...document.querySelectorAll('main *, header *')].filter(el => {const r=el.getBoundingClientRect(); return r.width && r.right > document.documentElement.clientWidth+1}).slice(0,12).map(el=>({tag:el.tagName,text:el.textContent.slice(0,80),class:el.className}))"""), flush=True)
                assert dimensions["content"] <= dimensions["width"] + 1, (width, path, dimensions)
                if path in ("/login", "/inicio", "/registro", "/recuperar-senha"):
                    assert not calls, dict(calls)
                if path == "/maquinas":
                    assert calls["/api/cncs/statuses"] == 1, dict(calls)
                    assert len(calls) == 1, dict(calls)
                    cards = page.locator(".machine-grid > button")
                    assert cards.count() == 24
                    for card in cards.all():
                        assert card.evaluate("el => el.scrollWidth <= el.clientWidth + 1"), (width, "Cartão cortado")
                    page.get_by_role("button", name="Próxima", exact=True).click()
                    assert cards.count() == 16
                if path == "/dashboard":
                    assert page.get_by_text("Atenção Imediata", exact=True).bounding_box()["y"] < page.get_by_text("Alertas e Saúde das Máquinas", exact=True).bounding_box()["y"] if width < 1280 else True
                if width < 1024 and path == "/maquinas":
                    page.get_by_role("button", name="Abrir menu", exact=True).click()
                    page.get_by_role("button", name="Fechar menu", exact=True).wait_for()
                    assert page.locator("aside").evaluate("el => !el.inert")
                    assert page.evaluate("getComputedStyle(document.body).overflow") == "hidden"
                    page.keyboard.press("Escape")
                    assert page.locator("aside").evaluate("el => el.inert")
                    assert page.get_by_role("button", name="Abrir menu", exact=True).evaluate("el => el === document.activeElement")
                    page.get_by_role("button", name="Buscar máquinas", exact=True).click()
                    page.get_by_label("Buscar máquinas por nome ou código", exact=True).fill("CNC-040")
                    page.get_by_role("button", name="Buscar", exact=True).click()
                    page.wait_for_url("**/maquinas?busca=CNC-040")
                    page.wait_for_function("document.querySelectorAll('.machine-grid > button').length === 1")
                    assert cards.count() == 1
                if width < 768 and path == "/dashboard":
                    controls = page.locator("header").first.locator("button").all()
                    boxes = [button.bounding_box() for button in controls if button.is_visible()]
                    for a, b in zip(boxes, boxes[1:]):
                        assert a["x"] + a["width"] <= b["x"] + 1, (width, "Cabeçalho sobreposto")
                    page.get_by_role("button", name="Trocar contexto:", exact=False).click()
                    box = page.get_by_role("dialog", name="Trocar contexto", exact=True).bounding_box()
                    assert box["x"] >= 0 and box["x"] + box["width"] <= width
                    page.keyboard.press("Escape")
                    page.get_by_text("Alertas e Saúde das Máquinas", exact=True).scroll_into_view_if_needed()
                    page.get_by_text("Tempo em alerta", exact=True).first.wait_for()
                if path == "/historico":
                    page.get_by_role("button", name="Tabela Compacta", exact=True).click()
                    page.get_by_role("table").wait_for()
                    page.get_by_role("button", name="Próxima", exact=True).click()
                    page.get_by_text("Página 2 de 6 · 160 registros", exact=True).wait_for()
                    page.get_by_label("Máquina CNC").select_option("test-0")
                    page.get_by_text("Página 1 de 1 · 4 registros", exact=True).wait_for()
                assert not errors, (width, path, list(errors))
                if path in ("/dashboard", "/maquinas/CNC-001") and width in (320, 1024):
                    page.evaluate("window.scrollTo(0, 0)")
                    page.screenshot(path=str(output / f"{width}-{path.replace('/', '_')}.png"), full_page=True, animations="disabled")
                results.append({"width": width, "path": path, "approved": True})
            context.close()
            print(f"OK: {width}x{height}", flush=True)

        # Known emergencies survive failures and recover without false resolutions.
        context = browser.new_context(viewport={"width": 390, "height": 844})
        context.route("**/api/**", mock)
        page = context.new_page()
        page.goto(url.rstrip("/") + "/alertas", wait_until="domcontentloaded")
        page.get_by_role("link").filter(has_text="CNC-004").first.wait_for()
        unavailable.add("/api/cncs/statuses")
        page.get_by_text("Sem conexão com o backend.", exact=False).wait_for(timeout=12000)
        page.get_by_text("Último alerta conhecido.", exact=False).first.wait_for()
        unavailable.clear()
        page.get_by_text("Sem conexão com o backend.", exact=False).wait_for(state="hidden", timeout=12000)
        context.close()
        browser.close()
    (output / "resultado.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(results)} verificações de rota/tela aprovadas; falha e recuperação da API aprovadas.")
    print(f"Relatório e capturas: {output.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:5174")
    parser.add_argument("--output", type=Path, default=Path(".local/testes/frontend"))
    parser.add_argument("--chromium", help="Caminho opcional de um Chromium já instalado")
    args = parser.parse_args()
    run(args.url, args.output, args.chromium)
