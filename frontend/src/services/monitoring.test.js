import test from "node:test";
import assert from "node:assert/strict";
import { loadMachines, loadMachineStatuses } from "./machineData.js";
import { markStale } from "./telemetry.js";
import {
  monitoringAlerts,
  monitoringTransitions,
  monitoringWarning,
} from "./monitoring.js";

const timestamp = "2026-10-21T15:00:00Z";

test("current simulation reaches the dashboard with source and zero distinct from unknown", async () => {
  const snapshot = {
    id: "current",
    code: "CNC-001",
    name: "CNC",
    status: "OPERANDO",
    online: true,
    states: { ativo: true },
    analog_signals: { current: 12.5 },
    extra_signals: {
      current_input: {
        input: "I8",
        source: "simulated",
        physical_enabled: false,
      },
    },
  };
  const [machine] = await loadMachineStatuses(async () => [snapshot]);
  assert.equal(machine.current, 12.5);
  assert.equal(machine.currentSource, "simulated");
  const [zero] = await loadMachineStatuses(async () => [
    { ...snapshot, analog_signals: { current: 0 } },
  ]);
  assert.equal(zero.current, 0);
  const [missing] = await loadMachineStatuses(async () => [
    { ...snapshot, analog_signals: {}, extra_signals: {} },
  ]);
  assert.equal(missing.current, null);
  assert.equal(missing.currentSource, "unknown");
});

test("a combined diagnosis notifies even when emergency status was already active", async () => {
  const diagnosis = {
    code: "PORTA_ABERTA_EMERGENCIA",
    severity: "EMERGENCIA",
    title: "Operação falha",
    message: "Porta aberta e emergência acionada na mesma leitura.",
    signals: ["porta_aberta", "emergencia"],
  };
  const snapshot = {
    id: "a",
    code: "CNC-001",
    name: "CNC",
    status: "EMERGENCIA",
    online: true,
    states: { emergencia: true, porta_aberta: false },
    diagnostics: [],
    last_seen: timestamp,
    status_since: timestamp,
    telemetry_timestamp: timestamp,
  };
  const before = await loadMachineStatuses(async () => [snapshot]);
  const observed = "2026-10-21T15:01:00Z";
  const after = await loadMachineStatuses(
    async () => [
      {
        ...snapshot,
        states: { emergencia: true, porta_aberta: true },
        diagnostics: [diagnosis],
        telemetry_timestamp: observed,
      },
    ],
    before,
  );
  assert.deepEqual(after[0].diagnostics, [diagnosis]);
  const notices = monitoringTransitions(before, after).notices;
  assert.equal(notices.length, 1);
  assert.equal(notices[0].title, "Operação falha");
  assert.equal(notices[0].occurredAt, observed);
  assert.equal(monitoringTransitions(after, after).notices.length, 0);
  const alerts = monitoringAlerts(after);
  assert.equal(alerts[0].occurredAt, observed);
  assert.deepEqual(alerts[0].diagnostics, [diagnosis]);
  assert.equal(
    monitoringAlerts(
      [{ ...after[0], telemetryTimestamp: "2026-10-21T15:02:00Z" }],
      alerts,
    )[0].occurredAt,
    observed,
  );
  assert.deepEqual(monitoringAlerts(markStale(after), alerts)[0].diagnostics, [
    diagnosis,
  ]);
  assert.equal(monitoringAlerts(markStale(after), alerts)[0].stale, true);
  assert.equal(
    monitoringTransitions(after, markStale(before)).notices.length,
    0,
  );
});

test("conflicting activity signals have an alert without treating inactive as powered off", () => {
  const machine = {
    id: "CNC-001",
    status: "PARADA",
    communicationStatus: "ONLINE",
    diagnostics: [
      {
        code: "ATIVIDADE_CONFLITANTE",
        title: "Sinais de atividade conflitantes",
      },
    ],
  };
  assert.equal(
    monitoringAlerts([machine])[0].diagnostics[0].code,
    "ATIVIDADE_CONFLITANTE",
  );
});

test("bulk polling fetches only states and reuses unchanged machine references", async () => {
  const calls = [];
  const statuses = [
    {
      id: "a",
      code: "CNC-001",
      name: "CNC",
      status: "EMERGENCIA",
      online: true,
      states: { emergencia: true, porta_aberta: false },
      last_seen: timestamp,
      status_since: timestamp,
    },
  ];
  const request = async (path) => {
    calls.push(path);
    return statuses;
  };
  const first = await loadMachineStatuses(request);
  const same = await loadMachineStatuses(request, first);
  assert.equal(same, first);
  assert.deepEqual(calls, ["/cncs/statuses", "/cncs/statuses"]);
  assert.equal(first[0].current, null);
  statuses[0] = {
    ...statuses[0],
    status: "OPERANDO",
    states: { em_execucao: true },
  };
  const changed = await loadMachineStatuses(request, first);
  assert.deepEqual(changed[0].digitalSignals, { em_execucao: true });
  assert.equal(first[0].status, "EMERGENCIA");
  const notices = monitoringTransitions(first, changed).notices;
  assert.equal(notices.length, 1);
  assert.equal(notices[0].resolved, true);
});
function server() {
  const failures = new Set();
  const statuses = { a: "EMERGENCIA", b: "OPERANDO" };
  const request = async (path) => {
    if (failures.has(path)) throw new Error(`Falha em ${path}`);
    if (path === "/cncs")
      return ["a", "b"].map((id) => ({
        id,
        code: `CNC-${id}`,
        name: `Máquina ${id}`,
      }));
    if (path === "/devices")
      return ["a", "b"].map((id) => ({
        id: `device-${id}`,
        cnc_id: id,
        code: `OPTA-${id}`,
        firmware_version: "test",
      }));
    const id = path.split("/")[2];
    if (path.endsWith("/status"))
      return {
        status: statuses[id],
        online: true,
        status_since: timestamp,
        last_seen: timestamp,
        telemetry_timestamp: timestamp,
        states: { emergencia: statuses[id] === "EMERGENCIA" },
        analog_signals: {},
        extra_signals: {},
      };
    if (path.includes("/history"))
      return {
        total: 1,
        items: [
          {
            id,
            timestamp,
            machine_active: true,
            digital_signals: { ciclo: true },
          },
        ],
      };
    if (path.endsWith("/utilization")) return { buckets: [] };
    throw new Error(`Unexpected request ${path}`);
  };
  return { failures, statuses, request };
}

test("real snapshots map CNC signals without inventing analog readings or historical power", async () => {
  const source = server();
  const [machine] = await loadMachines(source.request);
  assert.equal(machine.status, "EMERGENCIA");
  assert.equal(machine.communicationStatus, "ONLINE");
  assert.equal(machine.digitalSignals.emergencia, true);
  assert.equal(machine.current, null);
  assert.equal(machine.powerAvg, null);
  assert.equal(monitoringWarning([machine]), null);
});

test("history and utilization failures preserve current status and previous data", async () => {
  const source = server();
  const initial = await loadMachines(source.request);
  source.failures.add("/cncs/a/history?limit=100");
  source.failures.add("/cncs/a/utilization");
  source.statuses.a = "ALARME";
  const machines = await loadMachines(source.request, initial);
  assert.equal(machines[0].status, "ALARME");
  assert.equal(machines[1].status, "OPERANDO");
  assert.equal(machines[0].dataStale, false);
  assert.deepEqual(machines[0].readings, initial[0].readings);
  assert.deepEqual(machines[0].utilization, initial[0].utilization);
  assert.match(monitoringWarning(machines), /Atualização parcial/);
});

test("one unavailable CNC keeps its emergency alert while the other continues updating, then recovers", async () => {
  const source = server();
  const initial = await loadMachines(source.request);
  const initialAlerts = monitoringAlerts(initial);
  source.failures.add("/cncs/a/status");
  source.statuses.b = "ALARME";
  const partial = await loadMachines(source.request, initial);
  assert.equal(partial[0].status, "DADOS_DESATUALIZADOS");
  assert.equal(partial[0].lastKnownStatus, "EMERGENCIA");
  assert.equal(partial[0].lastCommunicationAt, timestamp);
  assert.equal(partial[1].status, "ALARME");
  const alerts = monitoringAlerts(partial, initialAlerts);
  assert.equal(alerts[0].severity, "EMERGENCIA");
  assert.equal(alerts[0].stale, true);
  assert.equal(alerts[1].severity, "ALARME");
  const transitions = monitoringTransitions(initial, partial);
  assert.equal(transitions.notices.length, 1);
  assert.equal(transitions.notices[0].machineId, "CNC-b");
  source.failures.clear();
  const recovered = await loadMachines(source.request, partial);
  assert.equal(recovered[0].status, "EMERGENCIA");
  assert.equal(monitoringAlerts(recovered, alerts)[0].stale, false);
  assert.equal(monitoringWarning(recovered), null);
  assert.equal(
    monitoringTransitions(transitions.confirmed, recovered).notices.length,
    0,
  );
});

test("total API outage never clears a known emergency or fabricates a resolution", async () => {
  const source = server();
  const initial = await loadMachines(source.request);
  source.failures.add("/cncs");
  await assert.rejects(
    loadMachines(source.request, initial),
    /Falha em \/cncs/,
  );
  const stale = markStale(markStale(initial));
  const alerts = monitoringAlerts(stale, monitoringAlerts(initial));
  assert.equal(
    alerts.find((alert) => alert.machineId === "CNC-a").severity,
    "EMERGENCIA",
  );
  assert.equal(alerts.find((alert) => alert.machineId === "CNC-a").stale, true);
  assert.equal(stale[0].lastKnownStatus, "EMERGENCIA");
  assert.equal(monitoringTransitions(initial, stale).notices.length, 0);
});

test("initial failed status is unknown rather than a healthy machine", async () => {
  const source = server();
  source.failures.add("/cncs/a/status");
  const machines = await loadMachines(source.request);
  assert.equal(machines[0].status, "DADOS_DESATUALIZADOS");
  assert.equal(machines[0].current, null);
  assert.equal(monitoringAlerts(machines)[0].severity, "DADOS_DESATUALIZADOS");
  assert.equal(monitoringTransitions([], machines).notices.length, 0);
});

test("confirmed emergency and resolution notify once, while initial load and repeated polling stay quiet", async () => {
  const source = server();
  source.statuses.a = "OPERANDO";
  const initial = await loadMachines(source.request);
  const first = monitoringTransitions([], initial);
  assert.deepEqual(first.notices, []);
  source.statuses.a = "EMERGENCIA";
  const emergency = await loadMachines(source.request, initial);
  const next = monitoringTransitions(first.confirmed, emergency);
  assert.equal(next.notices.length, 1);
  assert.equal(next.notices[0].title, "Nova emergência detectada");
  assert.equal(
    monitoringTransitions(next.confirmed, emergency).notices.length,
    0,
  );
  source.statuses.a = "OPERANDO";
  const recovered = await loadMachines(source.request, emergency);
  const resolution = monitoringTransitions(next.confirmed, recovered);
  assert.equal(resolution.notices.length, 1);
  assert.equal(resolution.notices[0].resolved, true);
  assert.equal(monitoringAlerts(recovered).length, 0);
});

test("dashboard never queries collector endpoints and accepts arbitrary machine states", async () => {
  const paths = [];
  const request = async (path) => {
    paths.push(path);
    if (path === "/cncs")
      return [
        { id: "machine-only", code: "CNC-001", name: "Origem independente" },
      ];
    if (path.endsWith("/status"))
      return {
        status: "PARADA",
        online: true,
        states: { porta_aberta: true, pausa: false },
        last_seen: timestamp,
      };
    if (path.includes("/history")) return { total: 0, items: [] };
    if (path.endsWith("/utilization")) return { buckets: [] };
    throw new Error(`Consulta indevida: ${path}`);
  };
  const [machine] = await loadMachines(request);
  assert.deepEqual(machine.digitalSignals, {
    porta_aberta: true,
    pausa: false,
  });
  assert.equal(machine.communicationStatus, "ONLINE");
  assert.ok(paths.every((path) => !path.includes("devices")));
  assert.equal(monitoringWarning([machine]), null);
});
