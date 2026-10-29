import test from "node:test";
import assert from "node:assert/strict";
import { loadMachines } from "./machineData.js";
import { markStale } from "./telemetry.js";
import { monitoringAlerts, monitoringTransitions, monitoringWarning } from "./monitoring.js";

const timestamp = "2026-10-21T15:00:00Z";
function server() {
  const failures = new Set();
  const statuses = { a: "EMERGENCIA", b: "OPERANDO" };
  const request = async path => {
    if (failures.has(path)) throw new Error(`Falha em ${path}`);
    if (path === "/cncs") return ["a", "b"].map(id => ({ id, code: `CNC-${id}`, name: `Máquina ${id}` }));
    if (path === "/devices") return ["a", "b"].map(id => ({ id: `device-${id}`, cnc_id: id, code: `OPTA-${id}`, firmware_version: "test" }));
    const id = path.split("/")[2];
    if (path.endsWith("/status")) return { status: statuses[id], online: true, status_since: timestamp,
      last_seen: timestamp, telemetry_timestamp: timestamp, states: { emergencia: statuses[id] === "EMERGENCIA" },
      analog_signals: {}, extra_signals: {} };
    if (path.includes("/history")) return { total: 1, items: [{ id, timestamp, machine_active: true, digital_signals: { ciclo: true } }] };
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
  assert.equal(monitoringTransitions(transitions.confirmed, recovered).notices.length, 0);
});

test("total API outage never clears a known emergency or fabricates a resolution", async () => {
  const source = server();
  const initial = await loadMachines(source.request);
  source.failures.add("/cncs");
  await assert.rejects(loadMachines(source.request, initial), /Falha em \/cncs/);
  const stale = markStale(markStale(initial));
  const alerts = monitoringAlerts(stale, monitoringAlerts(initial));
  assert.equal(alerts.find(alert => alert.machineId === "CNC-a").severity, "EMERGENCIA");
  assert.equal(alerts.find(alert => alert.machineId === "CNC-a").stale, true);
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
  assert.equal(monitoringTransitions(next.confirmed, emergency).notices.length, 0);
  source.statuses.a = "OPERANDO";
  const recovered = await loadMachines(source.request, emergency);
  const resolution = monitoringTransitions(next.confirmed, recovered);
  assert.equal(resolution.notices.length, 1);
  assert.equal(resolution.notices[0].resolved, true);
  assert.equal(monitoringAlerts(recovered).length, 0);
});

test("dashboard never queries collector endpoints and accepts arbitrary machine states", async () => {
  const paths = [];
  const request = async path => {
    paths.push(path);
    if (path === "/cncs") return [{ id: "machine-only", code: "CNC-001", name: "Origem independente" }];
    if (path.endsWith("/status")) return { status: "PARADA", online: true, states: { porta_aberta: true, pausa: false }, last_seen: timestamp };
    if (path.includes("/history")) return { total: 0, items: [] };
    if (path.endsWith("/utilization")) return { buckets: [] };
    throw new Error(`Consulta indevida: ${path}`);
  };
  const [machine] = await loadMachines(request);
  assert.deepEqual(machine.digitalSignals, { porta_aberta: true, pausa: false });
  assert.equal(machine.communicationStatus, "ONLINE");
  assert.ok(paths.every(path => !path.includes("devices")));
  assert.equal(monitoringWarning([machine]), null);
});
