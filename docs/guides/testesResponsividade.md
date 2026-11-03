# Navegação e responsividade do frontend

O teste utiliza o build de produção e uma API interceptada no navegador, com 40 máquinas e leituras sintéticas. Não exige backend, banco de dados ou Opta. O modo de demonstração deve ficar desativado para que as consultas percorram a camada real da aplicação e sejam interceptadas pelo teste.

Execute na raiz do projeto, com as dependências instaladas conforme o [README](../../README.md#setup).

## Preparação

```bash
npm --prefix frontend ci
.venv/bin/python -m pip install playwright
.venv/bin/python -m playwright install chromium
VITE_USE_MOCKS=false VITE_API_BASE_URL=/api npm --prefix frontend run build
```

A dependência de navegador é opcional e não integra os requisitos de produção. O teste usa a biblioteca oficial [Playwright para Python](https://playwright.dev/python/docs/library).

## Execução

No primeiro terminal:

```bash
npm --prefix frontend run preview -- --host 127.0.0.1 --port 5174 --strictPort
```

No segundo terminal:

```bash
.venv/bin/python tools/testarFrontend.py --url http://127.0.0.1:5174
```

Um Chromium já instalado pode ser informado com `--chromium /caminho/do/chrome`. O parâmetro `--output` permite alterar a pasta dos resultados.

O script verifica:

- Login sem consultas de monitoramento e listagem com uma consulta coletiva de estados.
- Paginação de 40 máquinas, busca no cabeçalho e histórico global paginado.
- Carregamento direto dos detalhes de uma CNC no build web.
- Menu móvel com bloqueio da rolagem de fundo, Escape, restauração de foco e conteúdo fechado inativo.
- Cabeçalho sem sobreposição, seletor de contexto dentro da tela e cartões sem conteúdo cortado.
- Alertas antes dos gráficos em telas menores.
- Ausência de rolagem horizontal na página e de erros JavaScript/console nas rotas verificadas.
- Preservação de alertas conhecidos quando a API falha e recuperação automática.

São verificadas oito rotas em 320, 390, 640, 768, 1024, 1366 e 1920 pixels de largura, mais sete rotas públicas/auxiliares em 320 e 1366 pixels (70 combinações de rota e largura), além do cenário de falha/recuperação. O processo retorna erro se uma asserção falhar. Capturas e relatório ficam em `.local/testes/frontend/`.

Confira visualmente as capturas, incluindo textos, gráficos e cartões, e faça uma passagem em Android e Safari/iPhone reais, orientação horizontal e zoom. A emulação Chromium não certifica esses navegadores e não mede os Core Web Vitals em usuários reais, a latência do MySQL ou a comunicação elétrica.

Ao terminar, encerre o preview com `Ctrl+C` no primeiro terminal.
