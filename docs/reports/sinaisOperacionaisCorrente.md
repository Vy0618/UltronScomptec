# Relatório — sinais operacionais e reserva para corrente

Data: 03/11/2026.

## Mudanças realizadas

O firmware, a API, o simulador e a dashboard passaram a acompanhar seis sinais: `ativo`, `inativo`, `emergencia`, `motor_ligado`, `alarme` e `porta_aberta`. O mapeamento adotado usa I1/A0 até I6/A5 nessa ordem; I7/A6 permanece livre e I8/A7 fica reservada para corrente. O firmware foi atualizado para a versão 2.1.0, perfil `six_signals_current_reserved_v2`.

Emergência e alarme mantêm prioridade sobre atividade. Inativo representa parada, sem significar desligamento. Ativo e inativo são independentes: a ausência de um não permite deduzir seu complemento. A aplicação preserva os sinais recebidos e a compatibilidade com nomes antigos de execução.

Foram incluídos dois diagnósticos, calculados com os sinais da mesma leitura:

- **Operação falha:** porta aberta e emergência acionadas simultaneamente, mantendo o estado de emergência.
- **Sinais de atividade conflitantes:** ativo e inativo acionados simultaneamente, mantendo parada quando não houver emergência ou alarme.

Os diagnósticos aparecem nos cartões, alertas e no painel de sinais, agora no início dos detalhes da máquina. Uma combinação nova gera notificação mesmo sem mudança do estado resumido. Falhas de comunicação preservam as últimas informações, identificadas como antigas.

## Resultado das interações entre sinais

Os exemplos abaixo consideram sinais da mesma leitura, comunicação atual e snapshots completos: os sinais não citados estão explicitamente em `false`. Não há indicação adicional de manutenção ou ausência de 24 V. Um campo ausente em uma leitura real continua **não informado**, sem ser convertido automaticamente em `false`.

| Sinais acionados / condição | Estado resultante | Diagnóstico ou interpretação | Saída visível na dashboard |
|---|---|---|---|
| `ativo` | `OPERANDO` | Atividade informada, sem diagnóstico de combinação. | Atividade informada |
| `inativo` | `PARADA` | Inatividade informada; não significa máquina desligada. | Inatividade informada |
| `ativo` + `inativo` | `PARADA` | **Sinais de atividade conflitantes**; ambos os valores são preservados. | Sinais de atividade conflitantes |
| Todos os seis sinais em `false` | `PARADA` | Estado padrão da classificação; não é fabricado um sinal `inativo=true`. | Nenhum sinal acionado |
| `motor_ligado` | `PARADA` | Motor ligado isoladamente não comprova atividade da máquina. | Motor ligado sem atividade confirmada |
| `ativo` + `motor_ligado` | `OPERANDO` | A atividade determina o estado; motor ligado é preservado como sinal independente. | Atividade com motor ligado |
| `inativo` + `motor_ligado` | `PARADA` | Inativo impede classificar como operando; não existe diagnóstico específico para essa combinação. | Inatividade com motor ligado |
| `porta_aberta` | `PARADA` | Porta aberta, sem diagnóstico específico de falha. | Porta aberta |
| `ativo` + `porta_aberta` | `OPERANDO` | A combinação é exibida, mas não possui regra própria de falha implementada. | Atividade com porta aberta |
| `inativo` + `porta_aberta` | `PARADA` | Sem diagnóstico específico de combinação. | Inatividade com porta aberta |
| `emergencia` | `EMERGENCIA` | Emergência tem prioridade sobre atividade; sem porta aberta, não gera o diagnóstico “Operação falha”. | Emergência acionada |
| `ativo` + `emergencia` | `EMERGENCIA` | A emergência prevalece sobre o sinal de atividade. | Emergência com atividade informada |
| `porta_aberta` + `emergencia` | `EMERGENCIA` | **Operação falha**; o estado de emergência é mantido. | Operação falha |
| `ativo` + `porta_aberta` + `emergencia` | `EMERGENCIA` | **Operação falha**, mesmo com atividade informada. | Operação falha; emergência com atividade informada |
| `ativo` + `alarme` | `ALARME` | O alarme prevalece sobre a atividade. | Atividade com alarme |
| `inativo` + `alarme` | `ALARME` | O alarme prevalece sobre a parada. | Inatividade com alarme |
| `porta_aberta` + `alarme` | `ALARME` | Sem emergência, não gera o diagnóstico “Operação falha”. | Porta aberta com alarme |
| `alarme` + `emergencia` | `EMERGENCIA` | A emergência prevalece sobre o alarme; os dois sinais permanecem registrados. | Emergência e alarme simultâneos |
| `ativo` + `inativo` + `alarme` | `ALARME` | **Sinais de atividade conflitantes**; o alarme determina o estado resumido. | Sinais de atividade conflitantes; atividade com alarme |
| Todos os seis sinais em `true` | `EMERGENCIA` | Os dois diagnósticos são apresentados: **Operação falha** e **Sinais de atividade conflitantes**. | Operação falha e demais interpretações aplicáveis |
| `ativo` + corrente simulada de `12.5 A` | `OPERANDO` | A corrente aparece como simulada; seu valor não modifica o estado operacional. | Atividade informada; corrente com atividade informada |
| `inativo` + corrente simulada de `12.5 A` | `PARADA` | Corrente recebida não substitui o sinal de inatividade nem gera diagnóstico específico de combinação. | Inatividade informada; corrente com inatividade informada |

Os únicos diagnósticos de combinação implementados são os dois descritos acima. Perda de comunicação e leitura antiga podem substituir o estado exibido por `SEM_COMUNICACAO` ou `DADOS_DESATUALIZADOS`; nesse caso, os sinais e diagnósticos apresentados pertencem à última leitura conhecida.

## Outputs na dashboard

As 22 situações da tabela agora possuem saídas interpretadas em `signal_outputs`, retornadas pelas consultas individuais/coletivas de status e pelo histórico. Cada saída contém `code`, `level`, `title`, `message` e `signals`. Há níveis **Informativo**, **Atenção** e **Crítico**. Combinações adicionais verdadeiras na mesma leitura podem produzir outras saídas além dos exemplos da tabela; uma mesma saída não é duplicada.

O painel **Interações entre sinais** permite filtrar por máquina e nível, mostra seis máquinas por página e resume duas saídas por cartão. Os detalhes exibem todas. Cartões de máquinas, alertas existentes, histórico e modo TV também apresentam interpretações. Mudanças nos sinais atualizam os resultados mesmo quando o status continua igual. As interpretações informativas não criam uma notificação a cada polling; as notificações existentes continuam ligadas ao estado e aos dois diagnósticos de falha/conflito.

Leituras incompletas mostram quais sinais não foram informados, sem deduzir false. Falha de comunicação mantém as últimas interpretações, com indicação de leitura antiga e apresentação sem destaque de alerta atual. O histórico interpreta cada snapshot armazenado; não usa os sinais atuais para explicar eventos passados. Não houve migração de banco nem alteração de saídas físicas.

## Corrente e simulação

I8 fica configurada como entrada, mas não é consultada digitalmente ou por ADC. Sem sensor, a corrente permanece **não informada**, em vez de receber um zero fictício. As saídas de relé não foram alteradas.

A API aceita medições opcionais em `analog_signals` e metadados em `extra_signals`. Corrente exige número finito e não negativo em A; zero é válido. A ponte USB preserva esses dados. `--current 12.5` no simulador envia corrente marcada como simulada; `--also emergencia` permite combinar sinais. Os valores seguem para estado, histórico e gráfico, com indicação de simulação na interface. Uma nova leitura sem corrente não reutiliza o valor anterior.

O README, os exemplos, os guias de integração e o contexto local para agentes foram atualizados. Não foi necessária migração do banco.

## Validação e limites

- 129 testes Python aprovados; três testes de concorrência MySQL ignorados por falta de banco de teste configurado.
- 34 testes frontend aprovados; lint e build web concluídos.
- Testes C++ de aquisição e telemetria aprovados, incluindo as 256 combinações de entradas e a reserva de I7/I8.
- Firmwares USB e Wi-Fi compilados para Arduino Opta, sem upload.
- 70 verificações gerais de navegador aprovadas, incluindo falha/recuperação da API e resoluções de 320 a 1920 px.
- Mais 21 cenários finais dos detalhes da máquina aprovados: sete larguras de tela, diagnóstico de operação falha e corrente simulada, zero ou ausente.
- Pipeline real simulador → publicador HTTP → API → SQLite validado com corrente simulada, zero e valor ausente.

O `Main.pdf` descreve o ladder anterior de oito sinais e não inclui porta aberta. A correspondência física entre o CLP e o novo mapeamento precisa ser ajustada antes do ensaio em bancada. Não houve medição elétrica, gravação na placa ou validação em MySQL real.

Validação adicional dos outputs: 156 testes Python e 37 testes frontend aprovados; três testes MySQL ignorados. Os testes cobrem os 22 cenários da tabela e as 64 combinações booleanas dos seis sinais, preservação de dados, campos ausentes e corrente zero. Passaram 70 verificações gerais de navegador e 44 combinações de cenário/tela (22 casos em 320 e 1366 px) com FastAPI/SQLite reais, incluindo filtros, paginação, atualização sem troca de estado e falha/recuperação da API.

Oito telas complementares foram verificadas em 320/1366 px: alertas, histórico compacto, modo TV e detalhes. O README passou a apresentar primeiro o setup local, com inicialização em três terminais e 12 exemplos de injeção/consulta, seguido do teste integrado com CLP/Opta. A função Bash e os 12 comandos de injeção foram executados contra API/SQLite isolados; os exemplos PowerShell foram revisados, sem execução em Windows.
## Revisão de regressões em 04/11/2026

A revisão incluiu as mudanças de aquisição, ponte USB, ingestão, classificação, consultas e apresentação. Foi corrigida uma divergência na interpretação de aliases: `emergency=true` ou `alarm=true` agora permanecem visíveis nos outputs mesmo quando o nome em português chega como `false`, seguindo a prioridade já usada no status. Três testes de regressão verificam esses casos, sem alterar os sinais armazenados.

Após a correção, passaram 159 testes Python (três testes exclusivos de MySQL ignorados), 37 testes frontend, lint, build web, testes C++ de aquisição/telemetria e 70 verificações de rota/tela no Chromium, incluindo perda e recuperação da API. Capturas e resultado desta revisão ficam em `.local/testes/revisao-final/`.

As mudanças incluem novas regras e um novo mapeamento físico, além de nomes: emergência passou de I4 para I3 e alarme de I8 para I5; I6 passou a representar porta aberta. O ladder/cabeamento precisam corresponder ao perfil antes do uso integrado. O firmware continua sem escrita em relés, e I8 permanece sem aquisição física. Não houve upload ou ensaio elétrico nesta revisão. A recompilação da placa nesta instalação ficou bloqueada pela ausência do executável ARM `arm-none-eabi-g++`; os testes C++ de host passaram. Os builds de placa registrados anteriormente não substituem essa validação nem o teste com hardware real.

