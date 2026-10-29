# Como produtores, API e dashboard se comunicam

A dashboard acompanha eventos de máquinas. Ela não precisa conhecer o equipamento, o protocolo ou o programa que os produziu.

```text
curl / arquivo / simulador / adaptador físico
  → JSON {machine_id, states}
  → API de eventos
  → MySQL
  → Dashboard
```

O ID identifica uma máquina cadastrada. `states` é um mapa de nomes e booleanos. Um evento representa o snapshot completo observado naquele instante. Campos ausentes permanecem não informados, em vez de serem interpretados como inativos.

A API recebe `POST /api/events`, valida os campos e guarda os eventos por máquina. A dashboard consulta estados, horários, histórico e utilização, sem chamar endpoints de coletores. Cadastros de Opta, MAC, firmware, porta serial e IHM/CLP ficam fora desse contrato.

## Programas que podem ser compostos

O simulador escreve JSON Lines em stdout, sem rede. O publicador lê stdin e faz os POSTs. Diagnósticos são escritos em stderr. É possível salvar eventos, inspecioná-los e publicá-los depois:

```bash
.venv/bin/python tools/simuladorCnc.py --machine-id CNC-001 --count 1 > .local/eventos.jsonl
.venv/bin/python tools/publicarEventos.py < .local/eventos.jsonl
```

Cadastre a máquina antes e use o código ou UUID retornado. Um POST de `curl` com o mesmo JSON funciona sem esses programas. A ponte serial também pode produzir o mesmo formato em stdout usando `--machine-id` e `--stdout`.

## Persistência

MySQL é o banco padrão da instalação. A tabela `machine_events` pertence às máquinas, não aos coletores. Remover ou trocar um coletor não apaga nem transfere os eventos. A compatibilidade com leituras antigas fica isolada no repositório de eventos.

`event_id` permite reenvio idempotente. `timestamp` registra a observação; `received_at` registra a recepção. Sem timestamp, a API usa o horário atual. Leituras antigas não substituem observações mais recentes, e reenvios idênticos não mantêm uma máquina online.

## Dashboard

A aplicação apresenta os estados recebidos e diferencia ausência de informação, falta de novos eventos e observações antigas. Durante falhas da API, preserva as últimas informações conhecidas com indicação de desatualização. O resumo operacional reconhece execução, emergência e alarme; pausa e modos continuam como estados booleanos independentes.

## Integração física opcional

Uma das fontes possíveis é computador/máquina → IHM/CLP → Arduino Opta → serial → adaptador. O contexto industrial inclui CNC Mitsubishi M60, M70 e M80. A ligação pouco invasiva e a autorização das interfaces devem ser validadas para cada instalação. O contrato de eventos não depende desse fabricante nem implementa seu protocolo proprietário.

Configuração, testes com `curl`, pipelines e execução local estão no [README](../../README.md).
