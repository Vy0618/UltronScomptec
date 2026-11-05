# Análise das diferenças de frontend

Data da análise: 04/11/2026. Comparação estática dos arquivos locais; não foram executados navegador, build ou testes nesta subanálise. Os nomes abaixo identificam pastas, sem pressupor ordem cronológica.

## Pastas examinadas

Todos os caminhos têm como base `C:\Users\pedro\OneDrive\Desktop`:

| Identificação | Pasta de frontend |
|---|---|
| Atual | `UltronScomptec-main\frontend` |
| Aninhada | `UltronScomptec-main\UltronScomptec-main\frontend` |
| Cópia (1) | `UltronScomptec-main (1)\UltronScomptec-main\frontend` |
| HTTP | `SCOMPTECHTTP\scomptec-cnc front 2` |
| V3 | `SCOMPTECV3\scomptec-cnc front 2` |
| TCC | `ps3youtube\ScompTecTCC-main\scomptec-cnc front 2` |

Não foi encontrado AGENTS.md aplicável nos projetos; o único resultado na busca do Desktop estava dentro de uma dependência de terceiros em node_modules e não se aplica aos arquivos analisados.

## Quantidade de diferenças

O frontend atual possui 103 arquivos nesta contagem. Foram excluídos `node_modules`, `dist`, `release`, `.cache` e `.git`. Para distinguir renomeações de remoções, o pareamento aqui ignora maiúsculas, hífen, sublinhado e espaço nos caminhos; o inventário geral deve ser usado para os nomes exatos. Arquivo idêntico significa bytes idênticos. Formatação também conta como alteração de conteúdo.

| Outra pasta | Idênticos ao atual | Alterados | Somente no atual | Somente na outra |
|---|---:|---:|---:|---:|
| Aninhada | 83 | 15 | 5 | 0 |
| Cópia (1) | 45 | 39 | 19 | 2 |
| HTTP | 28 | 55 | 20 | 6 |
| V3 | 28 | 52 | 23 | 6 |
| TCC | 27 | 53 | 23 | 6 |

## Diferenças frente à cópia aninhada

A cópia que está dentro da pasta atual também possui código diferente. Ela já contém a estrutura de carregamento sob demanda, consultas coletivas e melhorias de responsividade descritas mais adiante. A diferença concentrada do atual é o perfil de sinais, seus diagnósticos, suas interpretações e a identificação da corrente.

1. **Perfil digital:** `src/services/cncSignals.js:1` troca a lista de oito sinais (`em_execucao`, `pausa`, `parada`, `emergencia`, `motor_ligado`, `automatico`, `manual`, `alarme`) por seis (`ativo`, `inativo`, `emergencia`, `motor_ligado`, `alarme`, `porta_aberta`). Os nomes extras recebidos continuam aparecendo pela função `observedStates`.
2. **Regra de atividade:** `src/services/cncSignals.js:10` introduz `machineActiveFromStates`. `inativo=true` impede atividade; a presença explícita de `ativo` governa o resultado; os aliases legados `em_execucao`, `ciclo`, `cycle` são fallback. Isso altera a interpretação do histórico em `src/services/telemetry.js:52`.
3. **Dados transportados para a UI:** `src/services/machineData.js:23` passa a expor `currentSource`, `diagnostics` e `signalOutputs` recebidos da API. Vale tanto para a consulta coletiva quanto para o carregador individual.
4. **Diagnósticos podem gerar notificações mesmo sem trocar o status:** `src/services/monitoring.js:55` compara os códigos dos diagnósticos entre leituras confirmadas. A primeira observação não gera aviso. Resultados de leitura antiga não criam diagnóstico novo. A lista de alertas também inclui máquinas com diagnóstico. Os avisos informativos de `signal_outputs` não viram automaticamente notificações de transição.
5. **Interpretações reutilizadas:** o novo `src/services/signalOutputs.js:17` remove duplicações por código, ordena Crítico/Atenção/Informativo, usa diagnósticos como fallback e marca saídas antigas quando a máquina está offline ou desatualizada.
6. **Novo painel de frota:** `src/components/signalOutputs/fleetSignalOutputs.jsx:12` apresenta “Interações entre sinais”, com filtro por máquina e nível, seis máquinas por página, duas interpretações por cartão e link para todas nos detalhes. A dashboard o inclui em `src/pages/dashboard/dashboard.jsx:363`.
7. **Sinais nos detalhes ficam antes dos demais painéis:** `src/pages/machineDetails/machineDetails.jsx:258`. O componente `src/components/cncSignals/cncSignals.jsx:26` inclui todas as interpretações; cada booleano diferencia ACIONADO, NÃO ACIONADO e NÃO INFORMADO.
8. **Corrente recebe origem explícita:** `src/components/cncSignals/cncSignals.jsx:64` informa I8 reservada, ausência de medição física, corrente simulada ou valor recebido de origem física não confirmada. `null` aparece como NÃO INFORMADO; `0` permanece `0 A`. Há indicação “Simulada” nos detalhes e no cartão e aviso no gráfico em `src/components/charts/telemetryChart.jsx:106`.
9. **Mais superfícies exibem interpretação:** cartões de máquina, cartões de alerta, cartões de ocorrência e modo TV incluem `SignalOutputSummary`; histórico em tabela mostra até dois títulos por leitura. `readingEvent` mantém `reading.signal_outputs` em `src/services/telemetry.js:79`, portanto a UI usa as interpretações daquela leitura histórica.
10. **Áudio de emergência:** `src/contexts/monitoringContext.jsx:241` exige aviso não resolvido antes de tocar o som de emergência.
11. **Testes presentes:** são acrescentados `cncSignals.test.js`, `signalOutputs.test.js` e casos em `monitoring.test.js`. Presença de teste não significa que ele foi executado nesta análise.

Lista completa dos arquivos diferentes frente à aninhada:

| Situação | Caminho dentro de frontend |
|---|---|
| Alterado | `src/contexts/monitoringContext.jsx` |
| Alterado | `src/services/cncSignals.js` |
| Alterado | `src/services/machineData.js` |
| Alterado | `src/services/monitoring.js` |
| Alterado | `src/services/monitoring.test.js` |
| Alterado | `src/services/telemetry.js` |
| Alterado | `src/pages/dashboard/dashboard.jsx` |
| Alterado | `src/pages/history/history.jsx` |
| Alterado | `src/pages/machineDetails/machineDetails.jsx` |
| Alterado | `src/pages/tvDashboard/tvDashboard.jsx` |
| Alterado | `src/components/alertCard/alertCard.jsx` |
| Alterado | `src/components/charts/telemetryChart.jsx` |
| Alterado | `src/components/cncSignals/cncSignals.jsx` |
| Alterado | `src/components/machineCard/machineCard.jsx` |
| Alterado | `src/components/occurrenceCard/occurrenceCard.jsx` |
| Exclusivo do atual | `src/services/cncSignals.test.js` |
| Exclusivo do atual | `src/services/signalOutputs.js` |
| Exclusivo do atual | `src/services/signalOutputs.test.js` |
| Exclusivo do atual | `src/components/signalOutputs/fleetSignalOutputs.jsx` |
| Exclusivo do atual | `src/components/signalOutputs/signalOutputList.jsx` |

## Diferenças adicionais frente a Cópia (1), HTTP, V3 e TCC

As mudanças desta seção já estão na aninhada; distinguem o atual das quatro outras pastas.

### Monitoramento e histórico

- `src/services/machineData.js:39` consulta `/cncs/statuses` para o monitoramento da frota em uma requisição. Cópia (1) e HTTP carregam `/cncs`, `/devices` e, para cada máquina, status, histórico e utilização; V3/TCC concentram esse fluxo em `api.js`, com `Promise.all` que pode rejeitar o conjunto por falha em consulta opcional. O atual consulta o histórico e a utilização apenas nos componentes que precisam desses dados.
- O campo de comunicação atual usa `status.online`, e os sinais usam `status.states`. HTTP/V3/TCC usam `gateway_online` e `digital_signals`. O monitoramento atual trabalha com a identidade da máquina sem enriquecer cada snapshot com MAC, IP, RSSI e versão do coletor.
- `src/hooks/useMachineResources.js:6` carrega até 100 leituras da máquina nos detalhes, a cada 10 segundos; utilização da frota é consultada em até quatro requisições simultâneas a cada 60 segundos (`:31`). O histórico global usa `/cncs/history`, página de 30 registros e um horário final de snapshot (`src/pages/history/history.jsx:13`), em vez de construir todo o histórico com os últimos 100 registros de cada máquina já presentes no contexto.
- O filtro de status do histórico é local à página recebida (`src/pages/history/history.jsx:53`); ele não é enviado como filtro global à API.
- `src/hooks/useApiQuery.js:4` introduz cache limitado a 60 consultas, reuso de resultados, cancelamento e mensagem de erro preservando dados recebidos.
- `src/services/telemetry.js:96` mantém o agendamento de cinco segundos após a conclusão, acrescenta bloqueio de execução simultânea, cancelamento com AbortController e pausa quando a aba fica oculta. O agendamento após conclusão já existia nas quatro outras pastas; não deve ser apresentado como recurso inteiramente novo.
- `src/contexts/monitoringContext.jsx:168` desabilita consultas de monitoramento em início, login, registro e recuperação de acesso. O contexto separa notificações/toasts em `ToastContext`; o atual limita os toasts a três (`:226`).
- `src/hooks/useRelativeDuration.js:4` troca temporizadores individuais por um relógio compartilhado, também pausado com a aba oculta. `liveTime.jsx` localiza as atualizações de duração e horário relativo.
- Em V3/TCC, uma falha do backend limpava os alertas (`MonitoringContext.jsx:186`). O atual preserva a lista conhecida, marcando os dados como antigos. Essa preservação e notificações de transição já estão em HTTP e Cópia (1).

### Telas, navegação e apresentação

- `src/app.jsx:1` usa `React.lazy` nas páginas e layouts. `routeBoundary.jsx` trata carregamento e falha da página, com tentar novamente e voltar ao painel. A raiz redireciona para `/inicio`, em vez da tela Splash (o arquivo de Splash permanece no projeto).
- `/recuperar-senha` agora possui página própria; explica que a redefinição deve ser solicitada ao administrador. **Não implementa envio de e-mail ou recuperação automática.** Nas quatro outras pastas o login já possui o link, mas não existe rota correspondente.
- Login substitui PNG por duas imagens WebP, com versão para celular, `decoding="async"`, labels associados aos campos, autocomplete e nome acessível do botão de senha (`src/pages/login/login.jsx:31`).
- A lista de máquinas tem paginação de 24 itens e pesquisa ligada ao parâmetro `busca`. O dashboard limita a lista resumida a oito máquinas e os eventos recentes a nove; há link para a visão completa.
- `deferredHealth.jsx` carrega o gráfico ao se aproximar da região visível ou por ação do usuário. `fleetHealth.jsx` conecta o gráfico à consulta de utilização da frota.
- Cabeçalho foi refeito com busca funcional (Ctrl/Cmd+K), indicadores de conexão, painel de notificações, marcação de leitura, menu real da conta, logout, Escape e fechamento ao clicar fora (`header.jsx:20`). A marcação de leitura fica no estado da sessão do componente.
- O menu lateral controla foco, Escape e rolagem para uso móvel. O conteúdo atrás recebe `inert` quando o menu está aberto (`dashboardLayout.jsx:27`). CSS ajusta toques para 44 px, formulários para 16 px e respeita redução de movimento (`index.css:249`).
- O modo TV e seus cartões passam a usar a duração compartilhada; tratamentos de status sem conexão, carregamento e dados parciais são explícitos. As interpretações no TV são exclusivas do atual frente a todas as outras pastas analisadas.
- A UI deixa de mostrar o painel específico da mesa seletora: não exibe os contadores, altura, metal, ocupação das rampas nem comandos O1/O2/O3 de `MesaSignals`. No atual, o componente foi substituído pelo monitoramento genérico CNC. Isso representa mudança de finalidade, com funcionalidades específicas da mesa ausentes da interface atual.
- A página de dispositivos passa a “Coletores opcionais”, buscando diretamente `/devices`, com nome, ID e máquina; substitui a tabela de gateways com RSSI, firmware e métricas online/instável/offline. Ela não possui polling recorrente.
- Clientes/unidades têm mensagens de indisponibilidade quando não há estrutura cadastrada. A seleção de empresa usa textos condizentes com conexão e com a instalação direta por máquinas, em lugar do selo fixo “100% ONLINE” presente em HTTP/V3/TCC.

### Temas e administração

- O tema claro padrão e o seletor claro/escuro distinguem o atual de HTTP/V3/TCC, mas já existem em Cópia (1) e aninhada. `preferences.js` passa a validar `theme` e traduz `offwhite` para `light`; `dashboardLayout.jsx:17` aplica as variáveis do tema.
- O núcleo da administração **não é uma novidade do atual**: consultas, criação/edição/exclusão de usuários, ocorrências, limites, auditoria e exportação já estão nas pastas HTTP, V3 e TCC. Os arquivos principais de administração do atual só diferem dessas versões pelos caminhos/imports com capitalização padronizada; frente a Cópia (1) e aninhada estão idênticos.
- Os nomes de páginas/componentes foram padronizados de PascalCase para camelCase frente a HTTP/V3/TCC; vários arquivos classificados como alterados têm apenas import e formatação modificados. Essas mudanças de nomes não representam funcionalidades novas.

### Web, Electron e ferramentas

- `vite.config.js:7` usa `base: '/'` na web e `'./'` no modo Electron, em vez de `'./'` em todos os builds. O proxy `/api` para `127.0.0.1:8000` e o `.env.example` com `/api` permitem acesso web pela mesma origem.
- `src/services/apiConfig.js:1` resolve API relativa na web e endereço absoluto em `file:`/`scomptec:`. O package.json introduz `build:electron`, e `electron:build` passa a executar esse modo antes de empacotar. Isso difere de Cópia (1), HTTP, V3 e TCC; já está na aninhada.
- `api.js:56` agrega timeout de 10 segundos com cancelamento solicitado pelo componente; apenas envia Content-Type quando existe body e mantém o status HTTP no erro.
- O protocolo local seguro `scomptec://app` no Electron, com validação do caminho de arquivo e de navegação, é diferente de TCC, que usa `loadFile` e checagem textual de prefixo. O arquivo principal Electron já é idêntico em HTTP, V3, Cópia (1), aninhada e atual; não atribuir essa mudança ao atual frente a essas quatro pastas.
- `electron/main.js` da pasta antiga foi guardado como `electron/legacy/main.js`; `main.cjs` é o entrypoint. Os README/ADMINISTRACAO/.gitignore que estavam dentro do frontend de HTTP/V3/TCC não existem nesse mesmo lugar no atual; a documentação foi reorganizada fora da pasta de frontend.

## Dependências e testes

Os intervalos de versões de todas as dependências diretas e devDependencies declarados em package.json são iguais nas seis pastas, incluindo React `^19.2.8`, Router `^7.18.2`, Vite `^8.2.0` e Electron `^43.4.1`. Não houve troca de React nem de biblioteca de gráficos declarada. Os scripts e a formatação do package.json diferem.

O package-lock atual é idêntico ao da aninhada e ao da Cópia (1). Frente a HTTP/V3/TCC há 56 entradas de pacote diferentes, incluindo adições e remoções de pacotes internos. Exemplos das resoluções fixadas:

| Pacote | HTTP/V3/TCC | Atual |
|---|---|---|
| vite | 8.2.1 | 8.3.5 |
| electron | 43.4.1 | 43.8.3 |
| electron-builder | 26.15.3 | 26.18.0 |
| rolldown | 1.2.4 | 1.2.15 |
| postcss | 8.5.26 | 8.5.31 |
| concurrently | 10.0.5 | 10.0.6 |
| axios (transitiva) | 1.19.0 | 1.20.0 |
| undici (transitiva) | 7.29.0 | 7.30.1 |

Essas são versões do lockfile, não prova de quais versões estão instaladas ou de segurança corrigida.

| Pasta | Arquivos *.test.js em src | Script npm test |
|---|---:|---|
| Atual | 7 | Presente |
| Aninhada | 5 | Presente |
| Cópia (1) | 4 | Presente |
| HTTP | 4 | Presente |
| V3 | 3 | Ausente |
| TCC | 3 | Ausente |

Os dois testes exclusivos do atual frente à aninhada são sinais CNC e saídas interpretadas. A presença e o conteúdo dos testes foram inspecionados; esta análise não afirma aprovação da suíte, desempenho medido, funcionamento no Electron ou aparência visual validada.
