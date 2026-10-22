> **Documentação consolidada:** instalação, rede, firmware e testes atuais estão no [README principal](../../README.md#10-firmware-do-opta-wifi). Este guia complementar contém referências a pacotes/resultados de uma etapa anterior.

# U.L.T.R.O.N — notebook e Opta no hotspot maker

O caminho ativo é **Opta WiFi → HTTP/JSON → FastAPI no notebook → banco → dashboard local**. Como alternativa, o modo USB transmite telemetria pela ponte Python no Linux: consulte [USB no README](../../README.md#usb-no-linux--firmware-porta-e-transmissão). O controle da mesa permanece no Opta.

## Testar agora, sem hardware

Com as dependências instaladas, na raiz:

```powershell
.\iniciarLocal.ps1 -Simular
```

A API escuta em `0.0.0.0:8000`; a dashboard fica em `http://localhost:5173/dashboard`. Um dispositivo virtual alterna os sete estados e aparece como **SIMULADO — Mesa Opta**. O frontend usa a API real (`VITE_USE_MOCKS=false`), com SQLite isolado em `.local/simulacao.db` e timeout de 10 segundos. MySQL permanece o padrão fora desse modo. `ULTRON_SIMULATION=true` impede carregar o `.env` real; a simulação não herda sua conta administrativa ou chave de dispositivo.

Os processos ficam em segundo plano com logs em `.local/`. Para encerrar apenas os processos registrados pelo projeto:

```powershell
.\iniciarLocal.ps1 -Acao parar
```

`-Acao verificar` confere dependências. Também existem `-Acao backend`, `-Acao frontend`, `-PortaApi` e `-PortaDashboard`. Alterar a porta da API exige ajustar `BACKEND_PORT` no firmware.

## Configurar a rede para o Opta

Crie no celular o hotspot **maker**, senha **12345678**, e conecte notebook e Arduino **Opta WiFi** à mesma rede. O Opta Lite não possui Wi-Fi integrado.

No notebook conectado, execute:

```powershell
.\tools\configurarRede.ps1
# Se houver mais de um adaptador/candidato, informe o IPv4 do notebook:
.\tools\configurarRede.ps1 -BackendHost 192.168.43.25
```

O IPv4 acima é apenas exemplo. Use o IPv4 do adaptador Wi-Fi do notebook, visto no `ipconfig`; não use o gateway do celular, `localhost` ou `0.0.0.0` no Opta.

O script gera `firmware/optaMesaMonitor/optaSecrets.h` com as macros de configuração. Esse arquivo é local, ignorado pelo Git e excluído do ZIP. Ele não altera rede ou firewall. Se usar `DEVICE_API_KEY` no backend, passe o mesmo valor com `-DeviceKey`. Recompile e grave o Opta após mudar o IPv4.

O hotspot precisa permitir comunicação entre clientes. O Windows precisa permitir entrada TCP 8000 para o Python na rede usada pelo hotspot. O ensaio sem equipamento não comprova essas condições. Não é necessário publicar a API na Internet ou encaminhar portas no celular.

## Executar com MySQL e Opta físico

Configure `backend/.env` a partir do exemplo, incluindo o MySQL. O banco configurado precisa existir. Depois:

```powershell
.\iniciarLocal.ps1
```

Sem `-Simular`, nenhum dispositivo virtual é iniciado. Backend e dashboard usam a instalação normal. Pare a rodada de simulação antes de iniciar outro servidor nas mesmas portas.

## Compilar e gravar

Abra `firmware/optaMesaMonitor/optaMesaMonitor.ino` com todos os `.cpp` e `.h`. As versões verificadas foram **Arduino Mbed OS Opta Boards 4.6.0**, **ArduinoJson 7.4.2** e Arduino CLI 1.5.1. Consulte o [README principal, seção de firmware](../../README.md#10-firmware-do-opta-wifi) para instalar as ferramentas locais.

O ZIP de distribuição contém os mesmos fontes da pasta ativa, sem configuração privada de rede. Ao extrair em outro notebook, gere novamente `optaSecrets.h`.

## Como a comunicação se recupera

- Registro pelo MAC em `POST /api/devices/register`; envio em `POST /api/devices/{UUID}/telemetry`.
- Identidade de boot mantida nas reconexões; uma leitura pendente conserva JSON, evento e horário em todos os retries.
- HTTP 404 provoca recadastro; resposta truncada não confirma entrega. Erros permanentes e descartes geram diagnóstico.
- Heartbeat a cada segundo e captura de mudanças relevantes; fila RAM de 16 leituras mais uma pendente.
- UTC de captura estimado pelo horário do servidor e uptime monotônico, sem depender de NTP. Não é sincronização industrial de precisão.
- A fila é volátil e limitada por capacidade e idade. Descartes são contados; não existe retenção persistente para interrupções longas.
- O controle da mesa, pinos e temporizações foram preservados. Saídas transmitidas são comandos, sem confirmação mecânica.
- Medições ausentes continuam ausentes: `voltage_24v: null` e `analog_signals: {}`. O mapeamento atual não mede emergência.
- A dashboard preserva alertas conhecidos durante falhas. Falhas de histórico/utilização não devem apagar o estado atual.

## Repetir os testes

```powershell
.\tools\testarProjeto.ps1
.\tools\testarProjeto.ps1 -Firmware
```

`-Firmware` executa primeiro os testes C++ e a compilação Opta. Os JSON produzidos pelo serializador C++ real são enviados à API pelos testes. O runner não instala dependências automaticamente e grava logs e resumo em `.local/testes/`.

Para os cenários HTTP no servidor de simulação (timeout de 10 segundos):

```powershell
.\.venv\Scripts\python.exe tools/simuladorWifi.py --api http://127.0.0.1:8000/api --offline-timeout 10 --report .local/relatorio-wifi.json
```

Esse comando cria dados sintéticos. Os testes MySQL opcionais usam `ULTRON_TEST_MYSQL_URL`, somente localhost e banco com nome `ultron_test...`; não usam automaticamente o banco normal.

Resultados e limites: [testesWifiLocal.md](../reports/testesWifiLocal.md). Rádio no hotspot, polaridade elétrica, driver, RTOS e movimentos mecânicos continuam dependendo de bancada física.
