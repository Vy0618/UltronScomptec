# Verificação local do monitoramento CNC

Verificação de software em 29/10/2026, usando o contrato de eventos por máquina e seus estados.

O fluxo da aplicação é produtor → evento JSON com `machine_id` e `states` → API → MySQL → dashboard. A coleta física é um adaptador opcional. Os testes locais não executam uma CNC real.

| Verificação | Resultado |
|---|---|
| Aquisição e serializador C++ em host | Aprovados, incluindo as 256 combinações dos sinais |
| Compilação Opta em USB e HTTP | Aprovada nos dois modos, sem gravação da placa |
| Backend e ferramentas | 95 aprovados; três testes opcionais de MySQL ignorados |
| Frontend | 26 testes aprovados; build aprovado |
| API HTTP real com `curl` e SQLite isolado | Cadastro de máquina, POST mínimo, pipeline simulador/publicador e reenvios idempotentes aprovados sem coletores |

O build mantém o aviso de bundle acima de 500 kB; o lint termina sem erros, com avisos existentes no código.

## Aquisição e telemetria

Os testes C++ executam `cncMonitor.cpp` com GPIO e tempo simulados, verificando leitura das oito entradas, inicialização, entradas simultâneas, ausência de escrita de saídas, inversão de polaridade, filtro e rollover de tempo. O serializador é exercitado nas 256 combinações dos oito booleanos.

Também são verificados heartbeat, mudanças, filas limitadas, expiração, contador de descartes, identidade de boot, reenvios idempotentes, relógio de captura e parser HTTP do transporte alternativo. Os JSON reais gerados pelo C++ são usados nos testes da ponte e da API.

## Backend, ponte e interface

A rodada `backend/tests tools/tests` passou com 95 testes aprovados e três testes opcionais de MySQL ignorados, sem configuração de banco de teste MySQL. O banco dos testes de software é SQLite isolado. A suíte inclui serial Linux simulada por PTY, recepção do quadro C++, persistência dos oito sinais, histórico, falhas, recadastro, reconexão e recuperação.

Os 26 testes do frontend passaram, incluindo preservação de sinais e alertas durante indisponibilidade. O lint terminou sem erros, com avisos de código já existentes. O painel mostra os estados recebidos, sem pinos ou metadados de hardware, e identifica valores ausentes ou desatualizados. A dashboard não consulta endpoints de coletores.

Comandos para reproduzir estão no [README](../../README.md). O simulador opcional [simuladorCnc.py](../../tools/simuladorCnc.py) produz eventos JSON Lines sem rede; o publicador lê stdin e envia à API. Um POST por `curl` com ID da máquina e estados é suficiente, sem cadastro de dispositivo.

## Limites

Não houve gravação de firmware nem ensaio elétrico da IHM/CLP ou de máquina Mitsubishi M60, M70 ou M80. Os resultados não homologam polaridade, captura de pulsos, serial física, acesso remoto, garantia ou protocolo proprietário CNC. MySQL continua sendo o banco padrão da instalação; sua validação real depende de serviço/banco de teste disponível.

## Independência dos produtores

Os testes criam máquinas sem qualquer registro em `devices` e validam recepção, estados, histórico, utilização, timeout, ordem no mesmo segundo, idempotência por máquina e recuperação. Também verificam preservação de histórico antigo e novo ao remover ou realocar um coletor. Os testes do frontend rejeitam consultas indevidas de coletores e preservam estados adicionais de produtores desconhecidos.

O teste HTTP real iniciou uma API com SQLite isolado, cadastrou uma máquina e enviou eventos por `curl` e pelo pipeline `simuladorCnc.py | publicarEventos.py`. Foram conferidos estados, histórico, reenvios sem duplicação e ausência de coletores cadastrados. A definição da tabela nova foi compilada para o dialeto MySQL; os testes que dependem de um MySQL real continuam opcionais.
