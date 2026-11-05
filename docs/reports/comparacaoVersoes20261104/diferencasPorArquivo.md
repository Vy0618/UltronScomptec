# Inventário completo das diferenças por arquivo

Comparação em 04/11/2026. A direção é **outra cópia → pasta atual**. Nenhuma cópia foi alterada.

Os caminhos abaixo são relativos às origens listadas no relatório principal e no JSON. `+` e `−` são linhas textuais adicionadas/removidas após normalizar somente BOM UTF-8 e quebras de linha. Arquivos binários são comparados por SHA-256. Configurações locais são identificadas sem reproduzir seus valores.

**Estados:** `alterado` = conteúdo diferente; `realocado_identico` = bytes iguais em caminho diferente; `somente_bom_ou_quebras_de_linha` = diferença de codificação/quebra de linha; `somente_na_atual` / `somente_na_outra` = sem correspondência encontrada. Correspondências por nome/estrutura não afirmam uma renomeação histórica. Arquivos idênticos no mesmo caminho foram omitidos desta listagem, mas constam no JSON.

## ANINHADA — UltronScomptec-main dentro da pasta atual

Origem: `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main\UltronScomptec-main`

Contagens: `{"identico": 148, "alterado": 39, "somente_na_atual": 11}`

| Estado | Caminho na outra cópia | Caminho na atual | + linhas | − linhas |
|---|---|---|---:|---:|
| alterado | `backend/schemas/cnc.py` | `backend/schemas/cnc.py` | 11 | 0 |
| alterado | `backend/schemas/event.py` | `backend/schemas/event.py` | 13 | 1 |
| somente_na_atual | — | `backend/schemas/signalOutput.py` | 10 | — |
| alterado | `backend/schemas/telemetry.py` | `backend/schemas/telemetry.py` | 3 | 1 |
| alterado | `backend/services/cncService.py` | `backend/services/cncService.py` | 6 | 0 |
| alterado | `backend/services/events.py` | `backend/services/events.py` | 3 | 2 |
| alterado | `backend/services/machineState.py` | `backend/services/machineState.py` | 32 | 1 |
| somente_na_atual | — | `backend/services/signalOutputs.py` | 82 | — |
| alterado | `backend/tests/testEvents.py` | `backend/tests/testEvents.py` | 92 | 0 |
| somente_na_atual | — | `backend/tests/testSignalOutputs.py` | 105 | — |
| alterado | `docs/guides/explicacaoBackendFrontend.md` | `docs/guides/explicacaoBackendFrontend.md` | 1 | 1 |
| alterado | `docs/guides/guiaEquipe.md` | `docs/guides/guiaEquipe.md` | 10 | 2 |
| alterado | `docs/guides/integracaoOpta.md` | `docs/guides/integracaoOpta.md` | 14 | 10 |
| somente_na_atual | — | `docs/reports/sinaisOperacionaisCorrente.md` | 87 | — |
| alterado | `examples/machine-event.json` | `examples/machine-event.json` | 4 | 6 |
| alterado | `firmware/optaCncMonitor/cncMonitor.cpp` | `firmware/optaCncMonitor/cncMonitor.cpp` | 4 | 3 |
| alterado | `firmware/optaCncMonitor/config.h` | `firmware/optaCncMonitor/config.h` | 5 | 5 |
| alterado | `firmware/optaCncMonitor/monitorSample.json` | `firmware/optaCncMonitor/monitorSample.json` | 14 | 21 |
| somente_na_atual | — | `firmware/optaCncMonitor/signalProfile.h` | 15 | — |
| alterado | `firmware/optaCncMonitor/telemetryModel.h` | `firmware/optaCncMonitor/telemetryModel.h` | 1 | 1 |
| alterado | `firmware/optaCncMonitor/telemetryPayload.h` | `firmware/optaCncMonitor/telemetryPayload.h` | 12 | 9 |
| alterado | `firmware/tests/host/testControl.cpp` | `firmware/tests/host/testControl.cpp` | 8 | 5 |
| alterado | `firmware/tests/host/testTelemetry.cpp` | `firmware/tests/host/testTelemetry.cpp` | 12 | 11 |
| alterado | `frontend/src/components/alertCard/alertCard.jsx` | `frontend/src/components/alertCard/alertCard.jsx` | 10 | 0 |
| alterado | `frontend/src/components/charts/telemetryChart.jsx` | `frontend/src/components/charts/telemetryChart.jsx` | 7 | 1 |
| alterado | `frontend/src/components/cncSignals/cncSignals.jsx` | `frontend/src/components/cncSignals/cncSignals.jsx` | 74 | 22 |
| alterado | `frontend/src/components/machineCard/machineCard.jsx` | `frontend/src/components/machineCard/machineCard.jsx` | 6 | 0 |
| alterado | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | 4 | 0 |
| somente_na_atual | — | `frontend/src/components/signalOutputs/fleetSignalOutputs.jsx` | 146 | — |
| somente_na_atual | — | `frontend/src/components/signalOutputs/signalOutputList.jsx` | 56 | — |
| alterado | `frontend/src/contexts/monitoringContext.jsx` | `frontend/src/contexts/monitoringContext.jsx` | 3 | 1 |
| alterado | `frontend/src/pages/dashboard/dashboard.jsx` | `frontend/src/pages/dashboard/dashboard.jsx` | 7 | 0 |
| alterado | `frontend/src/pages/history/history.jsx` | `frontend/src/pages/history/history.jsx` | 6 | 0 |
| alterado | `frontend/src/pages/machineDetails/machineDetails.jsx` | `frontend/src/pages/machineDetails/machineDetails.jsx` | 5 | 3 |
| alterado | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | 2 | 0 |
| alterado | `frontend/src/services/cncSignals.js` | `frontend/src/services/cncSignals.js` | 22 | 8 |
| somente_na_atual | — | `frontend/src/services/cncSignals.test.js` | 47 | — |
| alterado | `frontend/src/services/machineData.js` | `frontend/src/services/machineData.js` | 6 | 0 |
| alterado | `frontend/src/services/monitoring.js` | `frontend/src/services/monitoring.js` | 115 | 25 |
| alterado | `frontend/src/services/monitoring.test.js` | `frontend/src/services/monitoring.test.js` | 108 | 0 |
| somente_na_atual | — | `frontend/src/services/signalOutputs.js` | 61 | — |
| somente_na_atual | — | `frontend/src/services/signalOutputs.test.js` | 100 | — |
| alterado | `frontend/src/services/telemetry.js` | `frontend/src/services/telemetry.js` | 4 | 6 |
| somente_na_atual | — | `Main.pdf` | — | — |
| alterado | `README.md` | `README.md` | 277 | 147 |
| alterado | `tools/ponteUsb.py` | `tools/ponteUsb.py` | 6 | 0 |
| alterado | `tools/simuladorCnc.py` | `tools/simuladorCnc.py` | 16 | 6 |
| alterado | `tools/testarFrontend.py` | `tools/testarFrontend.py` | 24 | 2 |
| alterado | `tools/tests/testEventTools.py` | `tools/tests/testEventTools.py` | 30 | 3 |
| alterado | `tools/tests/testPonteUsb.py` | `tools/tests/testPonteUsb.py` | 19 | 5 |

## ULTRON_1 — UltronScomptec-main (1)

Origem: `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main (1)\UltronScomptec-main`

Contagens: `{"alterado": 85, "identico": 71, "somente_na_atual": 41, "somente_na_outra": 6, "realocado_identico": 1}`

| Estado | Caminho na outra cópia | Caminho na atual | + linhas | − linhas |
|---|---|---|---:|---:|
| alterado | `.gitignore` | `.gitignore` | 4 | 0 |
| alterado | `backend/.env.example` | `backend/.env.example` | 7 | 0 |
| alterado | `backend/config.example.json` | `backend/config.example.json` | 3 | 1 |
| alterado | `backend/config.py` | `backend/config.py` | 1 | 1 |
| alterado | `backend/database/models.py` | `backend/database/models.py` | 34 | 1 |
| alterado | `backend/main.py` | `backend/main.py` | 2 | 1 |
| alterado | `backend/schemas/cnc.py` | `backend/schemas/cnc.py` | 15 | 1 |
| somente_na_atual | — | `backend/schemas/event.py` | 33 | — |
| somente_na_atual | — | `backend/schemas/observation.py` | 19 | — |
| somente_na_atual | — | `backend/schemas/signalOutput.py` | 10 | — |
| alterado | `backend/schemas/telemetry.py` | `backend/schemas/telemetry.py` | 7 | 14 |
| alterado | `backend/services/clock.py` | `backend/services/clock.py` | 4 | 4 |
| alterado | `backend/services/cncService.py` | `backend/services/cncService.py` | 60 | 21 |
| somente_na_atual | — | `backend/services/codeService.py` | 29 | — |
| alterado | `backend/services/deviceAuth.py` | `backend/services/deviceAuth.py` | 2 | 10 |
| alterado | `backend/services/deviceService.py` | `backend/services/deviceService.py` | 7 | 27 |
| somente_na_atual | — | `backend/services/eventRepository.py` | 103 | — |
| somente_na_atual | — | `backend/services/events.py` | 88 | — |
| somente_na_atual | — | `backend/services/ingestAuth.py` | 11 | — |
| somente_na_atual | — | `backend/services/machineState.py` | 48 | — |
| somente_na_atual | — | `backend/services/signalOutputs.py` | 82 | — |
| alterado | `backend/services/telemetry.py` | `backend/services/telemetry.py` | 13 | 56 |
| alterado | `backend/services/utilization.py` | `backend/services/utilization.py` | 3 | 3 |
| somente_na_atual | — | `backend/tests/testEvents.py` | 332 | — |
| alterado | `backend/tests/testMysqlConcurrency.py` | `backend/tests/testMysqlConcurrency.py` | 2 | 2 |
| alterado | `backend/tests/testOptaApi.py` | `backend/tests/testOptaApi.py` | 17 | 14 |
| somente_na_atual | — | `backend/tests/testSignalOutputs.py` | 105 | — |
| somente_na_outra | `backend/tests/testWifiFlow.py` | — | — | 171 |
| somente_na_atual | — | `configuracao.json` | 552 | — |
| alterado | `docs/guides/administracao.md` | `docs/guides/administracao.md` | 1 | 1 |
| alterado | `docs/guides/explicacaoBackendFrontend.md` | `docs/guides/explicacaoBackendFrontend.md` | 26 | 638 |
| alterado | `docs/guides/guiaEquipe.md` | `docs/guides/guiaEquipe.md` | 54 | 443 |
| alterado | `docs/guides/integracaoOpta.md` | `docs/guides/integracaoOpta.md` | 48 | 79 |
| somente_na_atual | — | `docs/guides/testesResponsividade.md` | 49 | — |
| alterado | `docs/reports/administracaoFrontendLegada.md` | `docs/reports/administracaoFrontendLegada.md` | 1 | 1 |
| somente_na_outra | `docs/reports/relatorioCompletoOpta.txt` | — | — | 739 |
| somente_na_atual | — | `docs/reports/sinaisOperacionaisCorrente.md` | 87 | — |
| somente_na_atual | — | `docs/reports/testesCncLocal.md` | 39 | — |
| somente_na_outra | `docs/reports/testesWifiLocal.md` | — | — | 72 |
| somente_na_atual | — | `examples/machine-event.json` | 11 | — |
| alterado | `firmware/archives/optaMesaMonitor.zip` | `firmware/archives/optaCncMonitor.zip` | — | — |
| alterado | `firmware/optaMesaMonitor/mesaControl.cpp` | `firmware/optaCncMonitor/cncMonitor.cpp` | 39 | 478 |
| alterado | `firmware/optaMesaMonitor/mesaControl.h` | `firmware/optaCncMonitor/cncMonitor.h` | 2 | 2 |
| alterado | `firmware/optaMesaMonitor/config.h` | `firmware/optaCncMonitor/config.h` | 32 | 21 |
| realocado_identico | `firmware/optaMesaMonitor/httpResponse.h` | `firmware/optaCncMonitor/httpResponse.h` | — | — |
| somente_na_atual | — | `firmware/optaCncMonitor/inputMonitor.h` | 29 | — |
| alterado | `firmware/optaMesaMonitor/mesaSample.json` | `firmware/optaCncMonitor/monitorSample.json` | 23 | 24 |
| somente_na_atual | — | `firmware/optaCncMonitor/optaCncMonitor.ino` | 10 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/signalProfile.h` | 15 | — |
| alterado | `firmware/optaMesaMonitor/telemetry.cpp` | `firmware/optaCncMonitor/telemetry.cpp` | 7 | 71 |
| alterado | `firmware/optaMesaMonitor/telemetry.h` | `firmware/optaCncMonitor/telemetry.h` | 1 | 3 |
| alterado | `firmware/optaMesaMonitor/telemetryCore.h` | `firmware/optaCncMonitor/telemetryCore.h` | 4 | 8 |
| alterado | `firmware/optaMesaMonitor/telemetryModel.h` | `firmware/optaCncMonitor/telemetryModel.h` | 3 | 15 |
| alterado | `firmware/optaMesaMonitor/telemetryPayload.h` | `firmware/optaCncMonitor/telemetryPayload.h` | 18 | 33 |
| somente_na_outra | `firmware/optaMesaMonitor/optaMesaMonitor.ino` | — | — | 12 |
| somente_na_outra | `firmware/reference/mesaOptaV2Original.ino` | — | — | 416 |
| alterado | `firmware/testarFirmware.ps1` | `firmware/testarFirmware.ps1` | 2 | 2 |
| alterado | `firmware/tests/host/Arduino.h` | `firmware/tests/host/Arduino.h` | 5 | 2 |
| alterado | `firmware/tests/host/testControl.cpp` | `firmware/tests/host/testControl.cpp` | 52 | 61 |
| alterado | `firmware/tests/host/testTelemetry.cpp` | `firmware/tests/host/testTelemetry.cpp` | 56 | 19 |
| alterado | `frontend/.env.example` | `frontend/.env.example` | 4 | 2 |
| alterado | `frontend/.oxlintrc.json` | `frontend/.oxlintrc.json` | 11 | 2 |
| alterado | `frontend/package.json` | `frontend/package.json` | 2 | 11 |
| alterado | `frontend/public/loginCncBackground.png` | `frontend/public/loginCncBackground.webp` | — | — |
| somente_na_atual | — | `frontend/public/loginCncBackgroundMobile.webp` | — | — |
| alterado | `frontend/src/app.jsx` | `frontend/src/app.jsx` | 63 | 45 |
| alterado | `frontend/src/components/alertCard/alertCard.jsx` | `frontend/src/components/alertCard/alertCard.jsx` | 33 | 12 |
| somente_na_atual | — | `frontend/src/components/charts/deferredHealth.jsx` | 51 | — |
| somente_na_atual | — | `frontend/src/components/charts/fleetHealth.jsx` | 15 | — |
| alterado | `frontend/src/components/charts/telemetryChart.jsx` | `frontend/src/components/charts/telemetryChart.jsx` | 173 | 40 |
| alterado | `frontend/src/components/clientCard/clientCard.jsx` | `frontend/src/components/clientCard/clientCard.jsx` | 35 | 15 |
| alterado | `frontend/src/components/mesaSignals/mesaSignals.jsx` | `frontend/src/components/cncSignals/cncSignals.jsx` | 72 | 61 |
| alterado | `frontend/src/components/contextSwitcher/contextSwitcher.jsx` | `frontend/src/components/contextSwitcher/contextSwitcher.jsx` | 90 | 78 |
| alterado | `frontend/src/components/header/header.jsx` | `frontend/src/components/header/header.jsx` | 286 | 176 |
| somente_na_atual | — | `frontend/src/components/liveTime/liveTime.jsx` | 12 | — |
| alterado | `frontend/src/components/machineCard/machineCard.jsx` | `frontend/src/components/machineCard/machineCard.jsx` | 75 | 34 |
| alterado | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | 117 | 73 |
| somente_na_atual | — | `frontend/src/components/pagination/pagination.jsx` | 37 | — |
| somente_na_atual | — | `frontend/src/components/routeBoundary/routeBoundary.jsx` | 61 | — |
| alterado | `frontend/src/components/sidebar/sidebar.jsx` | `frontend/src/components/sidebar/sidebar.jsx` | 138 | 28 |
| somente_na_atual | — | `frontend/src/components/signalOutputs/fleetSignalOutputs.jsx` | 146 | — |
| somente_na_atual | — | `frontend/src/components/signalOutputs/signalOutputList.jsx` | 56 | — |
| alterado | `frontend/src/components/toastCenter/toastCenter.jsx` | `frontend/src/components/toastCenter/toastCenter.jsx` | 12 | 5 |
| alterado | `frontend/src/contexts/monitoringContext.jsx` | `frontend/src/contexts/monitoringContext.jsx` | 364 | 182 |
| somente_na_atual | — | `frontend/src/hooks/useApiQuery.js` | 57 | — |
| somente_na_atual | — | `frontend/src/hooks/useMachineResources.js` | 85 | — |
| alterado | `frontend/src/hooks/useMachines.js` | `frontend/src/hooks/useMachines.js` | 24 | 3 |
| alterado | `frontend/src/hooks/useRelativeDuration.js` | `frontend/src/hooks/useRelativeDuration.js` | 45 | 6 |
| alterado | `frontend/src/index.css` | `frontend/src/index.css` | 92 | 15 |
| alterado | `frontend/src/layouts/dashboardLayout/dashboardLayout.jsx` | `frontend/src/layouts/dashboardLayout/dashboardLayout.jsx` | 14 | 7 |
| alterado | `frontend/src/pages/alerts/alerts.jsx` | `frontend/src/pages/alerts/alerts.jsx` | 38 | 14 |
| alterado | `frontend/src/pages/clients/clients.jsx` | `frontend/src/pages/clients/clients.jsx` | 11 | 6 |
| alterado | `frontend/src/pages/companySelection/companySelection.jsx` | `frontend/src/pages/companySelection/companySelection.jsx` | 111 | 40 |
| alterado | `frontend/src/pages/dashboard/dashboard.jsx` | `frontend/src/pages/dashboard/dashboard.jsx` | 122 | 30 |
| alterado | `frontend/src/pages/devices/devices.jsx` | `frontend/src/pages/devices/devices.jsx` | 25 | 146 |
| alterado | `frontend/src/pages/history/history.jsx` | `frontend/src/pages/history/history.jsx` | 188 | 168 |
| alterado | `frontend/src/pages/landing/landing.jsx` | `frontend/src/pages/landing/landing.jsx` | 29 | 9 |
| alterado | `frontend/src/pages/login/login.jsx` | `frontend/src/pages/login/login.jsx` | 55 | 17 |
| alterado | `frontend/src/pages/machineDetails/machineDetails.jsx` | `frontend/src/pages/machineDetails/machineDetails.jsx` | 347 | 206 |
| alterado | `frontend/src/pages/machines/machines.jsx` | `frontend/src/pages/machines/machines.jsx` | 77 | 20 |
| somente_na_atual | — | `frontend/src/pages/passwordHelp/passwordHelp.jsx` | 21 | — |
| alterado | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | 270 | 61 |
| alterado | `frontend/src/pages/units/units.jsx` | `frontend/src/pages/units/units.jsx` | 44 | 16 |
| alterado | `frontend/src/services/api.js` | `frontend/src/services/api.js` | 137 | 42 |
| somente_na_atual | — | `frontend/src/services/apiConfig.js` | 9 | — |
| somente_na_atual | — | `frontend/src/services/apiConfig.test.js` | 17 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.js` | 31 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.test.js` | 47 | — |
| alterado | `frontend/src/services/machineData.js` | `frontend/src/services/machineData.js` | 124 | 54 |
| alterado | `frontend/src/services/monitoring.js` | `frontend/src/services/monitoring.js` | 115 | 25 |
| alterado | `frontend/src/services/monitoring.test.js` | `frontend/src/services/monitoring.test.js` | 236 | 20 |
| somente_na_atual | — | `frontend/src/services/signalOutputs.js` | 61 | — |
| somente_na_atual | — | `frontend/src/services/signalOutputs.test.js` | 100 | — |
| alterado | `frontend/src/services/telemetry.js` | `frontend/src/services/telemetry.js` | 88 | 22 |
| alterado | `frontend/src/services/telemetry.test.js` | `frontend/src/services/telemetry.test.js` | 148 | 29 |
| alterado | `frontend/src/utils/status.js` | `frontend/src/utils/status.js` | 64 | 29 |
| alterado | `frontend/src/utils/time.js` | `frontend/src/utils/time.js` | 14 | 5 |
| alterado | `frontend/vite.config.js` | `frontend/vite.config.js` | 9 | 8 |
| alterado | `iniciarLocal.ps1` | `iniciarLocal.ps1` | 7 | 6 |
| somente_na_atual | — | `Main.pdf` | — | — |
| alterado | `README.md` | `README.md` | 515 | 135 |
| alterado | `tools/configurarRede.ps1` | `tools/configurarRede.ps1` | 1 | 1 |
| alterado | `tools/configurarTransmissao.py` | `tools/configurarTransmissao.py` | 14 | 15 |
| alterado | `tools/ponteUsb.py` | `tools/ponteUsb.py` | 59 | 42 |
| somente_na_atual | — | `tools/publicarEventos.py` | 42 | — |
| somente_na_atual | — | `tools/simuladorCnc.py` | 53 | — |
| somente_na_outra | `tools/simuladorWifi.py` | — | — | 260 |
| somente_na_atual | — | `tools/testarFrontend.py` | 200 | — |
| alterado | `tools/testarOpta.ps1` | `tools/testarOpta.ps1` | 3 | 3 |
| alterado | `tools/testarProjeto.ps1` | `tools/testarProjeto.ps1` | 3 | 1 |
| alterado | `tools/tests/testConfigurarTransmissao.py` | `tools/tests/testConfigurarTransmissao.py` | 27 | 1 |
| somente_na_atual | — | `tools/tests/testEventTools.py` | 111 | — |
| alterado | `tools/tests/testPonteUsb.py` | `tools/tests/testPonteUsb.py` | 67 | 18 |

## HTTP — SCOMPTECHTTP

Origem: `C:\Users\pedro\OneDrive\Desktop\SCOMPTECHTTP`

Contagens: `{"alterado": 113, "somente_na_atual": 44, "realocado_identico": 41, "somente_na_outra": 14}`

| Estado | Caminho na outra cópia | Caminho na atual | + linhas | − linhas |
|---|---|---|---:|---:|
| alterado | `.gitignore` | `.gitignore` | 41 | 9 |
| alterado | `SCOMPTEC- Back/.env.example` | `backend/.env.example` | 7 | 0 |
| somente_na_atual | — | `backend/config.example.json` | 14 | — |
| alterado | `SCOMPTEC- Back/config.py` | `backend/config.py` | 35 | 4 |
| alterado | `SCOMPTEC- Back/create_admin.py` | `backend/createAdmin.py` | 4 | 4 |
| realocado_identico | `SCOMPTEC- Back/data/seed.test.json` | `backend/data/seed.test.json` | — | — |
| alterado | `SCOMPTEC- Back/Database/Connection.py` | `backend/database/connection.py` | 29 | 1 |
| realocado_identico | `SCOMPTEC- Back/Database/migrations/001_device_network_fields.sql` | `backend/database/migrations/001_deviceNetworkFields.sql` | — | — |
| alterado | `SCOMPTEC- Back/Database/models.py` | `backend/database/models.py` | 34 | 1 |
| alterado | `SCOMPTEC- Back/Main.py` | `backend/main.py` | 8 | 7 |
| alterado | `SCOMPTEC- Back/Schema/admin.py` | `backend/schemas/admin.py` | 1 | 1 |
| realocado_identico | `SCOMPTEC- Back/Schema/auth.py` | `backend/schemas/auth.py` | — | — |
| alterado | `SCOMPTEC- Back/Schema/cnc.py` | `backend/schemas/cnc.py` | 16 | 2 |
| realocado_identico | `SCOMPTEC- Back/Schema/common.py` | `backend/schemas/common.py` | — | — |
| alterado | `SCOMPTEC- Back/Schema/device.py` | `backend/schemas/device.py` | 1 | 1 |
| somente_na_atual | — | `backend/schemas/event.py` | 33 | — |
| somente_na_atual | — | `backend/schemas/observation.py` | 19 | — |
| somente_na_atual | — | `backend/schemas/signalOutput.py` | 10 | — |
| alterado | `SCOMPTEC- Back/Schema/telemetry.py` | `backend/schemas/telemetry.py` | 8 | 15 |
| alterado | `SCOMPTEC- Back/Services/admin_bootstrap.py` | `backend/services/adminBootstrap.py` | 3 | 3 |
| alterado | `SCOMPTEC- Back/Services/adminservice.py` | `backend/services/adminService.py` | 5 | 5 |
| alterado | `SCOMPTEC- Back/Services/authservice.py` | `backend/services/authService.py` | 4 | 4 |
| alterado | `SCOMPTEC- Back/Services/clock.py` | `backend/services/clock.py` | 4 | 4 |
| alterado | `SCOMPTEC- Back/Services/cncservice.py` | `backend/services/cncService.py` | 66 | 27 |
| somente_na_atual | — | `backend/services/codeService.py` | 29 | — |
| alterado | `SCOMPTEC- Back/Services/device_auth.py` | `backend/services/deviceAuth.py` | 2 | 10 |
| alterado | `SCOMPTEC- Back/Services/deviceservice.py` | `backend/services/deviceService.py` | 11 | 31 |
| somente_na_atual | — | `backend/services/eventRepository.py` | 103 | — |
| somente_na_atual | — | `backend/services/events.py` | 88 | — |
| somente_na_atual | — | `backend/services/ingestAuth.py` | 11 | — |
| somente_na_atual | — | `backend/services/machineState.py` | 48 | — |
| realocado_identico | `SCOMPTEC- Back/Services/security.py` | `backend/services/security.py` | — | — |
| somente_na_atual | — | `backend/services/signalOutputs.py` | 82 | — |
| alterado | `SCOMPTEC- Back/Services/telemetry.py` | `backend/services/telemetry.py` | 18 | 61 |
| alterado | `SCOMPTEC- Back/Services/utilization.py` | `backend/services/utilization.py` | 4 | 4 |
| alterado | `SCOMPTEC- Back/tests/test_admin.py` | `backend/tests/testAdmin.py` | 6 | 6 |
| somente_na_atual | — | `backend/tests/testDatabaseBootstrap.py` | 70 | — |
| alterado | `SCOMPTEC- Back/tests/test_device_provisioning.py` | `backend/tests/testDeviceProvisioning.py` | 3 | 3 |
| somente_na_atual | — | `backend/tests/testEvents.py` | 332 | — |
| alterado | `SCOMPTEC- Back/tests/test_mysql_concurrency.py` | `backend/tests/testMysqlConcurrency.py` | 7 | 7 |
| alterado | `SCOMPTEC- Back/tests/test_opta_api.py` | `backend/tests/testOptaApi.py` | 23 | 20 |
| somente_na_atual | — | `backend/tests/testSignalOutputs.py` | 105 | — |
| alterado | `SCOMPTEC- Back/tests/test_simulation_config.py` | `backend/tests/testSimulationConfig.py` | 42 | 1 |
| somente_na_atual | — | `configuracao.json` | 552 | — |
| alterado | `docs/ADMINISTRACAO.md` | `docs/guides/administracao.md` | 6 | 5 |
| alterado | `docs/explicacao_backend_frontend.md` | `docs/guides/explicacaoBackendFrontend.md` | 26 | 636 |
| alterado | `docs/GUIA_EQUIPE.md` | `docs/guides/guiaEquipe.md` | 54 | 441 |
| alterado | `INTEGRACAO_OPTA.md` | `docs/guides/integracaoOpta.md` | 48 | 79 |
| somente_na_atual | — | `docs/guides/testesResponsividade.md` | 49 | — |
| realocado_identico | `docs/SCOMPTEC_Explicacao_Backend_e_Frontend.docx` | `docs/reference/explicacaoBackendFrontend.docx` | — | — |
| realocado_identico | `docs/openapi.json` | `docs/reference/openapi.json` | — | — |
| somente_na_outra | `docs/RELATORIO_COMPLETO_OPTA.txt` | — | — | 737 |
| alterado | `scomptec-cnc front 2/ADMINISTRACAO.md` | `docs/reports/administracaoFrontendLegada.md` | 4 | 2 |
| alterado | `IMPLEMENTATION_REPORT.md` | `docs/reports/implementationReport.md` | 10 | 8 |
| somente_na_atual | — | `docs/reports/sinaisOperacionaisCorrente.md` | 87 | — |
| somente_na_atual | — | `docs/reports/testesCncLocal.md` | 39 | — |
| somente_na_outra | `docs/TESTES_WIFI_LOCAL.md` | — | — | 72 |
| somente_na_atual | — | `examples/machine-event.json` | 11 | — |
| alterado | `firmware/opta_mesa_monitor.zip` | `firmware/archives/optaCncMonitor.zip` | — | — |
| somente_na_outra | `firmware/esp32_cnc_monitor/README.md` | — | — | 28 |
| realocado_identico | `firmware/esp32_cnc_monitor/esp32_cnc_monitor.ino` | `firmware/legacy/esp32CncMonitor/esp32CncMonitor.ino` | — | — |
| realocado_identico | `firmware/esp32_cnc_monitor/platformio.ini` | `firmware/legacy/esp32CncMonitor/platformio.ini` | — | — |
| somente_na_outra | `firmware/opta_mesa_monitor/README.md` | — | — | 52 |
| alterado | `firmware/opta_mesa_monitor/MesaControl.cpp` | `firmware/optaCncMonitor/cncMonitor.cpp` | 42 | 446 |
| alterado | `firmware/opta_mesa_monitor/MesaControl.h` | `firmware/optaCncMonitor/cncMonitor.h` | 2 | 2 |
| alterado | `firmware/opta_mesa_monitor/Config.h` | `firmware/optaCncMonitor/config.h` | 40 | 3 |
| realocado_identico | `firmware/opta_mesa_monitor/HttpResponse.h` | `firmware/optaCncMonitor/httpResponse.h` | — | — |
| somente_na_atual | — | `firmware/optaCncMonitor/inputMonitor.h` | 29 | — |
| alterado | `firmware/opta_mesa_monitor/mesa_sample.json` | `firmware/optaCncMonitor/monitorSample.json` | 23 | 24 |
| alterado | `firmware/opta_mesa_monitor/opta_mesa_monitor.ino` | `firmware/optaCncMonitor/optaCncMonitor.ino` | 5 | 7 |
| somente_na_atual | — | `firmware/optaCncMonitor/signalProfile.h` | 15 | — |
| alterado | `firmware/opta_mesa_monitor/Telemetry.cpp` | `firmware/optaCncMonitor/telemetry.cpp` | 35 | 10 |
| alterado | `firmware/opta_mesa_monitor/Telemetry.h` | `firmware/optaCncMonitor/telemetry.h` | 2 | 2 |
| alterado | `firmware/opta_mesa_monitor/TelemetryCore.h` | `firmware/optaCncMonitor/telemetryCore.h` | 14 | 9 |
| alterado | `firmware/opta_mesa_monitor/TelemetryModel.h` | `firmware/optaCncMonitor/telemetryModel.h` | 3 | 15 |
| alterado | `firmware/opta_mesa_monitor/TelemetryPayload.h` | `firmware/optaCncMonitor/telemetryPayload.h` | 46 | 42 |
| somente_na_outra | `firmware/reference/mesa_opta_v2_original.ino` | — | — | 416 |
| alterado | `firmware/testar-firmware.ps1` | `firmware/testarFirmware.ps1` | 7 | 7 |
| alterado | `firmware/tests/host/Arduino.h` | `firmware/tests/host/Arduino.h` | 5 | 2 |
| alterado | `firmware/tests/host/test_control.cpp` | `firmware/tests/host/testControl.cpp` | 52 | 61 |
| alterado | `firmware/tests/host/test_telemetry.cpp` | `firmware/tests/host/testTelemetry.cpp` | 85 | 16 |
| alterado | `scomptec-cnc front 2/.env.example` | `frontend/.env.example` | 4 | 2 |
| alterado | `scomptec-cnc front 2/.oxlintrc.json` | `frontend/.oxlintrc.json` | 11 | 2 |
| alterado | `scomptec-cnc front 2/electron/main.js` | `frontend/electron/legacy/main.js` | 1 | 1 |
| realocado_identico | `scomptec-cnc front 2/electron/main.cjs` | `frontend/electron/main.cjs` | — | — |
| alterado | `scomptec-cnc front 2/index.html` | `frontend/index.html` | 1 | 1 |
| alterado | `scomptec-cnc front 2/package-lock.json` | `frontend/package-lock.json` | 244 | 215 |
| alterado | `scomptec-cnc front 2/package.json` | `frontend/package.json` | 3 | 12 |
| realocado_identico | `scomptec-cnc front 2/postcss.config.js` | `frontend/postcss.config.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/favicon.svg` | `frontend/public/favicon.svg` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/icons.svg` | `frontend/public/icons.svg` | — | — |
| alterado | `scomptec-cnc front 2/public/login-cnc-background.png` | `frontend/public/loginCncBackground.webp` | — | — |
| somente_na_atual | — | `frontend/public/loginCncBackgroundMobile.webp` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/scomptec-icon.svg` | `frontend/public/scomptecIcon.svg` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/scomptec-logo.webp` | `frontend/public/scomptecLogo.webp` | — | — |
| alterado | `scomptec-cnc front 2/src/App.jsx` | `frontend/src/app.jsx` | 64 | 46 |
| realocado_identico | `scomptec-cnc front 2/src/assets/hero.png` | `frontend/src/assets/hero.png` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/assets/vite.svg` | `frontend/src/assets/vite.svg` | — | — |
| alterado | `scomptec-cnc front 2/src/components/AlertCard/AlertCard.jsx` | `frontend/src/components/alertCard/alertCard.jsx` | 33 | 12 |
| alterado | `scomptec-cnc front 2/src/components/Breadcrumb/Breadcrumb.jsx` | `frontend/src/components/breadcrumb/breadcrumb.jsx` | 1 | 1 |
| somente_na_atual | — | `frontend/src/components/charts/deferredHealth.jsx` | 51 | — |
| somente_na_atual | — | `frontend/src/components/charts/fleetHealth.jsx` | 15 | — |
| alterado | `scomptec-cnc front 2/src/components/charts/TelemetryChart.jsx` | `frontend/src/components/charts/telemetryChart.jsx` | 178 | 40 |
| alterado | `scomptec-cnc front 2/src/components/charts/UtilizationChart.jsx` | `frontend/src/components/charts/utilizationChart.jsx` | 7 | 5 |
| alterado | `scomptec-cnc front 2/src/components/ClientCard/ClientCard.jsx` | `frontend/src/components/clientCard/clientCard.jsx` | 37 | 17 |
| alterado | `scomptec-cnc front 2/src/components/MesaSignals/MesaSignals.jsx` | `frontend/src/components/cncSignals/cncSignals.jsx` | 72 | 61 |
| alterado | `scomptec-cnc front 2/src/components/ConnectionNotice/ConnectionNotice.jsx` | `frontend/src/components/connectionNotice/connectionNotice.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/components/ContextSwitcher/ContextSwitcher.jsx` | `frontend/src/components/contextSwitcher/contextSwitcher.jsx` | 92 | 80 |
| realocado_identico | `scomptec-cnc front 2/src/components/EmptyState/EmptyState.jsx` | `frontend/src/components/emptyState/emptyState.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/Header/Header.jsx` | `frontend/src/components/header/header.jsx` | 290 | 173 |
| somente_na_atual | — | `frontend/src/components/liveTime/liveTime.jsx` | 12 | — |
| realocado_identico | `scomptec-cnc front 2/src/components/LoadingState/LoadingState.jsx` | `frontend/src/components/loadingState/loadingState.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/Logo/Logo.jsx` | `frontend/src/components/logo/logo.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/components/MachineCard/MachineCard.jsx` | `frontend/src/components/machineCard/machineCard.jsx` | 76 | 35 |
| realocado_identico | `scomptec-cnc front 2/src/components/MachineIncidents/MachineIncidents.jsx` | `frontend/src/components/machineIncidents/machineIncidents.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/OccurrenceCard/OccurrenceCard.jsx` | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | 117 | 73 |
| realocado_identico | `scomptec-cnc front 2/src/components/OperatingTimeline/OperatingTimeline.jsx` | `frontend/src/components/operatingTimeline/operatingTimeline.jsx` | — | — |
| somente_na_atual | — | `frontend/src/components/pagination/pagination.jsx` | 37 | — |
| somente_na_atual | — | `frontend/src/components/routeBoundary/routeBoundary.jsx` | 61 | — |
| alterado | `scomptec-cnc front 2/src/components/Sidebar/Sidebar.jsx` | `frontend/src/components/sidebar/sidebar.jsx` | 141 | 31 |
| somente_na_atual | — | `frontend/src/components/signalOutputs/fleetSignalOutputs.jsx` | 146 | — |
| somente_na_atual | — | `frontend/src/components/signalOutputs/signalOutputList.jsx` | 56 | — |
| realocado_identico | `scomptec-cnc front 2/src/components/StatCard/StatCard.jsx` | `frontend/src/components/statCard/statCard.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/components/StatusBadge/StatusBadge.jsx` | `frontend/src/components/statusBadge/statusBadge.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/ToastCenter/ToastCenter.jsx` | `frontend/src/components/toastCenter/toastCenter.jsx` | 12 | 5 |
| alterado | `scomptec-cnc front 2/src/contexts/MonitoringContext.jsx` | `frontend/src/contexts/monitoringContext.jsx` | 364 | 182 |
| realocado_identico | `scomptec-cnc front 2/src/data/mockData.js` | `frontend/src/data/mockData.js` | — | — |
| alterado | `scomptec-cnc front 2/src/hooks/useAlerts.js` | `frontend/src/hooks/useAlerts.js` | 1 | 1 |
| somente_na_atual | — | `frontend/src/hooks/useApiQuery.js` | 57 | — |
| somente_na_atual | — | `frontend/src/hooks/useMachineResources.js` | 85 | — |
| alterado | `scomptec-cnc front 2/src/hooks/useMachines.js` | `frontend/src/hooks/useMachines.js` | 25 | 4 |
| alterado | `scomptec-cnc front 2/src/hooks/useRelativeDuration.js` | `frontend/src/hooks/useRelativeDuration.js` | 45 | 6 |
| alterado | `scomptec-cnc front 2/src/index.css` | `frontend/src/index.css` | 187 | 11 |
| alterado | `scomptec-cnc front 2/src/layouts/DashboardLayout/DashboardLayout.jsx` | `frontend/src/layouts/dashboardLayout/dashboardLayout.jsx` | 19 | 12 |
| alterado | `scomptec-cnc front 2/src/layouts/TVLayout/TVLayout.jsx` | `frontend/src/layouts/tvLayout/tvLayout.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/main.jsx` | `frontend/src/main.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/pages/Admin/admin.css` | `frontend/src/pages/admin/admin.css` | 19 | 0 |
| alterado | `scomptec-cnc front 2/src/pages/Admin/Admin.jsx` | `frontend/src/pages/admin/admin.jsx` | 3 | 3 |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminAccess.jsx` | `frontend/src/pages/admin/adminAccess.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminActivity.jsx` | `frontend/src/pages/admin/adminActivity.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/adminModel.js` | `frontend/src/pages/admin/adminModel.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/adminModel.test.js` | `frontend/src/pages/admin/adminModel.test.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminUserRow.jsx` | `frontend/src/pages/admin/adminUserRow.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/pages/Alerts/Alerts.jsx` | `frontend/src/pages/alerts/alerts.jsx` | 43 | 19 |
| alterado | `scomptec-cnc front 2/src/pages/Clients/Clients.jsx` | `frontend/src/pages/clients/clients.jsx` | 12 | 7 |
| alterado | `scomptec-cnc front 2/src/pages/CompanySelection/CompanySelection.jsx` | `frontend/src/pages/companySelection/companySelection.jsx` | 115 | 44 |
| alterado | `scomptec-cnc front 2/src/pages/Dashboard/Dashboard.jsx` | `frontend/src/pages/dashboard/dashboard.jsx` | 136 | 44 |
| alterado | `scomptec-cnc front 2/src/pages/Devices/Devices.jsx` | `frontend/src/pages/devices/devices.jsx` | 25 | 146 |
| alterado | `scomptec-cnc front 2/src/pages/History/History.jsx` | `frontend/src/pages/history/history.jsx` | 191 | 171 |
| alterado | `scomptec-cnc front 2/src/pages/Landing/Landing.jsx` | `frontend/src/pages/landing/landing.jsx` | 30 | 10 |
| alterado | `scomptec-cnc front 2/src/pages/Login/Login.jsx` | `frontend/src/pages/login/login.jsx` | 56 | 18 |
| alterado | `scomptec-cnc front 2/src/pages/MachineDetails/MachineDetails.jsx` | `frontend/src/pages/machineDetails/machineDetails.jsx` | 354 | 213 |
| alterado | `scomptec-cnc front 2/src/pages/Machines/Machines.jsx` | `frontend/src/pages/machines/machines.jsx` | 80 | 23 |
| somente_na_atual | — | `frontend/src/pages/passwordHelp/passwordHelp.jsx` | 21 | — |
| alterado | `scomptec-cnc front 2/src/pages/Register/Register.jsx` | `frontend/src/pages/register/register.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/pages/Settings/Settings.jsx` | `frontend/src/pages/settings/settings.jsx` | 11 | 0 |
| alterado | `scomptec-cnc front 2/src/pages/Splash/Splash.jsx` | `frontend/src/pages/splash/splash.jsx` | 1 | 1 |
| realocado_identico | `scomptec-cnc front 2/src/pages/TVDashboard/tv.css` | `frontend/src/pages/tvDashboard/tv.css` | — | — |
| alterado | `scomptec-cnc front 2/src/pages/TVDashboard/TVDashboard.jsx` | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | 272 | 63 |
| alterado | `scomptec-cnc front 2/src/pages/Units/Units.jsx` | `frontend/src/pages/units/units.jsx` | 45 | 17 |
| realocado_identico | `scomptec-cnc front 2/src/services/adminSession.js` | `frontend/src/services/adminSession.js` | — | — |
| alterado | `scomptec-cnc front 2/src/services/api.js` | `frontend/src/services/api.js` | 137 | 42 |
| somente_na_atual | — | `frontend/src/services/apiConfig.js` | 9 | — |
| somente_na_atual | — | `frontend/src/services/apiConfig.test.js` | 17 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.js` | 31 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.test.js` | 47 | — |
| realocado_identico | `scomptec-cnc front 2/src/services/eventBus.js` | `frontend/src/services/eventBus.js` | — | — |
| alterado | `scomptec-cnc front 2/src/services/machineData.js` | `frontend/src/services/machineData.js` | 124 | 54 |
| alterado | `scomptec-cnc front 2/src/services/monitoring.js` | `frontend/src/services/monitoring.js` | 115 | 25 |
| alterado | `scomptec-cnc front 2/src/services/monitoring.test.js` | `frontend/src/services/monitoring.test.js` | 236 | 20 |
| alterado | `scomptec-cnc front 2/src/services/preferences.js` | `frontend/src/services/preferences.js` | 3 | 1 |
| somente_na_atual | — | `frontend/src/services/signalOutputs.js` | 61 | — |
| somente_na_atual | — | `frontend/src/services/signalOutputs.test.js` | 100 | — |
| alterado | `scomptec-cnc front 2/src/services/telemetry.js` | `frontend/src/services/telemetry.js` | 88 | 22 |
| alterado | `scomptec-cnc front 2/src/services/telemetry.test.js` | `frontend/src/services/telemetry.test.js` | 148 | 29 |
| realocado_identico | `scomptec-cnc front 2/src/services/utilization.js` | `frontend/src/services/utilization.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/services/utilization.test.js` | `frontend/src/services/utilization.test.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/services/websocket.js` | `frontend/src/services/websocket.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/utils/problems.js` | `frontend/src/utils/problems.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/utils/severity.js` | `frontend/src/utils/severity.js` | — | — |
| alterado | `scomptec-cnc front 2/src/utils/status.js` | `frontend/src/utils/status.js` | 64 | 29 |
| alterado | `scomptec-cnc front 2/src/utils/time.js` | `frontend/src/utils/time.js` | 14 | 5 |
| alterado | `scomptec-cnc front 2/tailwind.config.js` | `frontend/tailwind.config.js` | 20 | 20 |
| alterado | `scomptec-cnc front 2/vite.config.js` | `frontend/vite.config.js` | 9 | 8 |
| somente_na_outra | `iniciar.cmd` | — | — | 80 |
| alterado | `iniciar-local.ps1` | `iniciarLocal.ps1` | 12 | 11 |
| realocado_identico | `tests/conftest.py` | `legacy/mongodb/tests/conftest.py` | — | — |
| realocado_identico | `tests/test_endpoints.py` | `legacy/mongodb/tests/testEndpoints.py` | — | — |
| realocado_identico | `tests/test_services.py` | `legacy/mongodb/tests/testServices.py` | — | — |
| somente_na_atual | — | `Main.pdf` | — | — |
| alterado | `pytest.ini` | `pytest.ini` | 2 | 1 |
| alterado | `README.md` | `README.md` | 531 | 130 |
| alterado | `requirements.txt` | `requirements.txt` | 21 | 9 |
| somente_na_outra | `SCOMPTEC- Back/README.md` | — | — | 48 |
| somente_na_outra | `SCOMPTEC- Back/requirements-dev.txt` | — | — | 3 |
| somente_na_outra | `SCOMPTEC- Back/requirements.txt` | — | — | 6 |
| somente_na_outra | `SCOMPTEC- Back/tests/test_wifi_flow.py` | — | — | 171 |
| somente_na_outra | `scomptec-cnc front 2/.gitignore` | — | — | 4 |
| somente_na_outra | `scomptec-cnc front 2/README.md` | — | — | 115 |
| alterado | `tools/configurar-rede.ps1` | `tools/configurarRede.ps1` | 1 | 1 |
| somente_na_atual | — | `tools/configurarTransmissao.py` | 78 | — |
| alterado | `tools/ponte_usb.py` | `tools/ponteUsb.py` | 105 | 73 |
| somente_na_atual | — | `tools/publicarEventos.py` | 42 | — |
| somente_na_outra | `tools/requirements-usb.txt` | — | — | 2 |
| somente_na_outra | `tools/simulador_wifi.py` | — | — | 260 |
| somente_na_atual | — | `tools/simuladorCnc.py` | 53 | — |
| somente_na_atual | — | `tools/testarFrontend.py` | 200 | — |
| alterado | `docs/testar-opta.ps1` | `tools/testarOpta.ps1` | 3 | 3 |
| alterado | `tools/testar-projeto.ps1` | `tools/testarProjeto.ps1` | 7 | 5 |
| somente_na_atual | — | `tools/tests/testConfigurarTransmissao.py` | 115 | — |
| somente_na_atual | — | `tools/tests/testEventTools.py` | 111 | — |
| alterado | `tools/tests/test_ponte_usb.py` | `tools/tests/testPonteUsb.py` | 132 | 20 |

## V3 — SCOMPTECV3

Origem: `C:\Users\pedro\OneDrive\Desktop\SCOMPTECV3`

Contagens: `{"alterado": 98, "somente_na_atual": 60, "realocado_identico": 40, "somente_na_outra": 11}`

| Estado | Caminho na outra cópia | Caminho na atual | + linhas | − linhas |
|---|---|---|---:|---:|
| alterado | `.gitignore` | `.gitignore` | 41 | 8 |
| alterado | `SCOMPTEC- Back/.env.example` | `backend/.env.example` | 7 | 0 |
| somente_na_atual | — | `backend/config.example.json` | 14 | — |
| alterado | `SCOMPTEC- Back/config.py` | `backend/config.py` | 37 | 2 |
| alterado | `SCOMPTEC- Back/create_admin.py` | `backend/createAdmin.py` | 4 | 4 |
| realocado_identico | `SCOMPTEC- Back/data/seed.test.json` | `backend/data/seed.test.json` | — | — |
| alterado | `SCOMPTEC- Back/Database/Connection.py` | `backend/database/connection.py` | 42 | 3 |
| realocado_identico | `SCOMPTEC- Back/Database/migrations/001_device_network_fields.sql` | `backend/database/migrations/001_deviceNetworkFields.sql` | — | — |
| alterado | `SCOMPTEC- Back/Database/models.py` | `backend/database/models.py` | 34 | 1 |
| alterado | `SCOMPTEC- Back/Main.py` | `backend/main.py` | 8 | 7 |
| alterado | `SCOMPTEC- Back/Schema/admin.py` | `backend/schemas/admin.py` | 1 | 1 |
| realocado_identico | `SCOMPTEC- Back/Schema/auth.py` | `backend/schemas/auth.py` | — | — |
| alterado | `SCOMPTEC- Back/Schema/cnc.py` | `backend/schemas/cnc.py` | 16 | 2 |
| realocado_identico | `SCOMPTEC- Back/Schema/common.py` | `backend/schemas/common.py` | — | — |
| alterado | `SCOMPTEC- Back/Schema/device.py` | `backend/schemas/device.py` | 1 | 1 |
| somente_na_atual | — | `backend/schemas/event.py` | 33 | — |
| somente_na_atual | — | `backend/schemas/observation.py` | 19 | — |
| somente_na_atual | — | `backend/schemas/signalOutput.py` | 10 | — |
| alterado | `SCOMPTEC- Back/Schema/telemetry.py` | `backend/schemas/telemetry.py` | 8 | 15 |
| alterado | `SCOMPTEC- Back/Services/admin_bootstrap.py` | `backend/services/adminBootstrap.py` | 3 | 3 |
| alterado | `SCOMPTEC- Back/Services/adminservice.py` | `backend/services/adminService.py` | 5 | 5 |
| alterado | `SCOMPTEC- Back/Services/authservice.py` | `backend/services/authService.py` | 4 | 4 |
| alterado | `SCOMPTEC- Back/Services/clock.py` | `backend/services/clock.py` | 10 | 4 |
| alterado | `SCOMPTEC- Back/Services/cncservice.py` | `backend/services/cncService.py` | 68 | 29 |
| somente_na_atual | — | `backend/services/codeService.py` | 29 | — |
| alterado | `SCOMPTEC- Back/Services/device_auth.py` | `backend/services/deviceAuth.py` | 2 | 10 |
| alterado | `SCOMPTEC- Back/Services/deviceservice.py` | `backend/services/deviceService.py` | 11 | 31 |
| somente_na_atual | — | `backend/services/eventRepository.py` | 103 | — |
| somente_na_atual | — | `backend/services/events.py` | 88 | — |
| somente_na_atual | — | `backend/services/ingestAuth.py` | 11 | — |
| somente_na_atual | — | `backend/services/machineState.py` | 48 | — |
| realocado_identico | `SCOMPTEC- Back/Services/security.py` | `backend/services/security.py` | — | — |
| somente_na_atual | — | `backend/services/signalOutputs.py` | 82 | — |
| alterado | `SCOMPTEC- Back/Services/telemetry.py` | `backend/services/telemetry.py` | 18 | 54 |
| alterado | `SCOMPTEC- Back/Services/utilization.py` | `backend/services/utilization.py` | 4 | 4 |
| alterado | `SCOMPTEC- Back/tests/test_admin.py` | `backend/tests/testAdmin.py` | 6 | 6 |
| somente_na_atual | — | `backend/tests/testDatabaseBootstrap.py` | 70 | — |
| alterado | `SCOMPTEC- Back/tests/test_device_provisioning.py` | `backend/tests/testDeviceProvisioning.py` | 3 | 3 |
| somente_na_atual | — | `backend/tests/testEvents.py` | 332 | — |
| somente_na_atual | — | `backend/tests/testMysqlConcurrency.py` | 108 | — |
| alterado | `SCOMPTEC- Back/tests/test_opta_api.py` | `backend/tests/testOptaApi.py` | 23 | 20 |
| somente_na_atual | — | `backend/tests/testSignalOutputs.py` | 105 | — |
| somente_na_atual | — | `backend/tests/testSimulationConfig.py` | 58 | — |
| somente_na_atual | — | `configuracao.json` | 552 | — |
| alterado | `docs/ADMINISTRACAO.md` | `docs/guides/administracao.md` | 6 | 5 |
| alterado | `docs/explicacao_backend_frontend.md` | `docs/guides/explicacaoBackendFrontend.md` | 26 | 636 |
| alterado | `docs/GUIA_EQUIPE.md` | `docs/guides/guiaEquipe.md` | 54 | 441 |
| alterado | `INTEGRACAO_OPTA.md` | `docs/guides/integracaoOpta.md` | 48 | 115 |
| somente_na_atual | — | `docs/guides/testesResponsividade.md` | 49 | — |
| realocado_identico | `docs/SCOMPTEC_Explicacao_Backend_e_Frontend.docx` | `docs/reference/explicacaoBackendFrontend.docx` | — | — |
| realocado_identico | `docs/openapi.json` | `docs/reference/openapi.json` | — | — |
| somente_na_outra | `docs/RELATORIO_COMPLETO_OPTA.txt` | — | — | 737 |
| alterado | `scomptec-cnc front 2/ADMINISTRACAO.md` | `docs/reports/administracaoFrontendLegada.md` | 4 | 2 |
| alterado | `IMPLEMENTATION_REPORT.md` | `docs/reports/implementationReport.md` | 10 | 8 |
| somente_na_atual | — | `docs/reports/sinaisOperacionaisCorrente.md` | 87 | — |
| somente_na_atual | — | `docs/reports/testesCncLocal.md` | 39 | — |
| somente_na_atual | — | `examples/machine-event.json` | 11 | — |
| alterado | `firmware/opta_mesa_monitor.zip` | `firmware/archives/optaCncMonitor.zip` | — | — |
| somente_na_outra | `firmware/esp32_cnc_monitor/README.md` | — | — | 28 |
| realocado_identico | `firmware/esp32_cnc_monitor/esp32_cnc_monitor.ino` | `firmware/legacy/esp32CncMonitor/esp32CncMonitor.ino` | — | — |
| realocado_identico | `firmware/esp32_cnc_monitor/platformio.ini` | `firmware/legacy/esp32CncMonitor/platformio.ini` | — | — |
| somente_na_outra | `firmware/opta_mesa_monitor/README.md` | — | — | 18 |
| alterado | `firmware/opta_mesa_monitor/MesaControl.cpp` | `firmware/optaCncMonitor/cncMonitor.cpp` | 42 | 447 |
| alterado | `firmware/opta_mesa_monitor/MesaControl.h` | `firmware/optaCncMonitor/cncMonitor.h` | 2 | 2 |
| alterado | `firmware/opta_mesa_monitor/Config.h` | `firmware/optaCncMonitor/config.h` | 71 | 4 |
| somente_na_atual | — | `firmware/optaCncMonitor/httpResponse.h` | 80 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/inputMonitor.h` | 29 | — |
| alterado | `firmware/opta_mesa_monitor/mesa_sample.json` | `firmware/optaCncMonitor/monitorSample.json` | 23 | 24 |
| alterado | `firmware/opta_mesa_monitor/opta_mesa_monitor.ino` | `firmware/optaCncMonitor/optaCncMonitor.ino` | 5 | 6 |
| somente_na_atual | — | `firmware/optaCncMonitor/signalProfile.h` | 15 | — |
| alterado | `firmware/opta_mesa_monitor/Telemetry.cpp` | `firmware/optaCncMonitor/telemetry.cpp` | 159 | 56 |
| alterado | `firmware/opta_mesa_monitor/Telemetry.h` | `firmware/optaCncMonitor/telemetry.h` | 2 | 24 |
| somente_na_atual | — | `firmware/optaCncMonitor/telemetryCore.h` | 151 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/telemetryModel.h` | 10 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/telemetryPayload.h` | 82 | — |
| somente_na_outra | `firmware/reference/mesa_opta_v2_original.ino` | — | — | 416 |
| somente_na_atual | — | `firmware/testarFirmware.ps1` | 66 | — |
| somente_na_atual | — | `firmware/tests/host/Arduino.h` | 37 | — |
| somente_na_atual | — | `firmware/tests/host/testControl.cpp` | 63 | — |
| somente_na_atual | — | `firmware/tests/host/testTelemetry.cpp` | 181 | — |
| alterado | `scomptec-cnc front 2/.env.example` | `frontend/.env.example` | 4 | 2 |
| alterado | `scomptec-cnc front 2/.oxlintrc.json` | `frontend/.oxlintrc.json` | 11 | 2 |
| alterado | `scomptec-cnc front 2/electron/main.js` | `frontend/electron/legacy/main.js` | 1 | 1 |
| realocado_identico | `scomptec-cnc front 2/electron/main.cjs` | `frontend/electron/main.cjs` | — | — |
| alterado | `scomptec-cnc front 2/index.html` | `frontend/index.html` | 1 | 1 |
| alterado | `scomptec-cnc front 2/package-lock.json` | `frontend/package-lock.json` | 244 | 215 |
| alterado | `scomptec-cnc front 2/package.json` | `frontend/package.json` | 3 | 11 |
| realocado_identico | `scomptec-cnc front 2/postcss.config.js` | `frontend/postcss.config.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/favicon.svg` | `frontend/public/favicon.svg` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/icons.svg` | `frontend/public/icons.svg` | — | — |
| alterado | `scomptec-cnc front 2/public/login-cnc-background.png` | `frontend/public/loginCncBackground.webp` | — | — |
| somente_na_atual | — | `frontend/public/loginCncBackgroundMobile.webp` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/scomptec-icon.svg` | `frontend/public/scomptecIcon.svg` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/scomptec-logo.webp` | `frontend/public/scomptecLogo.webp` | — | — |
| alterado | `scomptec-cnc front 2/src/App.jsx` | `frontend/src/app.jsx` | 64 | 46 |
| realocado_identico | `scomptec-cnc front 2/src/assets/hero.png` | `frontend/src/assets/hero.png` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/assets/vite.svg` | `frontend/src/assets/vite.svg` | — | — |
| alterado | `scomptec-cnc front 2/src/components/AlertCard/AlertCard.jsx` | `frontend/src/components/alertCard/alertCard.jsx` | 33 | 11 |
| alterado | `scomptec-cnc front 2/src/components/Breadcrumb/Breadcrumb.jsx` | `frontend/src/components/breadcrumb/breadcrumb.jsx` | 1 | 1 |
| somente_na_atual | — | `frontend/src/components/charts/deferredHealth.jsx` | 51 | — |
| somente_na_atual | — | `frontend/src/components/charts/fleetHealth.jsx` | 15 | — |
| alterado | `scomptec-cnc front 2/src/components/charts/TelemetryChart.jsx` | `frontend/src/components/charts/telemetryChart.jsx` | 178 | 40 |
| alterado | `scomptec-cnc front 2/src/components/charts/UtilizationChart.jsx` | `frontend/src/components/charts/utilizationChart.jsx` | 7 | 5 |
| alterado | `scomptec-cnc front 2/src/components/ClientCard/ClientCard.jsx` | `frontend/src/components/clientCard/clientCard.jsx` | 37 | 17 |
| alterado | `scomptec-cnc front 2/src/components/MesaSignals/MesaSignals.jsx` | `frontend/src/components/cncSignals/cncSignals.jsx` | 72 | 61 |
| alterado | `scomptec-cnc front 2/src/components/ConnectionNotice/ConnectionNotice.jsx` | `frontend/src/components/connectionNotice/connectionNotice.jsx` | 5 | 5 |
| alterado | `scomptec-cnc front 2/src/components/ContextSwitcher/ContextSwitcher.jsx` | `frontend/src/components/contextSwitcher/contextSwitcher.jsx` | 92 | 80 |
| realocado_identico | `scomptec-cnc front 2/src/components/EmptyState/EmptyState.jsx` | `frontend/src/components/emptyState/emptyState.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/Header/Header.jsx` | `frontend/src/components/header/header.jsx` | 290 | 173 |
| somente_na_atual | — | `frontend/src/components/liveTime/liveTime.jsx` | 12 | — |
| realocado_identico | `scomptec-cnc front 2/src/components/LoadingState/LoadingState.jsx` | `frontend/src/components/loadingState/loadingState.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/Logo/Logo.jsx` | `frontend/src/components/logo/logo.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/components/MachineCard/MachineCard.jsx` | `frontend/src/components/machineCard/machineCard.jsx` | 76 | 35 |
| realocado_identico | `scomptec-cnc front 2/src/components/MachineIncidents/MachineIncidents.jsx` | `frontend/src/components/machineIncidents/machineIncidents.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/OccurrenceCard/OccurrenceCard.jsx` | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | 118 | 73 |
| realocado_identico | `scomptec-cnc front 2/src/components/OperatingTimeline/OperatingTimeline.jsx` | `frontend/src/components/operatingTimeline/operatingTimeline.jsx` | — | — |
| somente_na_atual | — | `frontend/src/components/pagination/pagination.jsx` | 37 | — |
| somente_na_atual | — | `frontend/src/components/routeBoundary/routeBoundary.jsx` | 61 | — |
| alterado | `scomptec-cnc front 2/src/components/Sidebar/Sidebar.jsx` | `frontend/src/components/sidebar/sidebar.jsx` | 141 | 31 |
| somente_na_atual | — | `frontend/src/components/signalOutputs/fleetSignalOutputs.jsx` | 146 | — |
| somente_na_atual | — | `frontend/src/components/signalOutputs/signalOutputList.jsx` | 56 | — |
| realocado_identico | `scomptec-cnc front 2/src/components/StatCard/StatCard.jsx` | `frontend/src/components/statCard/statCard.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/components/StatusBadge/StatusBadge.jsx` | `frontend/src/components/statusBadge/statusBadge.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/ToastCenter/ToastCenter.jsx` | `frontend/src/components/toastCenter/toastCenter.jsx` | 12 | 5 |
| alterado | `scomptec-cnc front 2/src/contexts/MonitoringContext.jsx` | `frontend/src/contexts/monitoringContext.jsx` | 370 | 174 |
| realocado_identico | `scomptec-cnc front 2/src/data/mockData.js` | `frontend/src/data/mockData.js` | — | — |
| alterado | `scomptec-cnc front 2/src/hooks/useAlerts.js` | `frontend/src/hooks/useAlerts.js` | 2 | 2 |
| somente_na_atual | — | `frontend/src/hooks/useApiQuery.js` | 57 | — |
| somente_na_atual | — | `frontend/src/hooks/useMachineResources.js` | 85 | — |
| alterado | `scomptec-cnc front 2/src/hooks/useMachines.js` | `frontend/src/hooks/useMachines.js` | 25 | 4 |
| alterado | `scomptec-cnc front 2/src/hooks/useRelativeDuration.js` | `frontend/src/hooks/useRelativeDuration.js` | 45 | 6 |
| alterado | `scomptec-cnc front 2/src/index.css` | `frontend/src/index.css` | 187 | 11 |
| alterado | `scomptec-cnc front 2/src/layouts/DashboardLayout/DashboardLayout.jsx` | `frontend/src/layouts/dashboardLayout/dashboardLayout.jsx` | 19 | 12 |
| alterado | `scomptec-cnc front 2/src/layouts/TVLayout/TVLayout.jsx` | `frontend/src/layouts/tvLayout/tvLayout.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/main.jsx` | `frontend/src/main.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/pages/Admin/admin.css` | `frontend/src/pages/admin/admin.css` | 19 | 0 |
| alterado | `scomptec-cnc front 2/src/pages/Admin/Admin.jsx` | `frontend/src/pages/admin/admin.jsx` | 3 | 3 |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminAccess.jsx` | `frontend/src/pages/admin/adminAccess.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminActivity.jsx` | `frontend/src/pages/admin/adminActivity.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/adminModel.js` | `frontend/src/pages/admin/adminModel.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/adminModel.test.js` | `frontend/src/pages/admin/adminModel.test.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminUserRow.jsx` | `frontend/src/pages/admin/adminUserRow.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/pages/Alerts/Alerts.jsx` | `frontend/src/pages/alerts/alerts.jsx` | 44 | 20 |
| alterado | `scomptec-cnc front 2/src/pages/Clients/Clients.jsx` | `frontend/src/pages/clients/clients.jsx` | 12 | 7 |
| alterado | `scomptec-cnc front 2/src/pages/CompanySelection/CompanySelection.jsx` | `frontend/src/pages/companySelection/companySelection.jsx` | 115 | 44 |
| alterado | `scomptec-cnc front 2/src/pages/Dashboard/Dashboard.jsx` | `frontend/src/pages/dashboard/dashboard.jsx` | 137 | 44 |
| alterado | `scomptec-cnc front 2/src/pages/Devices/Devices.jsx` | `frontend/src/pages/devices/devices.jsx` | 25 | 146 |
| alterado | `scomptec-cnc front 2/src/pages/History/History.jsx` | `frontend/src/pages/history/history.jsx` | 191 | 171 |
| alterado | `scomptec-cnc front 2/src/pages/Landing/Landing.jsx` | `frontend/src/pages/landing/landing.jsx` | 30 | 10 |
| alterado | `scomptec-cnc front 2/src/pages/Login/Login.jsx` | `frontend/src/pages/login/login.jsx` | 56 | 18 |
| alterado | `scomptec-cnc front 2/src/pages/MachineDetails/MachineDetails.jsx` | `frontend/src/pages/machineDetails/machineDetails.jsx` | 356 | 214 |
| alterado | `scomptec-cnc front 2/src/pages/Machines/Machines.jsx` | `frontend/src/pages/machines/machines.jsx` | 80 | 23 |
| somente_na_atual | — | `frontend/src/pages/passwordHelp/passwordHelp.jsx` | 21 | — |
| alterado | `scomptec-cnc front 2/src/pages/Register/Register.jsx` | `frontend/src/pages/register/register.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/pages/Settings/Settings.jsx` | `frontend/src/pages/settings/settings.jsx` | 11 | 0 |
| alterado | `scomptec-cnc front 2/src/pages/Splash/Splash.jsx` | `frontend/src/pages/splash/splash.jsx` | 1 | 1 |
| realocado_identico | `scomptec-cnc front 2/src/pages/TVDashboard/tv.css` | `frontend/src/pages/tvDashboard/tv.css` | — | — |
| alterado | `scomptec-cnc front 2/src/pages/TVDashboard/TVDashboard.jsx` | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | 272 | 62 |
| alterado | `scomptec-cnc front 2/src/pages/Units/Units.jsx` | `frontend/src/pages/units/units.jsx` | 45 | 17 |
| realocado_identico | `scomptec-cnc front 2/src/services/adminSession.js` | `frontend/src/services/adminSession.js` | — | — |
| alterado | `scomptec-cnc front 2/src/services/api.js` | `frontend/src/services/api.js` | 140 | 90 |
| somente_na_atual | — | `frontend/src/services/apiConfig.js` | 9 | — |
| somente_na_atual | — | `frontend/src/services/apiConfig.test.js` | 17 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.js` | 31 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.test.js` | 47 | — |
| realocado_identico | `scomptec-cnc front 2/src/services/eventBus.js` | `frontend/src/services/eventBus.js` | — | — |
| somente_na_atual | — | `frontend/src/services/machineData.js` | 130 | — |
| somente_na_atual | — | `frontend/src/services/monitoring.js` | 132 | — |
| somente_na_atual | — | `frontend/src/services/monitoring.test.js` | 338 | — |
| alterado | `scomptec-cnc front 2/src/services/preferences.js` | `frontend/src/services/preferences.js` | 3 | 1 |
| somente_na_atual | — | `frontend/src/services/signalOutputs.js` | 61 | — |
| somente_na_atual | — | `frontend/src/services/signalOutputs.test.js` | 100 | — |
| alterado | `scomptec-cnc front 2/src/services/telemetry.js` | `frontend/src/services/telemetry.js` | 87 | 21 |
| alterado | `scomptec-cnc front 2/src/services/telemetry.test.js` | `frontend/src/services/telemetry.test.js` | 148 | 29 |
| realocado_identico | `scomptec-cnc front 2/src/services/utilization.js` | `frontend/src/services/utilization.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/services/utilization.test.js` | `frontend/src/services/utilization.test.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/services/websocket.js` | `frontend/src/services/websocket.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/utils/problems.js` | `frontend/src/utils/problems.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/utils/severity.js` | `frontend/src/utils/severity.js` | — | — |
| alterado | `scomptec-cnc front 2/src/utils/status.js` | `frontend/src/utils/status.js` | 66 | 31 |
| alterado | `scomptec-cnc front 2/src/utils/time.js` | `frontend/src/utils/time.js` | 14 | 5 |
| alterado | `scomptec-cnc front 2/tailwind.config.js` | `frontend/tailwind.config.js` | 20 | 20 |
| alterado | `scomptec-cnc front 2/vite.config.js` | `frontend/vite.config.js` | 9 | 8 |
| somente_na_outra | `iniciar.cmd` | — | — | 69 |
| somente_na_atual | — | `iniciarLocal.ps1` | 169 | — |
| realocado_identico | `tests/conftest.py` | `legacy/mongodb/tests/conftest.py` | — | — |
| realocado_identico | `tests/test_endpoints.py` | `legacy/mongodb/tests/testEndpoints.py` | — | — |
| realocado_identico | `tests/test_services.py` | `legacy/mongodb/tests/testServices.py` | — | — |
| somente_na_atual | — | `Main.pdf` | — | — |
| alterado | `pytest.ini` | `pytest.ini` | 2 | 1 |
| alterado | `README.md` | `README.md` | 531 | 128 |
| alterado | `requirements.txt` | `requirements.txt` | 21 | 9 |
| somente_na_outra | `SCOMPTEC- Back/README.md` | — | — | 48 |
| somente_na_outra | `SCOMPTEC- Back/requirements-dev.txt` | — | — | 3 |
| somente_na_outra | `SCOMPTEC- Back/requirements.txt` | — | — | 6 |
| somente_na_outra | `scomptec-cnc front 2/.gitignore` | — | — | 4 |
| somente_na_outra | `scomptec-cnc front 2/README.md` | — | — | 115 |
| somente_na_atual | — | `tools/configurarRede.ps1` | 39 | — |
| somente_na_atual | — | `tools/configurarTransmissao.py` | 78 | — |
| alterado | `tools/ponte_usb.py` | `tools/ponteUsb.py` | 105 | 73 |
| somente_na_atual | — | `tools/publicarEventos.py` | 42 | — |
| somente_na_outra | `tools/requirements-usb.txt` | — | — | 2 |
| somente_na_atual | — | `tools/simuladorCnc.py` | 53 | — |
| somente_na_atual | — | `tools/testarFrontend.py` | 200 | — |
| alterado | `docs/testar-opta.ps1` | `tools/testarOpta.ps1` | 3 | 3 |
| somente_na_atual | — | `tools/testarProjeto.ps1` | 123 | — |
| somente_na_atual | — | `tools/tests/testConfigurarTransmissao.py` | 115 | — |
| somente_na_atual | — | `tools/tests/testEventTools.py` | 111 | — |
| alterado | `tools/tests/test_ponte_usb.py` | `tools/tests/testPonteUsb.py` | 132 | 20 |

## TCC — ScompTecTCC-main

Origem: `C:\Users\pedro\OneDrive\Desktop\ps3youtube\ScompTecTCC-main`

Contagens: `{"alterado": 97, "somente_na_atual": 62, "realocado_identico": 39, "somente_na_outra": 12}`

| Estado | Caminho na outra cópia | Caminho na atual | + linhas | − linhas |
|---|---|---|---:|---:|
| alterado | `.gitignore` | `.gitignore` | 41 | 8 |
| alterado | `SCOMPTEC- Back/.env.example` | `backend/.env.example` | 50 | 9 |
| somente_na_atual | — | `backend/config.example.json` | 14 | — |
| alterado | `SCOMPTEC- Back/config.py` | `backend/config.py` | 37 | 2 |
| alterado | `SCOMPTEC- Back/create_admin.py` | `backend/createAdmin.py` | 4 | 4 |
| realocado_identico | `SCOMPTEC- Back/data/seed.test.json` | `backend/data/seed.test.json` | — | — |
| alterado | `SCOMPTEC- Back/Database/Connection.py` | `backend/database/connection.py` | 42 | 3 |
| realocado_identico | `SCOMPTEC- Back/Database/migrations/001_device_network_fields.sql` | `backend/database/migrations/001_deviceNetworkFields.sql` | — | — |
| alterado | `SCOMPTEC- Back/Database/models.py` | `backend/database/models.py` | 34 | 1 |
| alterado | `SCOMPTEC- Back/Main.py` | `backend/main.py` | 9 | 8 |
| alterado | `SCOMPTEC- Back/Schema/admin.py` | `backend/schemas/admin.py` | 1 | 1 |
| realocado_identico | `SCOMPTEC- Back/Schema/auth.py` | `backend/schemas/auth.py` | — | — |
| alterado | `SCOMPTEC- Back/Schema/cnc.py` | `backend/schemas/cnc.py` | 16 | 2 |
| realocado_identico | `SCOMPTEC- Back/Schema/common.py` | `backend/schemas/common.py` | — | — |
| alterado | `SCOMPTEC- Back/Schema/device.py` | `backend/schemas/device.py` | 1 | 1 |
| somente_na_atual | — | `backend/schemas/event.py` | 33 | — |
| somente_na_atual | — | `backend/schemas/observation.py` | 19 | — |
| somente_na_atual | — | `backend/schemas/signalOutput.py` | 10 | — |
| alterado | `SCOMPTEC- Back/Schema/telemetry.py` | `backend/schemas/telemetry.py` | 8 | 15 |
| alterado | `SCOMPTEC- Back/Services/admin_bootstrap.py` | `backend/services/adminBootstrap.py` | 3 | 3 |
| alterado | `SCOMPTEC- Back/Services/adminservice.py` | `backend/services/adminService.py` | 5 | 5 |
| alterado | `SCOMPTEC- Back/Services/authservice.py` | `backend/services/authService.py` | 4 | 4 |
| alterado | `SCOMPTEC- Back/Services/clock.py` | `backend/services/clock.py` | 10 | 4 |
| alterado | `SCOMPTEC- Back/Services/cncservice.py` | `backend/services/cncService.py` | 68 | 29 |
| somente_na_atual | — | `backend/services/codeService.py` | 29 | — |
| alterado | `SCOMPTEC- Back/Services/device_auth.py` | `backend/services/deviceAuth.py` | 2 | 10 |
| alterado | `SCOMPTEC- Back/Services/deviceservice.py` | `backend/services/deviceService.py` | 11 | 31 |
| somente_na_atual | — | `backend/services/eventRepository.py` | 103 | — |
| somente_na_atual | — | `backend/services/events.py` | 88 | — |
| somente_na_atual | — | `backend/services/ingestAuth.py` | 11 | — |
| somente_na_atual | — | `backend/services/machineState.py` | 48 | — |
| realocado_identico | `SCOMPTEC- Back/Services/security.py` | `backend/services/security.py` | — | — |
| somente_na_atual | — | `backend/services/signalOutputs.py` | 82 | — |
| alterado | `SCOMPTEC- Back/Services/telemetry.py` | `backend/services/telemetry.py` | 18 | 54 |
| alterado | `SCOMPTEC- Back/Services/utilization.py` | `backend/services/utilization.py` | 4 | 4 |
| alterado | `SCOMPTEC- Back/tests/test_admin.py` | `backend/tests/testAdmin.py` | 6 | 6 |
| somente_na_atual | — | `backend/tests/testDatabaseBootstrap.py` | 70 | — |
| alterado | `SCOMPTEC- Back/tests/test_device_provisioning.py` | `backend/tests/testDeviceProvisioning.py` | 3 | 3 |
| somente_na_atual | — | `backend/tests/testEvents.py` | 332 | — |
| somente_na_atual | — | `backend/tests/testMysqlConcurrency.py` | 108 | — |
| alterado | `SCOMPTEC- Back/tests/test_opta_api.py` | `backend/tests/testOptaApi.py` | 23 | 20 |
| somente_na_atual | — | `backend/tests/testSignalOutputs.py` | 105 | — |
| somente_na_atual | — | `backend/tests/testSimulationConfig.py` | 58 | — |
| somente_na_atual | — | `configuracao.json` | 552 | — |
| alterado | `docs/ADMINISTRACAO.md` | `docs/guides/administracao.md` | 6 | 5 |
| alterado | `docs/explicacao_backend_frontend.md` | `docs/guides/explicacaoBackendFrontend.md` | 26 | 636 |
| alterado | `docs/GUIA_EQUIPE.md` | `docs/guides/guiaEquipe.md` | 54 | 441 |
| alterado | `INTEGRACAO_OPTA.md` | `docs/guides/integracaoOpta.md` | 46 | 162 |
| somente_na_atual | — | `docs/guides/testesResponsividade.md` | 49 | — |
| realocado_identico | `docs/SCOMPTEC_Explicacao_Backend_e_Frontend.docx` | `docs/reference/explicacaoBackendFrontend.docx` | — | — |
| realocado_identico | `docs/openapi.json` | `docs/reference/openapi.json` | — | — |
| somente_na_outra | `docs/RELATORIO_COMPLETO_OPTA.txt` | — | — | 737 |
| alterado | `scomptec-cnc front 2/ADMINISTRACAO.md` | `docs/reports/administracaoFrontendLegada.md` | 4 | 2 |
| alterado | `IMPLEMENTATION_REPORT.md` | `docs/reports/implementationReport.md` | 10 | 8 |
| somente_na_atual | — | `docs/reports/sinaisOperacionaisCorrente.md` | 87 | — |
| somente_na_atual | — | `docs/reports/testesCncLocal.md` | 39 | — |
| somente_na_atual | — | `examples/machine-event.json` | 11 | — |
| somente_na_outra | `explicacao_backend.txt` | — | — | 334 |
| alterado | `firmware/opta_mesa_monitor.zip` | `firmware/archives/optaCncMonitor.zip` | — | — |
| somente_na_outra | `firmware/esp32_cnc_monitor/README.md` | — | — | 28 |
| realocado_identico | `firmware/esp32_cnc_monitor/esp32_cnc_monitor.ino` | `firmware/legacy/esp32CncMonitor/esp32CncMonitor.ino` | — | — |
| realocado_identico | `firmware/esp32_cnc_monitor/platformio.ini` | `firmware/legacy/esp32CncMonitor/platformio.ini` | — | — |
| somente_na_outra | `firmware/opta_mesa_monitor/opta_secrets.example.h` | — | — | 10 |
| somente_na_outra | `firmware/opta_mesa_monitor/README.md` | — | — | 109 |
| alterado | `firmware/opta_mesa_monitor/MesaControl.cpp` | `firmware/optaCncMonitor/cncMonitor.cpp` | 42 | 417 |
| alterado | `firmware/opta_mesa_monitor/MesaControl.h` | `firmware/optaCncMonitor/cncMonitor.h` | 2 | 2 |
| alterado | `firmware/opta_mesa_monitor/Config.h` | `firmware/optaCncMonitor/config.h` | 70 | 12 |
| somente_na_atual | — | `firmware/optaCncMonitor/httpResponse.h` | 80 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/inputMonitor.h` | 29 | — |
| alterado | `firmware/opta_mesa_monitor/mesa_sample.json` | `firmware/optaCncMonitor/monitorSample.json` | 23 | 24 |
| alterado | `firmware/opta_mesa_monitor/opta_mesa_monitor.ino` | `firmware/optaCncMonitor/optaCncMonitor.ino` | 5 | 6 |
| somente_na_atual | — | `firmware/optaCncMonitor/signalProfile.h` | 15 | — |
| alterado | `firmware/opta_mesa_monitor/Telemetry.cpp` | `firmware/optaCncMonitor/telemetry.cpp` | 145 | 240 |
| alterado | `firmware/opta_mesa_monitor/Telemetry.h` | `firmware/optaCncMonitor/telemetry.h` | 2 | 24 |
| somente_na_atual | — | `firmware/optaCncMonitor/telemetryCore.h` | 151 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/telemetryModel.h` | 10 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/telemetryPayload.h` | 82 | — |
| somente_na_outra | `firmware/reference/mesa_opta_v2_original.ino` | — | — | 416 |
| somente_na_atual | — | `firmware/testarFirmware.ps1` | 66 | — |
| somente_na_atual | — | `firmware/tests/host/Arduino.h` | 37 | — |
| somente_na_atual | — | `firmware/tests/host/testControl.cpp` | 63 | — |
| somente_na_atual | — | `firmware/tests/host/testTelemetry.cpp` | 181 | — |
| alterado | `scomptec-cnc front 2/.env.example` | `frontend/.env.example` | 4 | 2 |
| alterado | `scomptec-cnc front 2/.oxlintrc.json` | `frontend/.oxlintrc.json` | 11 | 2 |
| alterado | `scomptec-cnc front 2/electron/main.js` | `frontend/electron/legacy/main.js` | 1 | 1 |
| alterado | `scomptec-cnc front 2/electron/main.cjs` | `frontend/electron/main.cjs` | 34 | 5 |
| alterado | `scomptec-cnc front 2/index.html` | `frontend/index.html` | 1 | 1 |
| alterado | `scomptec-cnc front 2/package-lock.json` | `frontend/package-lock.json` | 244 | 215 |
| alterado | `scomptec-cnc front 2/package.json` | `frontend/package.json` | 3 | 11 |
| realocado_identico | `scomptec-cnc front 2/postcss.config.js` | `frontend/postcss.config.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/favicon.svg` | `frontend/public/favicon.svg` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/icons.svg` | `frontend/public/icons.svg` | — | — |
| alterado | `scomptec-cnc front 2/public/login-cnc-background.png` | `frontend/public/loginCncBackground.webp` | — | — |
| somente_na_atual | — | `frontend/public/loginCncBackgroundMobile.webp` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/scomptec-icon.svg` | `frontend/public/scomptecIcon.svg` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/scomptec-logo.webp` | `frontend/public/scomptecLogo.webp` | — | — |
| alterado | `scomptec-cnc front 2/src/App.jsx` | `frontend/src/app.jsx` | 64 | 46 |
| realocado_identico | `scomptec-cnc front 2/src/assets/hero.png` | `frontend/src/assets/hero.png` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/assets/vite.svg` | `frontend/src/assets/vite.svg` | — | — |
| alterado | `scomptec-cnc front 2/src/components/AlertCard/AlertCard.jsx` | `frontend/src/components/alertCard/alertCard.jsx` | 33 | 11 |
| alterado | `scomptec-cnc front 2/src/components/Breadcrumb/Breadcrumb.jsx` | `frontend/src/components/breadcrumb/breadcrumb.jsx` | 1 | 1 |
| somente_na_atual | — | `frontend/src/components/charts/deferredHealth.jsx` | 51 | — |
| somente_na_atual | — | `frontend/src/components/charts/fleetHealth.jsx` | 15 | — |
| alterado | `scomptec-cnc front 2/src/components/charts/TelemetryChart.jsx` | `frontend/src/components/charts/telemetryChart.jsx` | 178 | 40 |
| alterado | `scomptec-cnc front 2/src/components/charts/UtilizationChart.jsx` | `frontend/src/components/charts/utilizationChart.jsx` | 7 | 5 |
| alterado | `scomptec-cnc front 2/src/components/ClientCard/ClientCard.jsx` | `frontend/src/components/clientCard/clientCard.jsx` | 37 | 17 |
| alterado | `scomptec-cnc front 2/src/components/MesaSignals/MesaSignals.jsx` | `frontend/src/components/cncSignals/cncSignals.jsx` | 72 | 61 |
| alterado | `scomptec-cnc front 2/src/components/ConnectionNotice/ConnectionNotice.jsx` | `frontend/src/components/connectionNotice/connectionNotice.jsx` | 5 | 5 |
| alterado | `scomptec-cnc front 2/src/components/ContextSwitcher/ContextSwitcher.jsx` | `frontend/src/components/contextSwitcher/contextSwitcher.jsx` | 92 | 80 |
| realocado_identico | `scomptec-cnc front 2/src/components/EmptyState/EmptyState.jsx` | `frontend/src/components/emptyState/emptyState.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/Header/Header.jsx` | `frontend/src/components/header/header.jsx` | 290 | 173 |
| somente_na_atual | — | `frontend/src/components/liveTime/liveTime.jsx` | 12 | — |
| realocado_identico | `scomptec-cnc front 2/src/components/LoadingState/LoadingState.jsx` | `frontend/src/components/loadingState/loadingState.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/Logo/Logo.jsx` | `frontend/src/components/logo/logo.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/components/MachineCard/MachineCard.jsx` | `frontend/src/components/machineCard/machineCard.jsx` | 76 | 35 |
| realocado_identico | `scomptec-cnc front 2/src/components/MachineIncidents/MachineIncidents.jsx` | `frontend/src/components/machineIncidents/machineIncidents.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/OccurrenceCard/OccurrenceCard.jsx` | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | 118 | 73 |
| realocado_identico | `scomptec-cnc front 2/src/components/OperatingTimeline/OperatingTimeline.jsx` | `frontend/src/components/operatingTimeline/operatingTimeline.jsx` | — | — |
| somente_na_atual | — | `frontend/src/components/pagination/pagination.jsx` | 37 | — |
| somente_na_atual | — | `frontend/src/components/routeBoundary/routeBoundary.jsx` | 61 | — |
| alterado | `scomptec-cnc front 2/src/components/Sidebar/Sidebar.jsx` | `frontend/src/components/sidebar/sidebar.jsx` | 141 | 31 |
| somente_na_atual | — | `frontend/src/components/signalOutputs/fleetSignalOutputs.jsx` | 146 | — |
| somente_na_atual | — | `frontend/src/components/signalOutputs/signalOutputList.jsx` | 56 | — |
| realocado_identico | `scomptec-cnc front 2/src/components/StatCard/StatCard.jsx` | `frontend/src/components/statCard/statCard.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/components/StatusBadge/StatusBadge.jsx` | `frontend/src/components/statusBadge/statusBadge.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/ToastCenter/ToastCenter.jsx` | `frontend/src/components/toastCenter/toastCenter.jsx` | 12 | 5 |
| alterado | `scomptec-cnc front 2/src/contexts/MonitoringContext.jsx` | `frontend/src/contexts/monitoringContext.jsx` | 370 | 174 |
| realocado_identico | `scomptec-cnc front 2/src/data/mockData.js` | `frontend/src/data/mockData.js` | — | — |
| alterado | `scomptec-cnc front 2/src/hooks/useAlerts.js` | `frontend/src/hooks/useAlerts.js` | 2 | 2 |
| somente_na_atual | — | `frontend/src/hooks/useApiQuery.js` | 57 | — |
| somente_na_atual | — | `frontend/src/hooks/useMachineResources.js` | 85 | — |
| alterado | `scomptec-cnc front 2/src/hooks/useMachines.js` | `frontend/src/hooks/useMachines.js` | 25 | 4 |
| alterado | `scomptec-cnc front 2/src/hooks/useRelativeDuration.js` | `frontend/src/hooks/useRelativeDuration.js` | 45 | 6 |
| alterado | `scomptec-cnc front 2/src/index.css` | `frontend/src/index.css` | 187 | 11 |
| alterado | `scomptec-cnc front 2/src/layouts/DashboardLayout/DashboardLayout.jsx` | `frontend/src/layouts/dashboardLayout/dashboardLayout.jsx` | 19 | 12 |
| alterado | `scomptec-cnc front 2/src/layouts/TVLayout/TVLayout.jsx` | `frontend/src/layouts/tvLayout/tvLayout.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/main.jsx` | `frontend/src/main.jsx` | 3 | 3 |
| alterado | `scomptec-cnc front 2/src/pages/Admin/admin.css` | `frontend/src/pages/admin/admin.css` | 19 | 0 |
| alterado | `scomptec-cnc front 2/src/pages/Admin/Admin.jsx` | `frontend/src/pages/admin/admin.jsx` | 3 | 3 |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminAccess.jsx` | `frontend/src/pages/admin/adminAccess.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminActivity.jsx` | `frontend/src/pages/admin/adminActivity.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/adminModel.js` | `frontend/src/pages/admin/adminModel.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/adminModel.test.js` | `frontend/src/pages/admin/adminModel.test.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminUserRow.jsx` | `frontend/src/pages/admin/adminUserRow.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/pages/Alerts/Alerts.jsx` | `frontend/src/pages/alerts/alerts.jsx` | 44 | 20 |
| alterado | `scomptec-cnc front 2/src/pages/Clients/Clients.jsx` | `frontend/src/pages/clients/clients.jsx` | 12 | 7 |
| alterado | `scomptec-cnc front 2/src/pages/CompanySelection/CompanySelection.jsx` | `frontend/src/pages/companySelection/companySelection.jsx` | 115 | 44 |
| alterado | `scomptec-cnc front 2/src/pages/Dashboard/Dashboard.jsx` | `frontend/src/pages/dashboard/dashboard.jsx` | 137 | 44 |
| alterado | `scomptec-cnc front 2/src/pages/Devices/Devices.jsx` | `frontend/src/pages/devices/devices.jsx` | 25 | 146 |
| alterado | `scomptec-cnc front 2/src/pages/History/History.jsx` | `frontend/src/pages/history/history.jsx` | 191 | 171 |
| alterado | `scomptec-cnc front 2/src/pages/Landing/Landing.jsx` | `frontend/src/pages/landing/landing.jsx` | 30 | 10 |
| alterado | `scomptec-cnc front 2/src/pages/Login/Login.jsx` | `frontend/src/pages/login/login.jsx` | 56 | 18 |
| alterado | `scomptec-cnc front 2/src/pages/MachineDetails/MachineDetails.jsx` | `frontend/src/pages/machineDetails/machineDetails.jsx` | 356 | 214 |
| alterado | `scomptec-cnc front 2/src/pages/Machines/Machines.jsx` | `frontend/src/pages/machines/machines.jsx` | 80 | 23 |
| somente_na_atual | — | `frontend/src/pages/passwordHelp/passwordHelp.jsx` | 21 | — |
| alterado | `scomptec-cnc front 2/src/pages/Register/Register.jsx` | `frontend/src/pages/register/register.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/pages/Settings/Settings.jsx` | `frontend/src/pages/settings/settings.jsx` | 11 | 0 |
| alterado | `scomptec-cnc front 2/src/pages/Splash/Splash.jsx` | `frontend/src/pages/splash/splash.jsx` | 1 | 1 |
| realocado_identico | `scomptec-cnc front 2/src/pages/TVDashboard/tv.css` | `frontend/src/pages/tvDashboard/tv.css` | — | — |
| alterado | `scomptec-cnc front 2/src/pages/TVDashboard/TVDashboard.jsx` | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | 272 | 62 |
| alterado | `scomptec-cnc front 2/src/pages/Units/Units.jsx` | `frontend/src/pages/units/units.jsx` | 45 | 17 |
| realocado_identico | `scomptec-cnc front 2/src/services/adminSession.js` | `frontend/src/services/adminSession.js` | — | — |
| alterado | `scomptec-cnc front 2/src/services/api.js` | `frontend/src/services/api.js` | 140 | 90 |
| somente_na_atual | — | `frontend/src/services/apiConfig.js` | 9 | — |
| somente_na_atual | — | `frontend/src/services/apiConfig.test.js` | 17 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.js` | 31 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.test.js` | 47 | — |
| realocado_identico | `scomptec-cnc front 2/src/services/eventBus.js` | `frontend/src/services/eventBus.js` | — | — |
| somente_na_atual | — | `frontend/src/services/machineData.js` | 130 | — |
| somente_na_atual | — | `frontend/src/services/monitoring.js` | 132 | — |
| somente_na_atual | — | `frontend/src/services/monitoring.test.js` | 338 | — |
| alterado | `scomptec-cnc front 2/src/services/preferences.js` | `frontend/src/services/preferences.js` | 3 | 1 |
| somente_na_atual | — | `frontend/src/services/signalOutputs.js` | 61 | — |
| somente_na_atual | — | `frontend/src/services/signalOutputs.test.js` | 100 | — |
| alterado | `scomptec-cnc front 2/src/services/telemetry.js` | `frontend/src/services/telemetry.js` | 87 | 21 |
| alterado | `scomptec-cnc front 2/src/services/telemetry.test.js` | `frontend/src/services/telemetry.test.js` | 148 | 29 |
| realocado_identico | `scomptec-cnc front 2/src/services/utilization.js` | `frontend/src/services/utilization.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/services/utilization.test.js` | `frontend/src/services/utilization.test.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/services/websocket.js` | `frontend/src/services/websocket.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/utils/problems.js` | `frontend/src/utils/problems.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/utils/severity.js` | `frontend/src/utils/severity.js` | — | — |
| alterado | `scomptec-cnc front 2/src/utils/status.js` | `frontend/src/utils/status.js` | 66 | 31 |
| alterado | `scomptec-cnc front 2/src/utils/time.js` | `frontend/src/utils/time.js` | 14 | 5 |
| alterado | `scomptec-cnc front 2/tailwind.config.js` | `frontend/tailwind.config.js` | 20 | 20 |
| alterado | `scomptec-cnc front 2/vite.config.js` | `frontend/vite.config.js` | 10 | 9 |
| somente_na_outra | `iniciar.cmd` | — | — | 68 |
| somente_na_atual | — | `iniciarLocal.ps1` | 169 | — |
| realocado_identico | `tests/conftest.py` | `legacy/mongodb/tests/conftest.py` | — | — |
| realocado_identico | `tests/test_endpoints.py` | `legacy/mongodb/tests/testEndpoints.py` | — | — |
| realocado_identico | `tests/test_services.py` | `legacy/mongodb/tests/testServices.py` | — | — |
| somente_na_atual | — | `Main.pdf` | — | — |
| alterado | `pytest.ini` | `pytest.ini` | 2 | 1 |
| alterado | `README.md` | `README.md` | 554 | 31 |
| alterado | `requirements.txt` | `requirements.txt` | 21 | 9 |
| somente_na_outra | `SCOMPTEC- Back/README.md` | — | — | 31 |
| somente_na_outra | `SCOMPTEC- Back/requirements-dev.txt` | — | — | 3 |
| somente_na_outra | `SCOMPTEC- Back/requirements.txt` | — | — | 6 |
| somente_na_outra | `scomptec-cnc front 2/.gitignore` | — | — | 4 |
| somente_na_outra | `scomptec-cnc front 2/README.md` | — | — | 82 |
| somente_na_atual | — | `tools/configurarRede.ps1` | 39 | — |
| somente_na_atual | — | `tools/configurarTransmissao.py` | 78 | — |
| somente_na_atual | — | `tools/ponteUsb.py` | 277 | — |
| somente_na_atual | — | `tools/publicarEventos.py` | 42 | — |
| somente_na_atual | — | `tools/simuladorCnc.py` | 53 | — |
| somente_na_atual | — | `tools/testarFrontend.py` | 200 | — |
| alterado | `docs/testar-opta.ps1` | `tools/testarOpta.ps1` | 3 | 3 |
| somente_na_atual | — | `tools/testarProjeto.ps1` | 123 | — |
| somente_na_atual | — | `tools/tests/testConfigurarTransmissao.py` | 115 | — |
| somente_na_atual | — | `tools/tests/testEventTools.py` | 111 | — |
| somente_na_atual | — | `tools/tests/testPonteUsb.py` | 259 | — |

## ZIP_ULTRON_1 — ZIP UltronScomptec-main (1)

Origem: `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main (1).zip`

Contagens: `{"alterado": 85, "identico": 71, "somente_na_atual": 41, "somente_na_outra": 6, "realocado_identico": 1}`

| Estado | Caminho na outra cópia | Caminho na atual | + linhas | − linhas |
|---|---|---|---:|---:|
| alterado | `.gitignore` | `.gitignore` | 4 | 0 |
| alterado | `backend/.env.example` | `backend/.env.example` | 7 | 0 |
| alterado | `backend/config.example.json` | `backend/config.example.json` | 3 | 1 |
| alterado | `backend/config.py` | `backend/config.py` | 1 | 1 |
| alterado | `backend/database/models.py` | `backend/database/models.py` | 34 | 1 |
| alterado | `backend/main.py` | `backend/main.py` | 2 | 1 |
| alterado | `backend/schemas/cnc.py` | `backend/schemas/cnc.py` | 15 | 1 |
| somente_na_atual | — | `backend/schemas/event.py` | 33 | — |
| somente_na_atual | — | `backend/schemas/observation.py` | 19 | — |
| somente_na_atual | — | `backend/schemas/signalOutput.py` | 10 | — |
| alterado | `backend/schemas/telemetry.py` | `backend/schemas/telemetry.py` | 7 | 14 |
| alterado | `backend/services/clock.py` | `backend/services/clock.py` | 4 | 4 |
| alterado | `backend/services/cncService.py` | `backend/services/cncService.py` | 60 | 21 |
| somente_na_atual | — | `backend/services/codeService.py` | 29 | — |
| alterado | `backend/services/deviceAuth.py` | `backend/services/deviceAuth.py` | 2 | 10 |
| alterado | `backend/services/deviceService.py` | `backend/services/deviceService.py` | 7 | 27 |
| somente_na_atual | — | `backend/services/eventRepository.py` | 103 | — |
| somente_na_atual | — | `backend/services/events.py` | 88 | — |
| somente_na_atual | — | `backend/services/ingestAuth.py` | 11 | — |
| somente_na_atual | — | `backend/services/machineState.py` | 48 | — |
| somente_na_atual | — | `backend/services/signalOutputs.py` | 82 | — |
| alterado | `backend/services/telemetry.py` | `backend/services/telemetry.py` | 13 | 56 |
| alterado | `backend/services/utilization.py` | `backend/services/utilization.py` | 3 | 3 |
| somente_na_atual | — | `backend/tests/testEvents.py` | 332 | — |
| alterado | `backend/tests/testMysqlConcurrency.py` | `backend/tests/testMysqlConcurrency.py` | 2 | 2 |
| alterado | `backend/tests/testOptaApi.py` | `backend/tests/testOptaApi.py` | 17 | 14 |
| somente_na_atual | — | `backend/tests/testSignalOutputs.py` | 105 | — |
| somente_na_outra | `backend/tests/testWifiFlow.py` | — | — | 171 |
| somente_na_atual | — | `configuracao.json` | 552 | — |
| alterado | `docs/guides/administracao.md` | `docs/guides/administracao.md` | 1 | 1 |
| alterado | `docs/guides/explicacaoBackendFrontend.md` | `docs/guides/explicacaoBackendFrontend.md` | 26 | 638 |
| alterado | `docs/guides/guiaEquipe.md` | `docs/guides/guiaEquipe.md` | 54 | 443 |
| alterado | `docs/guides/integracaoOpta.md` | `docs/guides/integracaoOpta.md` | 48 | 79 |
| somente_na_atual | — | `docs/guides/testesResponsividade.md` | 49 | — |
| alterado | `docs/reports/administracaoFrontendLegada.md` | `docs/reports/administracaoFrontendLegada.md` | 1 | 1 |
| somente_na_outra | `docs/reports/relatorioCompletoOpta.txt` | — | — | 739 |
| somente_na_atual | — | `docs/reports/sinaisOperacionaisCorrente.md` | 87 | — |
| somente_na_atual | — | `docs/reports/testesCncLocal.md` | 39 | — |
| somente_na_outra | `docs/reports/testesWifiLocal.md` | — | — | 72 |
| somente_na_atual | — | `examples/machine-event.json` | 11 | — |
| alterado | `firmware/archives/optaMesaMonitor.zip` | `firmware/archives/optaCncMonitor.zip` | — | — |
| alterado | `firmware/optaMesaMonitor/mesaControl.cpp` | `firmware/optaCncMonitor/cncMonitor.cpp` | 39 | 457 |
| alterado | `firmware/optaMesaMonitor/mesaControl.h` | `firmware/optaCncMonitor/cncMonitor.h` | 2 | 2 |
| alterado | `firmware/optaMesaMonitor/config.h` | `firmware/optaCncMonitor/config.h` | 23 | 3 |
| realocado_identico | `firmware/optaMesaMonitor/httpResponse.h` | `firmware/optaCncMonitor/httpResponse.h` | — | — |
| somente_na_atual | — | `firmware/optaCncMonitor/inputMonitor.h` | 29 | — |
| alterado | `firmware/optaMesaMonitor/mesaSample.json` | `firmware/optaCncMonitor/monitorSample.json` | 23 | 24 |
| somente_na_atual | — | `firmware/optaCncMonitor/optaCncMonitor.ino` | 10 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/signalProfile.h` | 15 | — |
| alterado | `firmware/optaMesaMonitor/telemetry.cpp` | `firmware/optaCncMonitor/telemetry.cpp` | 6 | 6 |
| alterado | `firmware/optaMesaMonitor/telemetry.h` | `firmware/optaCncMonitor/telemetry.h` | 1 | 1 |
| alterado | `firmware/optaMesaMonitor/telemetryCore.h` | `firmware/optaCncMonitor/telemetryCore.h` | 4 | 8 |
| alterado | `firmware/optaMesaMonitor/telemetryModel.h` | `firmware/optaCncMonitor/telemetryModel.h` | 3 | 15 |
| alterado | `firmware/optaMesaMonitor/telemetryPayload.h` | `firmware/optaCncMonitor/telemetryPayload.h` | 18 | 33 |
| somente_na_outra | `firmware/optaMesaMonitor/optaMesaMonitor.ino` | — | — | 12 |
| somente_na_outra | `firmware/reference/mesaOptaV2Original.ino` | — | — | 416 |
| alterado | `firmware/testarFirmware.ps1` | `firmware/testarFirmware.ps1` | 2 | 2 |
| alterado | `firmware/tests/host/Arduino.h` | `firmware/tests/host/Arduino.h` | 5 | 2 |
| alterado | `firmware/tests/host/testControl.cpp` | `firmware/tests/host/testControl.cpp` | 52 | 61 |
| alterado | `firmware/tests/host/testTelemetry.cpp` | `firmware/tests/host/testTelemetry.cpp` | 56 | 19 |
| alterado | `frontend/.env.example` | `frontend/.env.example` | 4 | 2 |
| alterado | `frontend/.oxlintrc.json` | `frontend/.oxlintrc.json` | 11 | 2 |
| alterado | `frontend/package.json` | `frontend/package.json` | 2 | 11 |
| alterado | `frontend/public/loginCncBackground.png` | `frontend/public/loginCncBackground.webp` | — | — |
| somente_na_atual | — | `frontend/public/loginCncBackgroundMobile.webp` | — | — |
| alterado | `frontend/src/app.jsx` | `frontend/src/app.jsx` | 63 | 45 |
| alterado | `frontend/src/components/alertCard/alertCard.jsx` | `frontend/src/components/alertCard/alertCard.jsx` | 33 | 12 |
| somente_na_atual | — | `frontend/src/components/charts/deferredHealth.jsx` | 51 | — |
| somente_na_atual | — | `frontend/src/components/charts/fleetHealth.jsx` | 15 | — |
| alterado | `frontend/src/components/charts/telemetryChart.jsx` | `frontend/src/components/charts/telemetryChart.jsx` | 173 | 40 |
| alterado | `frontend/src/components/clientCard/clientCard.jsx` | `frontend/src/components/clientCard/clientCard.jsx` | 35 | 15 |
| alterado | `frontend/src/components/mesaSignals/mesaSignals.jsx` | `frontend/src/components/cncSignals/cncSignals.jsx` | 72 | 61 |
| alterado | `frontend/src/components/contextSwitcher/contextSwitcher.jsx` | `frontend/src/components/contextSwitcher/contextSwitcher.jsx` | 90 | 78 |
| alterado | `frontend/src/components/header/header.jsx` | `frontend/src/components/header/header.jsx` | 286 | 176 |
| somente_na_atual | — | `frontend/src/components/liveTime/liveTime.jsx` | 12 | — |
| alterado | `frontend/src/components/machineCard/machineCard.jsx` | `frontend/src/components/machineCard/machineCard.jsx` | 75 | 34 |
| alterado | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | 117 | 73 |
| somente_na_atual | — | `frontend/src/components/pagination/pagination.jsx` | 37 | — |
| somente_na_atual | — | `frontend/src/components/routeBoundary/routeBoundary.jsx` | 61 | — |
| alterado | `frontend/src/components/sidebar/sidebar.jsx` | `frontend/src/components/sidebar/sidebar.jsx` | 138 | 28 |
| somente_na_atual | — | `frontend/src/components/signalOutputs/fleetSignalOutputs.jsx` | 146 | — |
| somente_na_atual | — | `frontend/src/components/signalOutputs/signalOutputList.jsx` | 56 | — |
| alterado | `frontend/src/components/toastCenter/toastCenter.jsx` | `frontend/src/components/toastCenter/toastCenter.jsx` | 12 | 5 |
| alterado | `frontend/src/contexts/monitoringContext.jsx` | `frontend/src/contexts/monitoringContext.jsx` | 364 | 182 |
| somente_na_atual | — | `frontend/src/hooks/useApiQuery.js` | 57 | — |
| somente_na_atual | — | `frontend/src/hooks/useMachineResources.js` | 85 | — |
| alterado | `frontend/src/hooks/useMachines.js` | `frontend/src/hooks/useMachines.js` | 24 | 3 |
| alterado | `frontend/src/hooks/useRelativeDuration.js` | `frontend/src/hooks/useRelativeDuration.js` | 45 | 6 |
| alterado | `frontend/src/index.css` | `frontend/src/index.css` | 92 | 15 |
| alterado | `frontend/src/layouts/dashboardLayout/dashboardLayout.jsx` | `frontend/src/layouts/dashboardLayout/dashboardLayout.jsx` | 14 | 7 |
| alterado | `frontend/src/pages/alerts/alerts.jsx` | `frontend/src/pages/alerts/alerts.jsx` | 38 | 14 |
| alterado | `frontend/src/pages/clients/clients.jsx` | `frontend/src/pages/clients/clients.jsx` | 11 | 6 |
| alterado | `frontend/src/pages/companySelection/companySelection.jsx` | `frontend/src/pages/companySelection/companySelection.jsx` | 111 | 40 |
| alterado | `frontend/src/pages/dashboard/dashboard.jsx` | `frontend/src/pages/dashboard/dashboard.jsx` | 122 | 30 |
| alterado | `frontend/src/pages/devices/devices.jsx` | `frontend/src/pages/devices/devices.jsx` | 25 | 146 |
| alterado | `frontend/src/pages/history/history.jsx` | `frontend/src/pages/history/history.jsx` | 188 | 168 |
| alterado | `frontend/src/pages/landing/landing.jsx` | `frontend/src/pages/landing/landing.jsx` | 29 | 9 |
| alterado | `frontend/src/pages/login/login.jsx` | `frontend/src/pages/login/login.jsx` | 55 | 17 |
| alterado | `frontend/src/pages/machineDetails/machineDetails.jsx` | `frontend/src/pages/machineDetails/machineDetails.jsx` | 347 | 206 |
| alterado | `frontend/src/pages/machines/machines.jsx` | `frontend/src/pages/machines/machines.jsx` | 77 | 20 |
| somente_na_atual | — | `frontend/src/pages/passwordHelp/passwordHelp.jsx` | 21 | — |
| alterado | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | 270 | 61 |
| alterado | `frontend/src/pages/units/units.jsx` | `frontend/src/pages/units/units.jsx` | 44 | 16 |
| alterado | `frontend/src/services/api.js` | `frontend/src/services/api.js` | 137 | 42 |
| somente_na_atual | — | `frontend/src/services/apiConfig.js` | 9 | — |
| somente_na_atual | — | `frontend/src/services/apiConfig.test.js` | 17 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.js` | 31 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.test.js` | 47 | — |
| alterado | `frontend/src/services/machineData.js` | `frontend/src/services/machineData.js` | 124 | 54 |
| alterado | `frontend/src/services/monitoring.js` | `frontend/src/services/monitoring.js` | 115 | 25 |
| alterado | `frontend/src/services/monitoring.test.js` | `frontend/src/services/monitoring.test.js` | 236 | 20 |
| somente_na_atual | — | `frontend/src/services/signalOutputs.js` | 61 | — |
| somente_na_atual | — | `frontend/src/services/signalOutputs.test.js` | 100 | — |
| alterado | `frontend/src/services/telemetry.js` | `frontend/src/services/telemetry.js` | 88 | 22 |
| alterado | `frontend/src/services/telemetry.test.js` | `frontend/src/services/telemetry.test.js` | 148 | 29 |
| alterado | `frontend/src/utils/status.js` | `frontend/src/utils/status.js` | 64 | 29 |
| alterado | `frontend/src/utils/time.js` | `frontend/src/utils/time.js` | 14 | 5 |
| alterado | `frontend/vite.config.js` | `frontend/vite.config.js` | 9 | 8 |
| alterado | `iniciarLocal.ps1` | `iniciarLocal.ps1` | 7 | 6 |
| somente_na_atual | — | `Main.pdf` | — | — |
| alterado | `README.md` | `README.md` | 523 | 129 |
| alterado | `tools/configurarRede.ps1` | `tools/configurarRede.ps1` | 1 | 1 |
| alterado | `tools/configurarTransmissao.py` | `tools/configurarTransmissao.py` | 8 | 2 |
| alterado | `tools/ponteUsb.py` | `tools/ponteUsb.py` | 59 | 42 |
| somente_na_atual | — | `tools/publicarEventos.py` | 42 | — |
| somente_na_atual | — | `tools/simuladorCnc.py` | 53 | — |
| somente_na_outra | `tools/simuladorWifi.py` | — | — | 260 |
| somente_na_atual | — | `tools/testarFrontend.py` | 200 | — |
| alterado | `tools/testarOpta.ps1` | `tools/testarOpta.ps1` | 3 | 3 |
| alterado | `tools/testarProjeto.ps1` | `tools/testarProjeto.ps1` | 3 | 1 |
| alterado | `tools/tests/testConfigurarTransmissao.py` | `tools/tests/testConfigurarTransmissao.py` | 27 | 1 |
| somente_na_atual | — | `tools/tests/testEventTools.py` | 111 | — |
| alterado | `tools/tests/testPonteUsb.py` | `tools/tests/testPonteUsb.py` | 67 | 18 |

## ZIP_ULTRON — ZIP UltronScomptec-main

Origem: `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main.zip`

Contagens: `{"identico": 148, "alterado": 39, "somente_na_atual": 11}`

| Estado | Caminho na outra cópia | Caminho na atual | + linhas | − linhas |
|---|---|---|---:|---:|
| alterado | `backend/schemas/cnc.py` | `backend/schemas/cnc.py` | 11 | 0 |
| alterado | `backend/schemas/event.py` | `backend/schemas/event.py` | 13 | 1 |
| somente_na_atual | — | `backend/schemas/signalOutput.py` | 10 | — |
| alterado | `backend/schemas/telemetry.py` | `backend/schemas/telemetry.py` | 3 | 1 |
| alterado | `backend/services/cncService.py` | `backend/services/cncService.py` | 6 | 0 |
| alterado | `backend/services/events.py` | `backend/services/events.py` | 3 | 2 |
| alterado | `backend/services/machineState.py` | `backend/services/machineState.py` | 32 | 1 |
| somente_na_atual | — | `backend/services/signalOutputs.py` | 82 | — |
| alterado | `backend/tests/testEvents.py` | `backend/tests/testEvents.py` | 92 | 0 |
| somente_na_atual | — | `backend/tests/testSignalOutputs.py` | 105 | — |
| alterado | `docs/guides/explicacaoBackendFrontend.md` | `docs/guides/explicacaoBackendFrontend.md` | 1 | 1 |
| alterado | `docs/guides/guiaEquipe.md` | `docs/guides/guiaEquipe.md` | 10 | 2 |
| alterado | `docs/guides/integracaoOpta.md` | `docs/guides/integracaoOpta.md` | 14 | 10 |
| somente_na_atual | — | `docs/reports/sinaisOperacionaisCorrente.md` | 87 | — |
| alterado | `examples/machine-event.json` | `examples/machine-event.json` | 4 | 6 |
| alterado | `firmware/optaCncMonitor/cncMonitor.cpp` | `firmware/optaCncMonitor/cncMonitor.cpp` | 4 | 3 |
| alterado | `firmware/optaCncMonitor/config.h` | `firmware/optaCncMonitor/config.h` | 5 | 5 |
| alterado | `firmware/optaCncMonitor/monitorSample.json` | `firmware/optaCncMonitor/monitorSample.json` | 14 | 21 |
| somente_na_atual | — | `firmware/optaCncMonitor/signalProfile.h` | 15 | — |
| alterado | `firmware/optaCncMonitor/telemetryModel.h` | `firmware/optaCncMonitor/telemetryModel.h` | 1 | 1 |
| alterado | `firmware/optaCncMonitor/telemetryPayload.h` | `firmware/optaCncMonitor/telemetryPayload.h` | 12 | 9 |
| alterado | `firmware/tests/host/testControl.cpp` | `firmware/tests/host/testControl.cpp` | 8 | 5 |
| alterado | `firmware/tests/host/testTelemetry.cpp` | `firmware/tests/host/testTelemetry.cpp` | 12 | 11 |
| alterado | `frontend/src/components/alertCard/alertCard.jsx` | `frontend/src/components/alertCard/alertCard.jsx` | 10 | 0 |
| alterado | `frontend/src/components/charts/telemetryChart.jsx` | `frontend/src/components/charts/telemetryChart.jsx` | 7 | 1 |
| alterado | `frontend/src/components/cncSignals/cncSignals.jsx` | `frontend/src/components/cncSignals/cncSignals.jsx` | 74 | 22 |
| alterado | `frontend/src/components/machineCard/machineCard.jsx` | `frontend/src/components/machineCard/machineCard.jsx` | 6 | 0 |
| alterado | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | 4 | 0 |
| somente_na_atual | — | `frontend/src/components/signalOutputs/fleetSignalOutputs.jsx` | 146 | — |
| somente_na_atual | — | `frontend/src/components/signalOutputs/signalOutputList.jsx` | 56 | — |
| alterado | `frontend/src/contexts/monitoringContext.jsx` | `frontend/src/contexts/monitoringContext.jsx` | 3 | 1 |
| alterado | `frontend/src/pages/dashboard/dashboard.jsx` | `frontend/src/pages/dashboard/dashboard.jsx` | 7 | 0 |
| alterado | `frontend/src/pages/history/history.jsx` | `frontend/src/pages/history/history.jsx` | 6 | 0 |
| alterado | `frontend/src/pages/machineDetails/machineDetails.jsx` | `frontend/src/pages/machineDetails/machineDetails.jsx` | 5 | 3 |
| alterado | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | 2 | 0 |
| alterado | `frontend/src/services/cncSignals.js` | `frontend/src/services/cncSignals.js` | 22 | 8 |
| somente_na_atual | — | `frontend/src/services/cncSignals.test.js` | 47 | — |
| alterado | `frontend/src/services/machineData.js` | `frontend/src/services/machineData.js` | 6 | 0 |
| alterado | `frontend/src/services/monitoring.js` | `frontend/src/services/monitoring.js` | 115 | 25 |
| alterado | `frontend/src/services/monitoring.test.js` | `frontend/src/services/monitoring.test.js` | 108 | 0 |
| somente_na_atual | — | `frontend/src/services/signalOutputs.js` | 61 | — |
| somente_na_atual | — | `frontend/src/services/signalOutputs.test.js` | 100 | — |
| alterado | `frontend/src/services/telemetry.js` | `frontend/src/services/telemetry.js` | 4 | 6 |
| somente_na_atual | — | `Main.pdf` | — | — |
| alterado | `README.md` | `README.md` | 277 | 147 |
| alterado | `tools/ponteUsb.py` | `tools/ponteUsb.py` | 6 | 0 |
| alterado | `tools/simuladorCnc.py` | `tools/simuladorCnc.py` | 16 | 6 |
| alterado | `tools/testarFrontend.py` | `tools/testarFrontend.py` | 24 | 2 |
| alterado | `tools/tests/testEventTools.py` | `tools/tests/testEventTools.py` | 30 | 3 |
| alterado | `tools/tests/testPonteUsb.py` | `tools/tests/testPonteUsb.py` | 19 | 5 |

## ZIP_MEXER — ZIP VERSÃO/ VERSÃOPRAMEXER

Origem: `C:\Users\pedro\OneDrive\Desktop\VERSÃOPRAMEXER.zip`

Contagens: `{"identico": 198}`

| Estado | Caminho na outra cópia | Caminho na atual | + linhas | − linhas |
|---|---|---|---:|---:|

## ZIP_TCC — ZIP ScompTecTCC-main

Origem: `C:\Users\pedro\Downloads\ScompTecTCC-main.zip`

Contagens: `{"alterado": 97, "somente_na_atual": 62, "realocado_identico": 39, "somente_na_outra": 11}`

| Estado | Caminho na outra cópia | Caminho na atual | + linhas | − linhas |
|---|---|---|---:|---:|
| alterado | `.gitignore` | `.gitignore` | 41 | 8 |
| alterado | `SCOMPTEC- Back/.env.example` | `backend/.env.example` | 50 | 9 |
| somente_na_atual | — | `backend/config.example.json` | 14 | — |
| alterado | `SCOMPTEC- Back/config.py` | `backend/config.py` | 37 | 2 |
| alterado | `SCOMPTEC- Back/create_admin.py` | `backend/createAdmin.py` | 4 | 4 |
| realocado_identico | `SCOMPTEC- Back/data/seed.test.json` | `backend/data/seed.test.json` | — | — |
| alterado | `SCOMPTEC- Back/Database/Connection.py` | `backend/database/connection.py` | 42 | 3 |
| realocado_identico | `SCOMPTEC- Back/Database/migrations/001_device_network_fields.sql` | `backend/database/migrations/001_deviceNetworkFields.sql` | — | — |
| alterado | `SCOMPTEC- Back/Database/models.py` | `backend/database/models.py` | 34 | 1 |
| alterado | `SCOMPTEC- Back/Main.py` | `backend/main.py` | 9 | 8 |
| alterado | `SCOMPTEC- Back/Schema/admin.py` | `backend/schemas/admin.py` | 1 | 1 |
| realocado_identico | `SCOMPTEC- Back/Schema/auth.py` | `backend/schemas/auth.py` | — | — |
| alterado | `SCOMPTEC- Back/Schema/cnc.py` | `backend/schemas/cnc.py` | 16 | 2 |
| realocado_identico | `SCOMPTEC- Back/Schema/common.py` | `backend/schemas/common.py` | — | — |
| alterado | `SCOMPTEC- Back/Schema/device.py` | `backend/schemas/device.py` | 1 | 1 |
| somente_na_atual | — | `backend/schemas/event.py` | 33 | — |
| somente_na_atual | — | `backend/schemas/observation.py` | 19 | — |
| somente_na_atual | — | `backend/schemas/signalOutput.py` | 10 | — |
| alterado | `SCOMPTEC- Back/Schema/telemetry.py` | `backend/schemas/telemetry.py` | 8 | 15 |
| alterado | `SCOMPTEC- Back/Services/admin_bootstrap.py` | `backend/services/adminBootstrap.py` | 3 | 3 |
| alterado | `SCOMPTEC- Back/Services/adminservice.py` | `backend/services/adminService.py` | 5 | 5 |
| alterado | `SCOMPTEC- Back/Services/authservice.py` | `backend/services/authService.py` | 4 | 4 |
| alterado | `SCOMPTEC- Back/Services/clock.py` | `backend/services/clock.py` | 10 | 4 |
| alterado | `SCOMPTEC- Back/Services/cncservice.py` | `backend/services/cncService.py` | 68 | 29 |
| somente_na_atual | — | `backend/services/codeService.py` | 29 | — |
| alterado | `SCOMPTEC- Back/Services/device_auth.py` | `backend/services/deviceAuth.py` | 2 | 10 |
| alterado | `SCOMPTEC- Back/Services/deviceservice.py` | `backend/services/deviceService.py` | 11 | 31 |
| somente_na_atual | — | `backend/services/eventRepository.py` | 103 | — |
| somente_na_atual | — | `backend/services/events.py` | 88 | — |
| somente_na_atual | — | `backend/services/ingestAuth.py` | 11 | — |
| somente_na_atual | — | `backend/services/machineState.py` | 48 | — |
| realocado_identico | `SCOMPTEC- Back/Services/security.py` | `backend/services/security.py` | — | — |
| somente_na_atual | — | `backend/services/signalOutputs.py` | 82 | — |
| alterado | `SCOMPTEC- Back/Services/telemetry.py` | `backend/services/telemetry.py` | 18 | 54 |
| alterado | `SCOMPTEC- Back/Services/utilization.py` | `backend/services/utilization.py` | 4 | 4 |
| alterado | `SCOMPTEC- Back/tests/test_admin.py` | `backend/tests/testAdmin.py` | 6 | 6 |
| somente_na_atual | — | `backend/tests/testDatabaseBootstrap.py` | 70 | — |
| alterado | `SCOMPTEC- Back/tests/test_device_provisioning.py` | `backend/tests/testDeviceProvisioning.py` | 3 | 3 |
| somente_na_atual | — | `backend/tests/testEvents.py` | 332 | — |
| somente_na_atual | — | `backend/tests/testMysqlConcurrency.py` | 108 | — |
| alterado | `SCOMPTEC- Back/tests/test_opta_api.py` | `backend/tests/testOptaApi.py` | 23 | 20 |
| somente_na_atual | — | `backend/tests/testSignalOutputs.py` | 105 | — |
| somente_na_atual | — | `backend/tests/testSimulationConfig.py` | 58 | — |
| somente_na_atual | — | `configuracao.json` | 552 | — |
| alterado | `docs/ADMINISTRACAO.md` | `docs/guides/administracao.md` | 6 | 5 |
| alterado | `docs/explicacao_backend_frontend.md` | `docs/guides/explicacaoBackendFrontend.md` | 26 | 636 |
| alterado | `docs/GUIA_EQUIPE.md` | `docs/guides/guiaEquipe.md` | 54 | 441 |
| alterado | `INTEGRACAO_OPTA.md` | `docs/guides/integracaoOpta.md` | 46 | 162 |
| somente_na_atual | — | `docs/guides/testesResponsividade.md` | 49 | — |
| realocado_identico | `docs/SCOMPTEC_Explicacao_Backend_e_Frontend.docx` | `docs/reference/explicacaoBackendFrontend.docx` | — | — |
| realocado_identico | `docs/openapi.json` | `docs/reference/openapi.json` | — | — |
| somente_na_outra | `docs/RELATORIO_COMPLETO_OPTA.txt` | — | — | 737 |
| alterado | `scomptec-cnc front 2/ADMINISTRACAO.md` | `docs/reports/administracaoFrontendLegada.md` | 4 | 2 |
| alterado | `IMPLEMENTATION_REPORT.md` | `docs/reports/implementationReport.md` | 10 | 8 |
| somente_na_atual | — | `docs/reports/sinaisOperacionaisCorrente.md` | 87 | — |
| somente_na_atual | — | `docs/reports/testesCncLocal.md` | 39 | — |
| somente_na_atual | — | `examples/machine-event.json` | 11 | — |
| alterado | `firmware/opta_mesa_monitor.zip` | `firmware/archives/optaCncMonitor.zip` | — | — |
| somente_na_outra | `firmware/esp32_cnc_monitor/README.md` | — | — | 28 |
| realocado_identico | `firmware/esp32_cnc_monitor/esp32_cnc_monitor.ino` | `firmware/legacy/esp32CncMonitor/esp32CncMonitor.ino` | — | — |
| realocado_identico | `firmware/esp32_cnc_monitor/platformio.ini` | `firmware/legacy/esp32CncMonitor/platformio.ini` | — | — |
| somente_na_outra | `firmware/opta_mesa_monitor/opta_secrets.example.h` | — | — | 10 |
| somente_na_outra | `firmware/opta_mesa_monitor/README.md` | — | — | 109 |
| alterado | `firmware/opta_mesa_monitor/MesaControl.cpp` | `firmware/optaCncMonitor/cncMonitor.cpp` | 42 | 417 |
| alterado | `firmware/opta_mesa_monitor/MesaControl.h` | `firmware/optaCncMonitor/cncMonitor.h` | 2 | 2 |
| alterado | `firmware/opta_mesa_monitor/Config.h` | `firmware/optaCncMonitor/config.h` | 70 | 12 |
| somente_na_atual | — | `firmware/optaCncMonitor/httpResponse.h` | 80 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/inputMonitor.h` | 29 | — |
| alterado | `firmware/opta_mesa_monitor/mesa_sample.json` | `firmware/optaCncMonitor/monitorSample.json` | 23 | 24 |
| alterado | `firmware/opta_mesa_monitor/opta_mesa_monitor.ino` | `firmware/optaCncMonitor/optaCncMonitor.ino` | 5 | 6 |
| somente_na_atual | — | `firmware/optaCncMonitor/signalProfile.h` | 15 | — |
| alterado | `firmware/opta_mesa_monitor/Telemetry.cpp` | `firmware/optaCncMonitor/telemetry.cpp` | 145 | 240 |
| alterado | `firmware/opta_mesa_monitor/Telemetry.h` | `firmware/optaCncMonitor/telemetry.h` | 2 | 24 |
| somente_na_atual | — | `firmware/optaCncMonitor/telemetryCore.h` | 151 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/telemetryModel.h` | 10 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/telemetryPayload.h` | 82 | — |
| somente_na_outra | `firmware/reference/mesa_opta_v2_original.ino` | — | — | 416 |
| somente_na_atual | — | `firmware/testarFirmware.ps1` | 66 | — |
| somente_na_atual | — | `firmware/tests/host/Arduino.h` | 37 | — |
| somente_na_atual | — | `firmware/tests/host/testControl.cpp` | 63 | — |
| somente_na_atual | — | `firmware/tests/host/testTelemetry.cpp` | 181 | — |
| alterado | `scomptec-cnc front 2/.env.example` | `frontend/.env.example` | 4 | 2 |
| alterado | `scomptec-cnc front 2/.oxlintrc.json` | `frontend/.oxlintrc.json` | 11 | 2 |
| alterado | `scomptec-cnc front 2/electron/main.js` | `frontend/electron/legacy/main.js` | 1 | 1 |
| alterado | `scomptec-cnc front 2/electron/main.cjs` | `frontend/electron/main.cjs` | 34 | 5 |
| alterado | `scomptec-cnc front 2/index.html` | `frontend/index.html` | 1 | 1 |
| alterado | `scomptec-cnc front 2/package-lock.json` | `frontend/package-lock.json` | 244 | 215 |
| alterado | `scomptec-cnc front 2/package.json` | `frontend/package.json` | 3 | 11 |
| realocado_identico | `scomptec-cnc front 2/postcss.config.js` | `frontend/postcss.config.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/favicon.svg` | `frontend/public/favicon.svg` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/icons.svg` | `frontend/public/icons.svg` | — | — |
| alterado | `scomptec-cnc front 2/public/login-cnc-background.png` | `frontend/public/loginCncBackground.webp` | — | — |
| somente_na_atual | — | `frontend/public/loginCncBackgroundMobile.webp` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/scomptec-icon.svg` | `frontend/public/scomptecIcon.svg` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/scomptec-logo.webp` | `frontend/public/scomptecLogo.webp` | — | — |
| alterado | `scomptec-cnc front 2/src/App.jsx` | `frontend/src/app.jsx` | 64 | 46 |
| realocado_identico | `scomptec-cnc front 2/src/assets/hero.png` | `frontend/src/assets/hero.png` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/assets/vite.svg` | `frontend/src/assets/vite.svg` | — | — |
| alterado | `scomptec-cnc front 2/src/components/AlertCard/AlertCard.jsx` | `frontend/src/components/alertCard/alertCard.jsx` | 33 | 11 |
| alterado | `scomptec-cnc front 2/src/components/Breadcrumb/Breadcrumb.jsx` | `frontend/src/components/breadcrumb/breadcrumb.jsx` | 1 | 1 |
| somente_na_atual | — | `frontend/src/components/charts/deferredHealth.jsx` | 51 | — |
| somente_na_atual | — | `frontend/src/components/charts/fleetHealth.jsx` | 15 | — |
| alterado | `scomptec-cnc front 2/src/components/charts/TelemetryChart.jsx` | `frontend/src/components/charts/telemetryChart.jsx` | 178 | 40 |
| alterado | `scomptec-cnc front 2/src/components/charts/UtilizationChart.jsx` | `frontend/src/components/charts/utilizationChart.jsx` | 7 | 5 |
| alterado | `scomptec-cnc front 2/src/components/ClientCard/ClientCard.jsx` | `frontend/src/components/clientCard/clientCard.jsx` | 37 | 17 |
| alterado | `scomptec-cnc front 2/src/components/MesaSignals/MesaSignals.jsx` | `frontend/src/components/cncSignals/cncSignals.jsx` | 72 | 61 |
| alterado | `scomptec-cnc front 2/src/components/ConnectionNotice/ConnectionNotice.jsx` | `frontend/src/components/connectionNotice/connectionNotice.jsx` | 5 | 5 |
| alterado | `scomptec-cnc front 2/src/components/ContextSwitcher/ContextSwitcher.jsx` | `frontend/src/components/contextSwitcher/contextSwitcher.jsx` | 92 | 80 |
| realocado_identico | `scomptec-cnc front 2/src/components/EmptyState/EmptyState.jsx` | `frontend/src/components/emptyState/emptyState.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/Header/Header.jsx` | `frontend/src/components/header/header.jsx` | 290 | 173 |
| somente_na_atual | — | `frontend/src/components/liveTime/liveTime.jsx` | 12 | — |
| realocado_identico | `scomptec-cnc front 2/src/components/LoadingState/LoadingState.jsx` | `frontend/src/components/loadingState/loadingState.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/Logo/Logo.jsx` | `frontend/src/components/logo/logo.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/components/MachineCard/MachineCard.jsx` | `frontend/src/components/machineCard/machineCard.jsx` | 76 | 35 |
| realocado_identico | `scomptec-cnc front 2/src/components/MachineIncidents/MachineIncidents.jsx` | `frontend/src/components/machineIncidents/machineIncidents.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/OccurrenceCard/OccurrenceCard.jsx` | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | 118 | 73 |
| realocado_identico | `scomptec-cnc front 2/src/components/OperatingTimeline/OperatingTimeline.jsx` | `frontend/src/components/operatingTimeline/operatingTimeline.jsx` | — | — |
| somente_na_atual | — | `frontend/src/components/pagination/pagination.jsx` | 37 | — |
| somente_na_atual | — | `frontend/src/components/routeBoundary/routeBoundary.jsx` | 61 | — |
| alterado | `scomptec-cnc front 2/src/components/Sidebar/Sidebar.jsx` | `frontend/src/components/sidebar/sidebar.jsx` | 141 | 31 |
| somente_na_atual | — | `frontend/src/components/signalOutputs/fleetSignalOutputs.jsx` | 146 | — |
| somente_na_atual | — | `frontend/src/components/signalOutputs/signalOutputList.jsx` | 56 | — |
| realocado_identico | `scomptec-cnc front 2/src/components/StatCard/StatCard.jsx` | `frontend/src/components/statCard/statCard.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/components/StatusBadge/StatusBadge.jsx` | `frontend/src/components/statusBadge/statusBadge.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/ToastCenter/ToastCenter.jsx` | `frontend/src/components/toastCenter/toastCenter.jsx` | 12 | 5 |
| alterado | `scomptec-cnc front 2/src/contexts/MonitoringContext.jsx` | `frontend/src/contexts/monitoringContext.jsx` | 370 | 174 |
| realocado_identico | `scomptec-cnc front 2/src/data/mockData.js` | `frontend/src/data/mockData.js` | — | — |
| alterado | `scomptec-cnc front 2/src/hooks/useAlerts.js` | `frontend/src/hooks/useAlerts.js` | 2 | 2 |
| somente_na_atual | — | `frontend/src/hooks/useApiQuery.js` | 57 | — |
| somente_na_atual | — | `frontend/src/hooks/useMachineResources.js` | 85 | — |
| alterado | `scomptec-cnc front 2/src/hooks/useMachines.js` | `frontend/src/hooks/useMachines.js` | 25 | 4 |
| alterado | `scomptec-cnc front 2/src/hooks/useRelativeDuration.js` | `frontend/src/hooks/useRelativeDuration.js` | 45 | 6 |
| alterado | `scomptec-cnc front 2/src/index.css` | `frontend/src/index.css` | 187 | 11 |
| alterado | `scomptec-cnc front 2/src/layouts/DashboardLayout/DashboardLayout.jsx` | `frontend/src/layouts/dashboardLayout/dashboardLayout.jsx` | 19 | 12 |
| alterado | `scomptec-cnc front 2/src/layouts/TVLayout/TVLayout.jsx` | `frontend/src/layouts/tvLayout/tvLayout.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/main.jsx` | `frontend/src/main.jsx` | 3 | 3 |
| alterado | `scomptec-cnc front 2/src/pages/Admin/admin.css` | `frontend/src/pages/admin/admin.css` | 19 | 0 |
| alterado | `scomptec-cnc front 2/src/pages/Admin/Admin.jsx` | `frontend/src/pages/admin/admin.jsx` | 3 | 3 |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminAccess.jsx` | `frontend/src/pages/admin/adminAccess.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminActivity.jsx` | `frontend/src/pages/admin/adminActivity.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/adminModel.js` | `frontend/src/pages/admin/adminModel.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/adminModel.test.js` | `frontend/src/pages/admin/adminModel.test.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminUserRow.jsx` | `frontend/src/pages/admin/adminUserRow.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/pages/Alerts/Alerts.jsx` | `frontend/src/pages/alerts/alerts.jsx` | 44 | 20 |
| alterado | `scomptec-cnc front 2/src/pages/Clients/Clients.jsx` | `frontend/src/pages/clients/clients.jsx` | 12 | 7 |
| alterado | `scomptec-cnc front 2/src/pages/CompanySelection/CompanySelection.jsx` | `frontend/src/pages/companySelection/companySelection.jsx` | 115 | 44 |
| alterado | `scomptec-cnc front 2/src/pages/Dashboard/Dashboard.jsx` | `frontend/src/pages/dashboard/dashboard.jsx` | 137 | 44 |
| alterado | `scomptec-cnc front 2/src/pages/Devices/Devices.jsx` | `frontend/src/pages/devices/devices.jsx` | 25 | 146 |
| alterado | `scomptec-cnc front 2/src/pages/History/History.jsx` | `frontend/src/pages/history/history.jsx` | 191 | 171 |
| alterado | `scomptec-cnc front 2/src/pages/Landing/Landing.jsx` | `frontend/src/pages/landing/landing.jsx` | 30 | 10 |
| alterado | `scomptec-cnc front 2/src/pages/Login/Login.jsx` | `frontend/src/pages/login/login.jsx` | 56 | 18 |
| alterado | `scomptec-cnc front 2/src/pages/MachineDetails/MachineDetails.jsx` | `frontend/src/pages/machineDetails/machineDetails.jsx` | 356 | 214 |
| alterado | `scomptec-cnc front 2/src/pages/Machines/Machines.jsx` | `frontend/src/pages/machines/machines.jsx` | 80 | 23 |
| somente_na_atual | — | `frontend/src/pages/passwordHelp/passwordHelp.jsx` | 21 | — |
| alterado | `scomptec-cnc front 2/src/pages/Register/Register.jsx` | `frontend/src/pages/register/register.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/pages/Settings/Settings.jsx` | `frontend/src/pages/settings/settings.jsx` | 11 | 0 |
| alterado | `scomptec-cnc front 2/src/pages/Splash/Splash.jsx` | `frontend/src/pages/splash/splash.jsx` | 1 | 1 |
| realocado_identico | `scomptec-cnc front 2/src/pages/TVDashboard/tv.css` | `frontend/src/pages/tvDashboard/tv.css` | — | — |
| alterado | `scomptec-cnc front 2/src/pages/TVDashboard/TVDashboard.jsx` | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | 272 | 62 |
| alterado | `scomptec-cnc front 2/src/pages/Units/Units.jsx` | `frontend/src/pages/units/units.jsx` | 45 | 17 |
| realocado_identico | `scomptec-cnc front 2/src/services/adminSession.js` | `frontend/src/services/adminSession.js` | — | — |
| alterado | `scomptec-cnc front 2/src/services/api.js` | `frontend/src/services/api.js` | 140 | 90 |
| somente_na_atual | — | `frontend/src/services/apiConfig.js` | 9 | — |
| somente_na_atual | — | `frontend/src/services/apiConfig.test.js` | 17 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.js` | 31 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.test.js` | 47 | — |
| realocado_identico | `scomptec-cnc front 2/src/services/eventBus.js` | `frontend/src/services/eventBus.js` | — | — |
| somente_na_atual | — | `frontend/src/services/machineData.js` | 130 | — |
| somente_na_atual | — | `frontend/src/services/monitoring.js` | 132 | — |
| somente_na_atual | — | `frontend/src/services/monitoring.test.js` | 338 | — |
| alterado | `scomptec-cnc front 2/src/services/preferences.js` | `frontend/src/services/preferences.js` | 3 | 1 |
| somente_na_atual | — | `frontend/src/services/signalOutputs.js` | 61 | — |
| somente_na_atual | — | `frontend/src/services/signalOutputs.test.js` | 100 | — |
| alterado | `scomptec-cnc front 2/src/services/telemetry.js` | `frontend/src/services/telemetry.js` | 87 | 21 |
| alterado | `scomptec-cnc front 2/src/services/telemetry.test.js` | `frontend/src/services/telemetry.test.js` | 148 | 29 |
| realocado_identico | `scomptec-cnc front 2/src/services/utilization.js` | `frontend/src/services/utilization.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/services/utilization.test.js` | `frontend/src/services/utilization.test.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/services/websocket.js` | `frontend/src/services/websocket.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/utils/problems.js` | `frontend/src/utils/problems.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/utils/severity.js` | `frontend/src/utils/severity.js` | — | — |
| alterado | `scomptec-cnc front 2/src/utils/status.js` | `frontend/src/utils/status.js` | 66 | 31 |
| alterado | `scomptec-cnc front 2/src/utils/time.js` | `frontend/src/utils/time.js` | 14 | 5 |
| alterado | `scomptec-cnc front 2/tailwind.config.js` | `frontend/tailwind.config.js` | 20 | 20 |
| alterado | `scomptec-cnc front 2/vite.config.js` | `frontend/vite.config.js` | 10 | 9 |
| somente_na_outra | `iniciar.cmd` | — | — | 68 |
| somente_na_atual | — | `iniciarLocal.ps1` | 169 | — |
| realocado_identico | `tests/conftest.py` | `legacy/mongodb/tests/conftest.py` | — | — |
| realocado_identico | `tests/test_endpoints.py` | `legacy/mongodb/tests/testEndpoints.py` | — | — |
| realocado_identico | `tests/test_services.py` | `legacy/mongodb/tests/testServices.py` | — | — |
| somente_na_atual | — | `Main.pdf` | — | — |
| alterado | `pytest.ini` | `pytest.ini` | 2 | 1 |
| alterado | `README.md` | `README.md` | 554 | 31 |
| alterado | `requirements.txt` | `requirements.txt` | 21 | 9 |
| somente_na_outra | `SCOMPTEC- Back/README.md` | — | — | 31 |
| somente_na_outra | `SCOMPTEC- Back/requirements-dev.txt` | — | — | 3 |
| somente_na_outra | `SCOMPTEC- Back/requirements.txt` | — | — | 6 |
| somente_na_outra | `scomptec-cnc front 2/.gitignore` | — | — | 4 |
| somente_na_outra | `scomptec-cnc front 2/README.md` | — | — | 82 |
| somente_na_atual | — | `tools/configurarRede.ps1` | 39 | — |
| somente_na_atual | — | `tools/configurarTransmissao.py` | 78 | — |
| somente_na_atual | — | `tools/ponteUsb.py` | 277 | — |
| somente_na_atual | — | `tools/publicarEventos.py` | 42 | — |
| somente_na_atual | — | `tools/simuladorCnc.py` | 53 | — |
| somente_na_atual | — | `tools/testarFrontend.py` | 200 | — |
| alterado | `docs/testar-opta.ps1` | `tools/testarOpta.ps1` | 3 | 3 |
| somente_na_atual | — | `tools/testarProjeto.ps1` | 123 | — |
| somente_na_atual | — | `tools/tests/testConfigurarTransmissao.py` | 115 | — |
| somente_na_atual | — | `tools/tests/testEventTools.py` | 111 | — |
| somente_na_atual | — | `tools/tests/testPonteUsb.py` | 259 | — |

## ZIP_V3 — ZIP SCOMPTECV3 de 20261021

Origem: `C:\Users\pedro\OneDrive\Desktop\BeeGuardDataset\ALERT\SCOMPTECV3-20261021T215457Z-1-001.zip`

Contagens: `{"alterado": 98, "somente_na_atual": 60, "realocado_identico": 40, "somente_na_outra": 11}`

| Estado | Caminho na outra cópia | Caminho na atual | + linhas | − linhas |
|---|---|---|---:|---:|
| alterado | `.gitignore` | `.gitignore` | 41 | 8 |
| alterado | `SCOMPTEC- Back/.env.example` | `backend/.env.example` | 7 | 0 |
| somente_na_atual | — | `backend/config.example.json` | 14 | — |
| alterado | `SCOMPTEC- Back/config.py` | `backend/config.py` | 37 | 2 |
| alterado | `SCOMPTEC- Back/create_admin.py` | `backend/createAdmin.py` | 4 | 4 |
| realocado_identico | `SCOMPTEC- Back/data/seed.test.json` | `backend/data/seed.test.json` | — | — |
| alterado | `SCOMPTEC- Back/Database/Connection.py` | `backend/database/connection.py` | 42 | 3 |
| realocado_identico | `SCOMPTEC- Back/Database/migrations/001_device_network_fields.sql` | `backend/database/migrations/001_deviceNetworkFields.sql` | — | — |
| alterado | `SCOMPTEC- Back/Database/models.py` | `backend/database/models.py` | 34 | 1 |
| alterado | `SCOMPTEC- Back/Main.py` | `backend/main.py` | 8 | 7 |
| alterado | `SCOMPTEC- Back/Schema/admin.py` | `backend/schemas/admin.py` | 1 | 1 |
| realocado_identico | `SCOMPTEC- Back/Schema/auth.py` | `backend/schemas/auth.py` | — | — |
| alterado | `SCOMPTEC- Back/Schema/cnc.py` | `backend/schemas/cnc.py` | 16 | 2 |
| realocado_identico | `SCOMPTEC- Back/Schema/common.py` | `backend/schemas/common.py` | — | — |
| alterado | `SCOMPTEC- Back/Schema/device.py` | `backend/schemas/device.py` | 1 | 1 |
| somente_na_atual | — | `backend/schemas/event.py` | 33 | — |
| somente_na_atual | — | `backend/schemas/observation.py` | 19 | — |
| somente_na_atual | — | `backend/schemas/signalOutput.py` | 10 | — |
| alterado | `SCOMPTEC- Back/Schema/telemetry.py` | `backend/schemas/telemetry.py` | 8 | 15 |
| alterado | `SCOMPTEC- Back/Services/admin_bootstrap.py` | `backend/services/adminBootstrap.py` | 3 | 3 |
| alterado | `SCOMPTEC- Back/Services/adminservice.py` | `backend/services/adminService.py` | 5 | 5 |
| alterado | `SCOMPTEC- Back/Services/authservice.py` | `backend/services/authService.py` | 4 | 4 |
| alterado | `SCOMPTEC- Back/Services/clock.py` | `backend/services/clock.py` | 10 | 4 |
| alterado | `SCOMPTEC- Back/Services/cncservice.py` | `backend/services/cncService.py` | 68 | 29 |
| somente_na_atual | — | `backend/services/codeService.py` | 29 | — |
| alterado | `SCOMPTEC- Back/Services/device_auth.py` | `backend/services/deviceAuth.py` | 2 | 10 |
| alterado | `SCOMPTEC- Back/Services/deviceservice.py` | `backend/services/deviceService.py` | 11 | 31 |
| somente_na_atual | — | `backend/services/eventRepository.py` | 103 | — |
| somente_na_atual | — | `backend/services/events.py` | 88 | — |
| somente_na_atual | — | `backend/services/ingestAuth.py` | 11 | — |
| somente_na_atual | — | `backend/services/machineState.py` | 48 | — |
| realocado_identico | `SCOMPTEC- Back/Services/security.py` | `backend/services/security.py` | — | — |
| somente_na_atual | — | `backend/services/signalOutputs.py` | 82 | — |
| alterado | `SCOMPTEC- Back/Services/telemetry.py` | `backend/services/telemetry.py` | 18 | 54 |
| alterado | `SCOMPTEC- Back/Services/utilization.py` | `backend/services/utilization.py` | 4 | 4 |
| alterado | `SCOMPTEC- Back/tests/test_admin.py` | `backend/tests/testAdmin.py` | 6 | 6 |
| somente_na_atual | — | `backend/tests/testDatabaseBootstrap.py` | 70 | — |
| alterado | `SCOMPTEC- Back/tests/test_device_provisioning.py` | `backend/tests/testDeviceProvisioning.py` | 3 | 3 |
| somente_na_atual | — | `backend/tests/testEvents.py` | 332 | — |
| somente_na_atual | — | `backend/tests/testMysqlConcurrency.py` | 108 | — |
| alterado | `SCOMPTEC- Back/tests/test_opta_api.py` | `backend/tests/testOptaApi.py` | 23 | 20 |
| somente_na_atual | — | `backend/tests/testSignalOutputs.py` | 105 | — |
| somente_na_atual | — | `backend/tests/testSimulationConfig.py` | 58 | — |
| somente_na_atual | — | `configuracao.json` | 552 | — |
| alterado | `docs/ADMINISTRACAO.md` | `docs/guides/administracao.md` | 6 | 5 |
| alterado | `docs/explicacao_backend_frontend.md` | `docs/guides/explicacaoBackendFrontend.md` | 26 | 636 |
| alterado | `docs/GUIA_EQUIPE.md` | `docs/guides/guiaEquipe.md` | 54 | 441 |
| alterado | `INTEGRACAO_OPTA.md` | `docs/guides/integracaoOpta.md` | 48 | 115 |
| somente_na_atual | — | `docs/guides/testesResponsividade.md` | 49 | — |
| realocado_identico | `docs/SCOMPTEC_Explicacao_Backend_e_Frontend.docx` | `docs/reference/explicacaoBackendFrontend.docx` | — | — |
| realocado_identico | `docs/openapi.json` | `docs/reference/openapi.json` | — | — |
| somente_na_outra | `docs/RELATORIO_COMPLETO_OPTA.txt` | — | — | 737 |
| alterado | `scomptec-cnc front 2/ADMINISTRACAO.md` | `docs/reports/administracaoFrontendLegada.md` | 4 | 2 |
| alterado | `IMPLEMENTATION_REPORT.md` | `docs/reports/implementationReport.md` | 10 | 8 |
| somente_na_atual | — | `docs/reports/sinaisOperacionaisCorrente.md` | 87 | — |
| somente_na_atual | — | `docs/reports/testesCncLocal.md` | 39 | — |
| somente_na_atual | — | `examples/machine-event.json` | 11 | — |
| alterado | `firmware/opta_mesa_monitor.zip` | `firmware/archives/optaCncMonitor.zip` | — | — |
| somente_na_outra | `firmware/esp32_cnc_monitor/README.md` | — | — | 28 |
| realocado_identico | `firmware/esp32_cnc_monitor/esp32_cnc_monitor.ino` | `firmware/legacy/esp32CncMonitor/esp32CncMonitor.ino` | — | — |
| realocado_identico | `firmware/esp32_cnc_monitor/platformio.ini` | `firmware/legacy/esp32CncMonitor/platformio.ini` | — | — |
| somente_na_outra | `firmware/opta_mesa_monitor/README.md` | — | — | 18 |
| alterado | `firmware/opta_mesa_monitor/MesaControl.cpp` | `firmware/optaCncMonitor/cncMonitor.cpp` | 42 | 447 |
| alterado | `firmware/opta_mesa_monitor/MesaControl.h` | `firmware/optaCncMonitor/cncMonitor.h` | 2 | 2 |
| alterado | `firmware/opta_mesa_monitor/Config.h` | `firmware/optaCncMonitor/config.h` | 71 | 4 |
| somente_na_atual | — | `firmware/optaCncMonitor/httpResponse.h` | 80 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/inputMonitor.h` | 29 | — |
| alterado | `firmware/opta_mesa_monitor/mesa_sample.json` | `firmware/optaCncMonitor/monitorSample.json` | 23 | 24 |
| alterado | `firmware/opta_mesa_monitor/opta_mesa_monitor.ino` | `firmware/optaCncMonitor/optaCncMonitor.ino` | 5 | 6 |
| somente_na_atual | — | `firmware/optaCncMonitor/signalProfile.h` | 15 | — |
| alterado | `firmware/opta_mesa_monitor/Telemetry.cpp` | `firmware/optaCncMonitor/telemetry.cpp` | 159 | 56 |
| alterado | `firmware/opta_mesa_monitor/Telemetry.h` | `firmware/optaCncMonitor/telemetry.h` | 2 | 24 |
| somente_na_atual | — | `firmware/optaCncMonitor/telemetryCore.h` | 151 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/telemetryModel.h` | 10 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/telemetryPayload.h` | 82 | — |
| somente_na_outra | `firmware/reference/mesa_opta_v2_original.ino` | — | — | 416 |
| somente_na_atual | — | `firmware/testarFirmware.ps1` | 66 | — |
| somente_na_atual | — | `firmware/tests/host/Arduino.h` | 37 | — |
| somente_na_atual | — | `firmware/tests/host/testControl.cpp` | 63 | — |
| somente_na_atual | — | `firmware/tests/host/testTelemetry.cpp` | 181 | — |
| alterado | `scomptec-cnc front 2/.env.example` | `frontend/.env.example` | 4 | 2 |
| alterado | `scomptec-cnc front 2/.oxlintrc.json` | `frontend/.oxlintrc.json` | 11 | 2 |
| alterado | `scomptec-cnc front 2/electron/main.js` | `frontend/electron/legacy/main.js` | 1 | 1 |
| realocado_identico | `scomptec-cnc front 2/electron/main.cjs` | `frontend/electron/main.cjs` | — | — |
| alterado | `scomptec-cnc front 2/index.html` | `frontend/index.html` | 1 | 1 |
| alterado | `scomptec-cnc front 2/package-lock.json` | `frontend/package-lock.json` | 244 | 215 |
| alterado | `scomptec-cnc front 2/package.json` | `frontend/package.json` | 3 | 11 |
| realocado_identico | `scomptec-cnc front 2/postcss.config.js` | `frontend/postcss.config.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/favicon.svg` | `frontend/public/favicon.svg` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/icons.svg` | `frontend/public/icons.svg` | — | — |
| alterado | `scomptec-cnc front 2/public/login-cnc-background.png` | `frontend/public/loginCncBackground.webp` | — | — |
| somente_na_atual | — | `frontend/public/loginCncBackgroundMobile.webp` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/scomptec-icon.svg` | `frontend/public/scomptecIcon.svg` | — | — |
| realocado_identico | `scomptec-cnc front 2/public/scomptec-logo.webp` | `frontend/public/scomptecLogo.webp` | — | — |
| alterado | `scomptec-cnc front 2/src/App.jsx` | `frontend/src/app.jsx` | 64 | 46 |
| realocado_identico | `scomptec-cnc front 2/src/assets/hero.png` | `frontend/src/assets/hero.png` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/assets/vite.svg` | `frontend/src/assets/vite.svg` | — | — |
| alterado | `scomptec-cnc front 2/src/components/AlertCard/AlertCard.jsx` | `frontend/src/components/alertCard/alertCard.jsx` | 33 | 11 |
| alterado | `scomptec-cnc front 2/src/components/Breadcrumb/Breadcrumb.jsx` | `frontend/src/components/breadcrumb/breadcrumb.jsx` | 1 | 1 |
| somente_na_atual | — | `frontend/src/components/charts/deferredHealth.jsx` | 51 | — |
| somente_na_atual | — | `frontend/src/components/charts/fleetHealth.jsx` | 15 | — |
| alterado | `scomptec-cnc front 2/src/components/charts/TelemetryChart.jsx` | `frontend/src/components/charts/telemetryChart.jsx` | 178 | 40 |
| alterado | `scomptec-cnc front 2/src/components/charts/UtilizationChart.jsx` | `frontend/src/components/charts/utilizationChart.jsx` | 7 | 5 |
| alterado | `scomptec-cnc front 2/src/components/ClientCard/ClientCard.jsx` | `frontend/src/components/clientCard/clientCard.jsx` | 37 | 17 |
| alterado | `scomptec-cnc front 2/src/components/MesaSignals/MesaSignals.jsx` | `frontend/src/components/cncSignals/cncSignals.jsx` | 72 | 61 |
| alterado | `scomptec-cnc front 2/src/components/ConnectionNotice/ConnectionNotice.jsx` | `frontend/src/components/connectionNotice/connectionNotice.jsx` | 5 | 5 |
| alterado | `scomptec-cnc front 2/src/components/ContextSwitcher/ContextSwitcher.jsx` | `frontend/src/components/contextSwitcher/contextSwitcher.jsx` | 92 | 80 |
| realocado_identico | `scomptec-cnc front 2/src/components/EmptyState/EmptyState.jsx` | `frontend/src/components/emptyState/emptyState.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/Header/Header.jsx` | `frontend/src/components/header/header.jsx` | 290 | 173 |
| somente_na_atual | — | `frontend/src/components/liveTime/liveTime.jsx` | 12 | — |
| realocado_identico | `scomptec-cnc front 2/src/components/LoadingState/LoadingState.jsx` | `frontend/src/components/loadingState/loadingState.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/Logo/Logo.jsx` | `frontend/src/components/logo/logo.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/components/MachineCard/MachineCard.jsx` | `frontend/src/components/machineCard/machineCard.jsx` | 76 | 35 |
| realocado_identico | `scomptec-cnc front 2/src/components/MachineIncidents/MachineIncidents.jsx` | `frontend/src/components/machineIncidents/machineIncidents.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/OccurrenceCard/OccurrenceCard.jsx` | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | 118 | 73 |
| realocado_identico | `scomptec-cnc front 2/src/components/OperatingTimeline/OperatingTimeline.jsx` | `frontend/src/components/operatingTimeline/operatingTimeline.jsx` | — | — |
| somente_na_atual | — | `frontend/src/components/pagination/pagination.jsx` | 37 | — |
| somente_na_atual | — | `frontend/src/components/routeBoundary/routeBoundary.jsx` | 61 | — |
| alterado | `scomptec-cnc front 2/src/components/Sidebar/Sidebar.jsx` | `frontend/src/components/sidebar/sidebar.jsx` | 141 | 31 |
| somente_na_atual | — | `frontend/src/components/signalOutputs/fleetSignalOutputs.jsx` | 146 | — |
| somente_na_atual | — | `frontend/src/components/signalOutputs/signalOutputList.jsx` | 56 | — |
| realocado_identico | `scomptec-cnc front 2/src/components/StatCard/StatCard.jsx` | `frontend/src/components/statCard/statCard.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/components/StatusBadge/StatusBadge.jsx` | `frontend/src/components/statusBadge/statusBadge.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/components/ToastCenter/ToastCenter.jsx` | `frontend/src/components/toastCenter/toastCenter.jsx` | 12 | 5 |
| alterado | `scomptec-cnc front 2/src/contexts/MonitoringContext.jsx` | `frontend/src/contexts/monitoringContext.jsx` | 370 | 174 |
| realocado_identico | `scomptec-cnc front 2/src/data/mockData.js` | `frontend/src/data/mockData.js` | — | — |
| alterado | `scomptec-cnc front 2/src/hooks/useAlerts.js` | `frontend/src/hooks/useAlerts.js` | 2 | 2 |
| somente_na_atual | — | `frontend/src/hooks/useApiQuery.js` | 57 | — |
| somente_na_atual | — | `frontend/src/hooks/useMachineResources.js` | 85 | — |
| alterado | `scomptec-cnc front 2/src/hooks/useMachines.js` | `frontend/src/hooks/useMachines.js` | 25 | 4 |
| alterado | `scomptec-cnc front 2/src/hooks/useRelativeDuration.js` | `frontend/src/hooks/useRelativeDuration.js` | 45 | 6 |
| alterado | `scomptec-cnc front 2/src/index.css` | `frontend/src/index.css` | 187 | 11 |
| alterado | `scomptec-cnc front 2/src/layouts/DashboardLayout/DashboardLayout.jsx` | `frontend/src/layouts/dashboardLayout/dashboardLayout.jsx` | 19 | 12 |
| alterado | `scomptec-cnc front 2/src/layouts/TVLayout/TVLayout.jsx` | `frontend/src/layouts/tvLayout/tvLayout.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/main.jsx` | `frontend/src/main.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/pages/Admin/admin.css` | `frontend/src/pages/admin/admin.css` | 19 | 0 |
| alterado | `scomptec-cnc front 2/src/pages/Admin/Admin.jsx` | `frontend/src/pages/admin/admin.jsx` | 3 | 3 |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminAccess.jsx` | `frontend/src/pages/admin/adminAccess.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminActivity.jsx` | `frontend/src/pages/admin/adminActivity.jsx` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/adminModel.js` | `frontend/src/pages/admin/adminModel.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/adminModel.test.js` | `frontend/src/pages/admin/adminModel.test.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/pages/Admin/AdminUserRow.jsx` | `frontend/src/pages/admin/adminUserRow.jsx` | — | — |
| alterado | `scomptec-cnc front 2/src/pages/Alerts/Alerts.jsx` | `frontend/src/pages/alerts/alerts.jsx` | 44 | 20 |
| alterado | `scomptec-cnc front 2/src/pages/Clients/Clients.jsx` | `frontend/src/pages/clients/clients.jsx` | 12 | 7 |
| alterado | `scomptec-cnc front 2/src/pages/CompanySelection/CompanySelection.jsx` | `frontend/src/pages/companySelection/companySelection.jsx` | 115 | 44 |
| alterado | `scomptec-cnc front 2/src/pages/Dashboard/Dashboard.jsx` | `frontend/src/pages/dashboard/dashboard.jsx` | 137 | 44 |
| alterado | `scomptec-cnc front 2/src/pages/Devices/Devices.jsx` | `frontend/src/pages/devices/devices.jsx` | 25 | 146 |
| alterado | `scomptec-cnc front 2/src/pages/History/History.jsx` | `frontend/src/pages/history/history.jsx` | 191 | 171 |
| alterado | `scomptec-cnc front 2/src/pages/Landing/Landing.jsx` | `frontend/src/pages/landing/landing.jsx` | 30 | 10 |
| alterado | `scomptec-cnc front 2/src/pages/Login/Login.jsx` | `frontend/src/pages/login/login.jsx` | 56 | 18 |
| alterado | `scomptec-cnc front 2/src/pages/MachineDetails/MachineDetails.jsx` | `frontend/src/pages/machineDetails/machineDetails.jsx` | 356 | 214 |
| alterado | `scomptec-cnc front 2/src/pages/Machines/Machines.jsx` | `frontend/src/pages/machines/machines.jsx` | 80 | 23 |
| somente_na_atual | — | `frontend/src/pages/passwordHelp/passwordHelp.jsx` | 21 | — |
| alterado | `scomptec-cnc front 2/src/pages/Register/Register.jsx` | `frontend/src/pages/register/register.jsx` | 1 | 1 |
| alterado | `scomptec-cnc front 2/src/pages/Settings/Settings.jsx` | `frontend/src/pages/settings/settings.jsx` | 11 | 0 |
| alterado | `scomptec-cnc front 2/src/pages/Splash/Splash.jsx` | `frontend/src/pages/splash/splash.jsx` | 1 | 1 |
| realocado_identico | `scomptec-cnc front 2/src/pages/TVDashboard/tv.css` | `frontend/src/pages/tvDashboard/tv.css` | — | — |
| alterado | `scomptec-cnc front 2/src/pages/TVDashboard/TVDashboard.jsx` | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | 272 | 62 |
| alterado | `scomptec-cnc front 2/src/pages/Units/Units.jsx` | `frontend/src/pages/units/units.jsx` | 45 | 17 |
| realocado_identico | `scomptec-cnc front 2/src/services/adminSession.js` | `frontend/src/services/adminSession.js` | — | — |
| alterado | `scomptec-cnc front 2/src/services/api.js` | `frontend/src/services/api.js` | 140 | 90 |
| somente_na_atual | — | `frontend/src/services/apiConfig.js` | 9 | — |
| somente_na_atual | — | `frontend/src/services/apiConfig.test.js` | 17 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.js` | 31 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.test.js` | 47 | — |
| realocado_identico | `scomptec-cnc front 2/src/services/eventBus.js` | `frontend/src/services/eventBus.js` | — | — |
| somente_na_atual | — | `frontend/src/services/machineData.js` | 130 | — |
| somente_na_atual | — | `frontend/src/services/monitoring.js` | 132 | — |
| somente_na_atual | — | `frontend/src/services/monitoring.test.js` | 338 | — |
| alterado | `scomptec-cnc front 2/src/services/preferences.js` | `frontend/src/services/preferences.js` | 3 | 1 |
| somente_na_atual | — | `frontend/src/services/signalOutputs.js` | 61 | — |
| somente_na_atual | — | `frontend/src/services/signalOutputs.test.js` | 100 | — |
| alterado | `scomptec-cnc front 2/src/services/telemetry.js` | `frontend/src/services/telemetry.js` | 87 | 21 |
| alterado | `scomptec-cnc front 2/src/services/telemetry.test.js` | `frontend/src/services/telemetry.test.js` | 148 | 29 |
| realocado_identico | `scomptec-cnc front 2/src/services/utilization.js` | `frontend/src/services/utilization.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/services/utilization.test.js` | `frontend/src/services/utilization.test.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/services/websocket.js` | `frontend/src/services/websocket.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/utils/problems.js` | `frontend/src/utils/problems.js` | — | — |
| realocado_identico | `scomptec-cnc front 2/src/utils/severity.js` | `frontend/src/utils/severity.js` | — | — |
| alterado | `scomptec-cnc front 2/src/utils/status.js` | `frontend/src/utils/status.js` | 66 | 31 |
| alterado | `scomptec-cnc front 2/src/utils/time.js` | `frontend/src/utils/time.js` | 14 | 5 |
| alterado | `scomptec-cnc front 2/tailwind.config.js` | `frontend/tailwind.config.js` | 20 | 20 |
| alterado | `scomptec-cnc front 2/vite.config.js` | `frontend/vite.config.js` | 9 | 8 |
| somente_na_outra | `iniciar.cmd` | — | — | 69 |
| somente_na_atual | — | `iniciarLocal.ps1` | 169 | — |
| realocado_identico | `tests/conftest.py` | `legacy/mongodb/tests/conftest.py` | — | — |
| realocado_identico | `tests/test_endpoints.py` | `legacy/mongodb/tests/testEndpoints.py` | — | — |
| realocado_identico | `tests/test_services.py` | `legacy/mongodb/tests/testServices.py` | — | — |
| somente_na_atual | — | `Main.pdf` | — | — |
| alterado | `pytest.ini` | `pytest.ini` | 2 | 1 |
| alterado | `README.md` | `README.md` | 531 | 128 |
| alterado | `requirements.txt` | `requirements.txt` | 21 | 9 |
| somente_na_outra | `SCOMPTEC- Back/README.md` | — | — | 48 |
| somente_na_outra | `SCOMPTEC- Back/requirements-dev.txt` | — | — | 3 |
| somente_na_outra | `SCOMPTEC- Back/requirements.txt` | — | — | 6 |
| somente_na_outra | `scomptec-cnc front 2/.gitignore` | — | — | 4 |
| somente_na_outra | `scomptec-cnc front 2/README.md` | — | — | 115 |
| somente_na_atual | — | `tools/configurarRede.ps1` | 39 | — |
| somente_na_atual | — | `tools/configurarTransmissao.py` | 78 | — |
| alterado | `tools/ponte_usb.py` | `tools/ponteUsb.py` | 105 | 73 |
| somente_na_atual | — | `tools/publicarEventos.py` | 42 | — |
| somente_na_outra | `tools/requirements-usb.txt` | — | — | 2 |
| somente_na_atual | — | `tools/simuladorCnc.py` | 53 | — |
| somente_na_atual | — | `tools/testarFrontend.py` | 200 | — |
| alterado | `docs/testar-opta.ps1` | `tools/testarOpta.ps1` | 3 | 3 |
| somente_na_atual | — | `tools/testarProjeto.ps1` | 123 | — |
| somente_na_atual | — | `tools/tests/testConfigurarTransmissao.py` | 115 | — |
| somente_na_atual | — | `tools/tests/testEventTools.py` | 111 | — |
| alterado | `tools/tests/test_ponte_usb.py` | `tools/tests/testPonteUsb.py` | 132 | 20 |

## ZIP_ALERT — ZIP UltronScomptec-main de ALERT

Origem: `C:\Users\pedro\OneDrive\Desktop\BeeGuardDataset\ALERT\UltronScomptec-main.zip`

Contagens: `{"alterado": 85, "identico": 71, "somente_na_atual": 41, "somente_na_outra": 6, "realocado_identico": 1}`

| Estado | Caminho na outra cópia | Caminho na atual | + linhas | − linhas |
|---|---|---|---:|---:|
| alterado | `.gitignore` | `.gitignore` | 4 | 0 |
| alterado | `backend/.env.example` | `backend/.env.example` | 7 | 0 |
| alterado | `backend/config.example.json` | `backend/config.example.json` | 3 | 1 |
| alterado | `backend/config.py` | `backend/config.py` | 1 | 1 |
| alterado | `backend/database/models.py` | `backend/database/models.py` | 34 | 1 |
| alterado | `backend/main.py` | `backend/main.py` | 2 | 1 |
| alterado | `backend/schemas/cnc.py` | `backend/schemas/cnc.py` | 15 | 1 |
| somente_na_atual | — | `backend/schemas/event.py` | 33 | — |
| somente_na_atual | — | `backend/schemas/observation.py` | 19 | — |
| somente_na_atual | — | `backend/schemas/signalOutput.py` | 10 | — |
| alterado | `backend/schemas/telemetry.py` | `backend/schemas/telemetry.py` | 7 | 14 |
| alterado | `backend/services/clock.py` | `backend/services/clock.py` | 4 | 4 |
| alterado | `backend/services/cncService.py` | `backend/services/cncService.py` | 60 | 21 |
| somente_na_atual | — | `backend/services/codeService.py` | 29 | — |
| alterado | `backend/services/deviceAuth.py` | `backend/services/deviceAuth.py` | 2 | 10 |
| alterado | `backend/services/deviceService.py` | `backend/services/deviceService.py` | 7 | 27 |
| somente_na_atual | — | `backend/services/eventRepository.py` | 103 | — |
| somente_na_atual | — | `backend/services/events.py` | 88 | — |
| somente_na_atual | — | `backend/services/ingestAuth.py` | 11 | — |
| somente_na_atual | — | `backend/services/machineState.py` | 48 | — |
| somente_na_atual | — | `backend/services/signalOutputs.py` | 82 | — |
| alterado | `backend/services/telemetry.py` | `backend/services/telemetry.py` | 13 | 56 |
| alterado | `backend/services/utilization.py` | `backend/services/utilization.py` | 3 | 3 |
| somente_na_atual | — | `backend/tests/testEvents.py` | 332 | — |
| alterado | `backend/tests/testMysqlConcurrency.py` | `backend/tests/testMysqlConcurrency.py` | 2 | 2 |
| alterado | `backend/tests/testOptaApi.py` | `backend/tests/testOptaApi.py` | 17 | 14 |
| somente_na_atual | — | `backend/tests/testSignalOutputs.py` | 105 | — |
| somente_na_outra | `backend/tests/testWifiFlow.py` | — | — | 171 |
| somente_na_atual | — | `configuracao.json` | 552 | — |
| alterado | `docs/guides/administracao.md` | `docs/guides/administracao.md` | 1 | 1 |
| alterado | `docs/guides/explicacaoBackendFrontend.md` | `docs/guides/explicacaoBackendFrontend.md` | 26 | 638 |
| alterado | `docs/guides/guiaEquipe.md` | `docs/guides/guiaEquipe.md` | 54 | 443 |
| alterado | `docs/guides/integracaoOpta.md` | `docs/guides/integracaoOpta.md` | 48 | 79 |
| somente_na_atual | — | `docs/guides/testesResponsividade.md` | 49 | — |
| alterado | `docs/reports/administracaoFrontendLegada.md` | `docs/reports/administracaoFrontendLegada.md` | 1 | 1 |
| somente_na_outra | `docs/reports/relatorioCompletoOpta.txt` | — | — | 739 |
| somente_na_atual | — | `docs/reports/sinaisOperacionaisCorrente.md` | 87 | — |
| somente_na_atual | — | `docs/reports/testesCncLocal.md` | 39 | — |
| somente_na_outra | `docs/reports/testesWifiLocal.md` | — | — | 72 |
| somente_na_atual | — | `examples/machine-event.json` | 11 | — |
| alterado | `firmware/archives/optaMesaMonitor.zip` | `firmware/archives/optaCncMonitor.zip` | — | — |
| alterado | `firmware/optaMesaMonitor/mesaControl.cpp` | `firmware/optaCncMonitor/cncMonitor.cpp` | 39 | 457 |
| alterado | `firmware/optaMesaMonitor/mesaControl.h` | `firmware/optaCncMonitor/cncMonitor.h` | 2 | 2 |
| alterado | `firmware/optaMesaMonitor/config.h` | `firmware/optaCncMonitor/config.h` | 23 | 3 |
| realocado_identico | `firmware/optaMesaMonitor/httpResponse.h` | `firmware/optaCncMonitor/httpResponse.h` | — | — |
| somente_na_atual | — | `firmware/optaCncMonitor/inputMonitor.h` | 29 | — |
| alterado | `firmware/optaMesaMonitor/mesaSample.json` | `firmware/optaCncMonitor/monitorSample.json` | 23 | 24 |
| somente_na_atual | — | `firmware/optaCncMonitor/optaCncMonitor.ino` | 10 | — |
| somente_na_atual | — | `firmware/optaCncMonitor/signalProfile.h` | 15 | — |
| alterado | `firmware/optaMesaMonitor/telemetry.cpp` | `firmware/optaCncMonitor/telemetry.cpp` | 6 | 6 |
| alterado | `firmware/optaMesaMonitor/telemetry.h` | `firmware/optaCncMonitor/telemetry.h` | 1 | 1 |
| alterado | `firmware/optaMesaMonitor/telemetryCore.h` | `firmware/optaCncMonitor/telemetryCore.h` | 4 | 8 |
| alterado | `firmware/optaMesaMonitor/telemetryModel.h` | `firmware/optaCncMonitor/telemetryModel.h` | 3 | 15 |
| alterado | `firmware/optaMesaMonitor/telemetryPayload.h` | `firmware/optaCncMonitor/telemetryPayload.h` | 18 | 33 |
| somente_na_outra | `firmware/optaMesaMonitor/optaMesaMonitor.ino` | — | — | 12 |
| somente_na_outra | `firmware/reference/mesaOptaV2Original.ino` | — | — | 416 |
| alterado | `firmware/testarFirmware.ps1` | `firmware/testarFirmware.ps1` | 2 | 2 |
| alterado | `firmware/tests/host/Arduino.h` | `firmware/tests/host/Arduino.h` | 5 | 2 |
| alterado | `firmware/tests/host/testControl.cpp` | `firmware/tests/host/testControl.cpp` | 52 | 61 |
| alterado | `firmware/tests/host/testTelemetry.cpp` | `firmware/tests/host/testTelemetry.cpp` | 56 | 19 |
| alterado | `frontend/.env.example` | `frontend/.env.example` | 4 | 2 |
| alterado | `frontend/.oxlintrc.json` | `frontend/.oxlintrc.json` | 11 | 2 |
| alterado | `frontend/package.json` | `frontend/package.json` | 2 | 11 |
| alterado | `frontend/public/loginCncBackground.png` | `frontend/public/loginCncBackground.webp` | — | — |
| somente_na_atual | — | `frontend/public/loginCncBackgroundMobile.webp` | — | — |
| alterado | `frontend/src/app.jsx` | `frontend/src/app.jsx` | 63 | 45 |
| alterado | `frontend/src/components/alertCard/alertCard.jsx` | `frontend/src/components/alertCard/alertCard.jsx` | 33 | 12 |
| somente_na_atual | — | `frontend/src/components/charts/deferredHealth.jsx` | 51 | — |
| somente_na_atual | — | `frontend/src/components/charts/fleetHealth.jsx` | 15 | — |
| alterado | `frontend/src/components/charts/telemetryChart.jsx` | `frontend/src/components/charts/telemetryChart.jsx` | 173 | 40 |
| alterado | `frontend/src/components/clientCard/clientCard.jsx` | `frontend/src/components/clientCard/clientCard.jsx` | 35 | 15 |
| alterado | `frontend/src/components/mesaSignals/mesaSignals.jsx` | `frontend/src/components/cncSignals/cncSignals.jsx` | 72 | 61 |
| alterado | `frontend/src/components/contextSwitcher/contextSwitcher.jsx` | `frontend/src/components/contextSwitcher/contextSwitcher.jsx` | 90 | 78 |
| alterado | `frontend/src/components/header/header.jsx` | `frontend/src/components/header/header.jsx` | 286 | 176 |
| somente_na_atual | — | `frontend/src/components/liveTime/liveTime.jsx` | 12 | — |
| alterado | `frontend/src/components/machineCard/machineCard.jsx` | `frontend/src/components/machineCard/machineCard.jsx` | 75 | 34 |
| alterado | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | `frontend/src/components/occurrenceCard/occurrenceCard.jsx` | 117 | 73 |
| somente_na_atual | — | `frontend/src/components/pagination/pagination.jsx` | 37 | — |
| somente_na_atual | — | `frontend/src/components/routeBoundary/routeBoundary.jsx` | 61 | — |
| alterado | `frontend/src/components/sidebar/sidebar.jsx` | `frontend/src/components/sidebar/sidebar.jsx` | 138 | 28 |
| somente_na_atual | — | `frontend/src/components/signalOutputs/fleetSignalOutputs.jsx` | 146 | — |
| somente_na_atual | — | `frontend/src/components/signalOutputs/signalOutputList.jsx` | 56 | — |
| alterado | `frontend/src/components/toastCenter/toastCenter.jsx` | `frontend/src/components/toastCenter/toastCenter.jsx` | 12 | 5 |
| alterado | `frontend/src/contexts/monitoringContext.jsx` | `frontend/src/contexts/monitoringContext.jsx` | 364 | 182 |
| somente_na_atual | — | `frontend/src/hooks/useApiQuery.js` | 57 | — |
| somente_na_atual | — | `frontend/src/hooks/useMachineResources.js` | 85 | — |
| alterado | `frontend/src/hooks/useMachines.js` | `frontend/src/hooks/useMachines.js` | 24 | 3 |
| alterado | `frontend/src/hooks/useRelativeDuration.js` | `frontend/src/hooks/useRelativeDuration.js` | 45 | 6 |
| alterado | `frontend/src/index.css` | `frontend/src/index.css` | 92 | 15 |
| alterado | `frontend/src/layouts/dashboardLayout/dashboardLayout.jsx` | `frontend/src/layouts/dashboardLayout/dashboardLayout.jsx` | 14 | 7 |
| alterado | `frontend/src/pages/alerts/alerts.jsx` | `frontend/src/pages/alerts/alerts.jsx` | 38 | 14 |
| alterado | `frontend/src/pages/clients/clients.jsx` | `frontend/src/pages/clients/clients.jsx` | 11 | 6 |
| alterado | `frontend/src/pages/companySelection/companySelection.jsx` | `frontend/src/pages/companySelection/companySelection.jsx` | 111 | 40 |
| alterado | `frontend/src/pages/dashboard/dashboard.jsx` | `frontend/src/pages/dashboard/dashboard.jsx` | 122 | 30 |
| alterado | `frontend/src/pages/devices/devices.jsx` | `frontend/src/pages/devices/devices.jsx` | 25 | 146 |
| alterado | `frontend/src/pages/history/history.jsx` | `frontend/src/pages/history/history.jsx` | 188 | 168 |
| alterado | `frontend/src/pages/landing/landing.jsx` | `frontend/src/pages/landing/landing.jsx` | 29 | 9 |
| alterado | `frontend/src/pages/login/login.jsx` | `frontend/src/pages/login/login.jsx` | 55 | 17 |
| alterado | `frontend/src/pages/machineDetails/machineDetails.jsx` | `frontend/src/pages/machineDetails/machineDetails.jsx` | 347 | 206 |
| alterado | `frontend/src/pages/machines/machines.jsx` | `frontend/src/pages/machines/machines.jsx` | 77 | 20 |
| somente_na_atual | — | `frontend/src/pages/passwordHelp/passwordHelp.jsx` | 21 | — |
| alterado | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | `frontend/src/pages/tvDashboard/tvDashboard.jsx` | 270 | 61 |
| alterado | `frontend/src/pages/units/units.jsx` | `frontend/src/pages/units/units.jsx` | 44 | 16 |
| alterado | `frontend/src/services/api.js` | `frontend/src/services/api.js` | 137 | 42 |
| somente_na_atual | — | `frontend/src/services/apiConfig.js` | 9 | — |
| somente_na_atual | — | `frontend/src/services/apiConfig.test.js` | 17 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.js` | 31 | — |
| somente_na_atual | — | `frontend/src/services/cncSignals.test.js` | 47 | — |
| alterado | `frontend/src/services/machineData.js` | `frontend/src/services/machineData.js` | 124 | 54 |
| alterado | `frontend/src/services/monitoring.js` | `frontend/src/services/monitoring.js` | 115 | 25 |
| alterado | `frontend/src/services/monitoring.test.js` | `frontend/src/services/monitoring.test.js` | 236 | 20 |
| somente_na_atual | — | `frontend/src/services/signalOutputs.js` | 61 | — |
| somente_na_atual | — | `frontend/src/services/signalOutputs.test.js` | 100 | — |
| alterado | `frontend/src/services/telemetry.js` | `frontend/src/services/telemetry.js` | 88 | 22 |
| alterado | `frontend/src/services/telemetry.test.js` | `frontend/src/services/telemetry.test.js` | 148 | 29 |
| alterado | `frontend/src/utils/status.js` | `frontend/src/utils/status.js` | 64 | 29 |
| alterado | `frontend/src/utils/time.js` | `frontend/src/utils/time.js` | 14 | 5 |
| alterado | `frontend/vite.config.js` | `frontend/vite.config.js` | 9 | 8 |
| alterado | `iniciarLocal.ps1` | `iniciarLocal.ps1` | 7 | 6 |
| somente_na_atual | — | `Main.pdf` | — | — |
| alterado | `README.md` | `README.md` | 523 | 129 |
| alterado | `tools/configurarRede.ps1` | `tools/configurarRede.ps1` | 1 | 1 |
| alterado | `tools/configurarTransmissao.py` | `tools/configurarTransmissao.py` | 8 | 2 |
| alterado | `tools/ponteUsb.py` | `tools/ponteUsb.py` | 59 | 42 |
| somente_na_atual | — | `tools/publicarEventos.py` | 42 | — |
| somente_na_atual | — | `tools/simuladorCnc.py` | 53 | — |
| somente_na_outra | `tools/simuladorWifi.py` | — | — | 260 |
| somente_na_atual | — | `tools/testarFrontend.py` | 200 | — |
| alterado | `tools/testarOpta.ps1` | `tools/testarOpta.ps1` | 3 | 3 |
| alterado | `tools/testarProjeto.ps1` | `tools/testarProjeto.ps1` | 3 | 1 |
| alterado | `tools/tests/testConfigurarTransmissao.py` | `tools/tests/testConfigurarTransmissao.py` | 27 | 1 |
| somente_na_atual | — | `tools/tests/testEventTools.py` | 111 | — |
| alterado | `tools/tests/testPonteUsb.py` | `tools/tests/testPonteUsb.py` | 67 | 18 |
