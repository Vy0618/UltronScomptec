# Responsividade da dashboard

Comandos para Linux/Bash.

Este teste verifica a adaptação do layout a diferentes tamanhos de tela sem depender do backend ou do Opta. O modo demonstrativo atual inicia com listas vazias; para conferir cartões e gráficos com dados, use também uma API de teste com máquinas e eventos cadastrados. Os comandos devem ser executados na raiz do projeto, com o ambiente `.venv` já criado conforme o [setup do README](../../README.md#setup).

**1. Preparar o frontend e o navegador de teste**

```bash
npm --prefix frontend ci
.venv/bin/python -m pip install playwright
.venv/bin/python -m playwright install chromium
```

A instalação utiliza a biblioteca oficial [Playwright para Python](https://playwright.dev/python/docs/library).

**2. Iniciar a dashboard no primeiro terminal**

```bash
VITE_USE_MOCKS=true npm --prefix frontend run dev -- \
  --host 127.0.0.1 --port 5174 --strictPort
```

Acesse `http://127.0.0.1:5174/dashboard`. Mantenha esse terminal aberto durante o teste. A porta 5174 precisa estar livre; `--strictPort` impede iniciar silenciosamente em outra porta.

**3. Executar o teste em outro terminal, também na raiz do projeto**

O script verifica celular, tablet, notebook e desktop, incluindo os pontos de mudança do layout. Salva capturas da página inteira, do menu quando disponível e um relatório JSON.

```bash
.venv/bin/python - <<'PY'
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

output = Path(".local/testes/responsividade")
output.mkdir(parents=True, exist_ok=True)

sizes = [
    (320, 568),
    (390, 844),
    (639, 900),
    (640, 900),
    (767, 1024),
    (768, 1024),
    (1023, 768),
    (1024, 768),
    (1366, 768),
    (1920, 1080),
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch()

    for width, height in sizes:
        context = browser.new_context(
            viewport={"width": width, "height": height},
            locale="pt-BR",
            reduced_motion="reduce",
        )
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))

        page.goto(
            "http://127.0.0.1:5174/dashboard",
            wait_until="domcontentloaded",
        )
        page.get_by_text(
            "Status da Operação CNC:", exact=True
        ).wait_for(state="visible")

        page.screenshot(
            path=str(output / f"dashboard-{width}x{height}.png"),
            full_page=True,
            animations="disabled",
        )

        dimensions = page.evaluate("""() => ({
            viewport: document.documentElement.clientWidth,
            content: Math.max(
                document.documentElement.scrollWidth,
                document.body.scrollWidth
            )
        })""")

        overflow = dimensions["content"] > dimensions["viewport"] + 1

        menu = page.get_by_role("button", name="Abrir menu", exact=True)
        menu_tested = menu.is_visible()
        if menu_tested:
            menu.click()
            page.screenshot(
                path=str(output / f"menu-{width}x{height}.png"),
                full_page=True,
                animations="disabled",
            )

        result = {
            "resolucao": f"{width}x{height}",
            "rolagem_horizontal": overflow,
            "menu_aberto_para_inspecao": menu_tested,
            "erros_javascript": list(errors),
            "aprovado": not overflow and not errors,
        }
        results.append(result)

        label = "OK" if result["aprovado"] else "FALHOU"
        print(f"{label}: {width}x{height}")
        context.close()

    browser.close()

(output / "resultado.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"\nCapturas e relatório: {output.resolve()}")
raise SystemExit(0 if all(r["aprovado"] for r in results) else 1)
PY
```

**4. Abrir as capturas e o relatório**

```bash
xdg-open .local/testes/responsividade
cat .local/testes/responsividade/resultado.json
```

O resultado automático identifica rolagem horizontal na página e erros JavaScript, retornando código de saída 1 se houver falha. A abertura do menu é registrada para inspeção, mas sua usabilidade não é validada automaticamente. Nas imagens, confira textos cortados, sobreposição de componentes, gráficos legíveis e acesso ao menu. Um resultado `OK` não substitui essa inspeção visual e não mede desempenho, tempo de resposta da API ou comunicação com o Opta.

Ao terminar, encerre a instância demonstrativa com `Ctrl+C` no primeiro terminal.

