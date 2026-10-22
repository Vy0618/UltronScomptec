# U.L.T.R.O.N — correções e testes da integração Wi-Fi

Rodada concluída em 21/10/2026. Cenário: notebook hospeda API e dashboard; notebook e Opta deverão usar o hotspot `maker`, senha `12345678`. Nenhum Opta físico estava disponível. Não houve upload de firmware, acesso a sensores reais ou alteração de firewall/rede do Windows.

## Resultado da rodada final

Comando executado na raiz, com a URL do MySQL isolado disponível apenas para os testes opcionais:

```powershell
$env:ULTRON_TEST_MYSQL_URL = 'mysql+pymysql://root:@127.0.0.1:3307/ultron_test_wifi?charset=utf8mb4'
.\tools\testarProjeto.ps1 -Firmware
```

| Verificação | Resultado |
|---|---|
| Firmware C++ em host | 12 cenários aprovados |
| Firmware para `arduino:mbed_opta:opta` | Compilação aprovada |
| Backend, ponte USB, integração e concorrência | 53 testes aprovados; nenhum skip nessa rodada |
| Lógica e integração de serviços frontend | 25 testes aprovados |
| Lint frontend | Código 0, sem erros; 54 avisos existentes |
| Build frontend | Aprovado; aviso de bundle acima de 500 kB |
| HTTP real → API → SQLite | 20 verificações aprovadas, 13 amostras |
| HTTP real → API → MySQL 8.4.13 | 20 verificações aprovadas, 13 amostras |
| Inicializador: parar e reiniciar | Aprovado; API, dashboard e dispositivo virtual respondendo |
| ZIP do firmware | 12 arquivos conferidos contra os fontes; sem configuração privada |

Log da rodada final: `../../.local/testes/20261021-203708-327/resumo.json`. O apontador `../../.local/testes/ultimo-resumo.json` é atualizado a cada execução. Os cenários HTTP estão em `../../.local/relatorio-http-sqlite.json` e `../../.local/relatorio-http-mysql.json`.

A compilação utilizou Arduino CLI 1.5.1, core Opta 4.6.0 e ArduinoJson 7.4.2: 270.852 bytes de programa (13%) e 70.208 bytes de memória global (13%). As ferramentas ficam em `.tools`; os resultados, em `.build`. Nenhum instalador Electron foi gerado.

O MySQL foi baixado da Oracle, com checksum comparado ao publicado, e executado como instância portátil apenas em `127.0.0.1:3307`, banco `ultron_test_wifi`, dentro de `.local/mysql-data`. Foi encerrado depois dos testes. Nenhum serviço Windows ou banco preexistente foi modificado. Para repetir os testes MySQL, essa instância ou outro banco local isolado `ultron_test...` precisa estar disponível; sem a variável, esses três casos são explicitamente ignorados.

## O que foi efetivamente simulado

Os testes C++ executam o `mesaControl.cpp` real com entradas GPIO e passagem de tempo simuladas. Cobrem peça metálica pequena, metálica média/grande, peça não metálica, janela de metal, duração dos desviadores, timeout de altura, recuperação, ocupação de rampa e alimentação de uma peça por vez. Pinos, regras e tempos do controle foram preservados.

Os testes de telemetria exercitam o mesmo núcleo C++ usado pelo firmware: fila limitada, descarte, relógio e rollover de `millis()`, identidade de boot, evento estável, retries, 404, parser estrutural de cadastro e framing HTTP com tamanho, chunked, fechamento, truncamento e timeout. O serializador real produz seis JSON que os testes Python enviam sem alterações à API, validando persistência, estado, sinais, mesa e deduplicação.

O simulador Python exercita o contrato por HTTP real: registro por MAC, sete estados da mesa, rampa, horário de captura, resposta perdida, reenvio idempotente, recadastro, reboot, leitura atrasada, pausa/offline, retomada, histórico e utilização. Ele identifica seus registros como `SIMULADO` e inclui `simulated: true`. É uma simulação do contrato e não executa o rádio ou o firmware Mbed.

Os testes MySQL fazem cadastros concorrentes do mesmo MAC, cadastros concorrentes de MACs diferentes e envios simultâneos do mesmo evento. Confirmaram unicidade do par e dos códigos, e uma única leitura para o evento repetido.

## Correções implementadas

- Removida API Wi-Fi específica do ESP32; uso da API Mbed do Opta e timeouts de socket/resposta.
- Resposta de cadastro interpretada como JSON e respostas HTTP completas verificadas antes de confirmar envio.
- Boot estável através de reconexões; JSON, evento e horário de cada leitura pendente congelados nos retries.
- Recadastro automático após HTTP 404, sem renomear a sessão física corrente.
- Timestamp de captura estimado pelo horário do registro e relógio monotônico; fonte da estimativa identificada.
- Fila RAM de 16 leituras mais uma pendente, heartbeat e captura de transições relevantes; descartes diagnosticados e contabilizados.
- Frescor de coleta coerente com a tolerância temporal da ingestão; duração operacional reiniciada após lacuna de observação; PUT da CNC retorna estado efetivo.
- Falhas globais preservam alertas conhecidos. Falha de uma CNC não derruba a frota inteira; falha de histórico/utilização mantém o estado atual.
- Notificações de transições reais, sem repetições na recuperação; cartões distinguem amostras de ocorrências; média fictícia de potência removida; atalhos dos detalhes preservam roteamento por hash.
- Inicialização local com banco isolado, sem carregar `.env` real no modo simulado; restauração do ambiente do chamador, logs, verificação de portas e encerramento da árvore dos processos próprios.
- ZIP regenerado com os fontes atuais; configuração do notebook em arquivo local excluído do pacote.

## Conferência visual

A dashboard real foi aberta em `http://localhost:5173/dashboard`, consumindo a API local sem mocks. Foram conferidos dashboard, listagem, detalhes, sinais e contadores da mesa, ausência de medidas analógicas, amostras no histórico e aviso de emergência sintética. A API foi interrompida: a tela mostrou indisponibilidade e alerta conhecido identificado como desatualizado, sem afirmar conformidade. Depois, os serviços foram reiniciados e a telemetria voltou a atualizar.

Evidência visual: `../../.local/dashboard-validada.png`. O modo TV e os componentes administrativos compartilham os serviços testados; esta rodada não constitui uma inspeção visual de cada tela nem um ensaio do executável Electron empacotado.

## Repetição e limites

```powershell
.\iniciarLocal.ps1 -Simular
# Abrir http://localhost:5173/dashboard
.\tools\testarProjeto.ps1 -Firmware
.\iniciarLocal.ps1 -Acao parar
```

A validação comprova o código compilável e os cenários executados. Permanecem pendentes: associação física ao hotspot maker, isolamento entre clientes do celular, firewall do notebook, polaridades e níveis elétricos, Wi-Fi/driver Mbed em execução, escalonamento RTOS e movimentos dos relés/atuadores. A fila é volátil e limitada; não promete recuperar toda interrupção prolongada nem todos os flancos dos sensores. O horário UTC é uma estimativa de rede, sem precisão industrial garantida. Os avisos de lint/deprecação e tamanho de bundle foram registrados e não impediram os testes.
