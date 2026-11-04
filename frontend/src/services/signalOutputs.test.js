import test from "node:test";
import assert from "node:assert/strict";
import {
  signalOutputsFor,
  signalOutputsStale,
  selectSignalOutputMachines,
} from "./signalOutputs.js";
import { loadMachineStatuses } from "./machineData.js";
import { markStale, readingEvent } from "./telemetry.js";

const output = (code, level = "info") => ({
  code,
  level,
  title: code,
  message: "Sinais da mesma leitura",
  signals: ["ativo"],
});
const machine = (id, outputs) => ({
  id,
  status: "OPERANDO",
  communicationStatus: "ONLINE",
  signalOutputs: outputs,
});

test("API outputs update without a change in status and survive communication loss", async () => {
  const snapshot = {
    id: "a",
    code: "CNC-001",
    name: "CNC",
    status: "OPERANDO",
    online: true,
    states: { ativo: true, porta_aberta: false },
    signal_outputs: [output("ATIVIDADE_INFORMADA")],
  };
  const before = await loadMachineStatuses(async () => [snapshot]);
  const next = await loadMachineStatuses(
    async () => [
      {
        ...snapshot,
        states: { ativo: true, porta_aberta: true },
        signal_outputs: [output("ATIVIDADE_COM_PORTA_ABERTA", "attention")],
      },
    ],
    before,
  );
  assert.notEqual(next, before);
  assert.equal(next[0].status, "OPERANDO");
  assert.equal(signalOutputsFor(next[0])[0].code, "ATIVIDADE_COM_PORTA_ABERTA");
  const stale = markStale(next)[0];
  assert.equal(signalOutputsStale(stale), true);
  assert.deepEqual(signalOutputsFor(stale), signalOutputsFor(next[0]));
});

test("panel filters by machine and level, orders urgent current readings before stale outputs", () => {
  const rows = [
    machine("CNC-001", [output("INFO")]),
    machine("CNC-002", [output("CRITICAL", "critical")]),
    machine("CNC-003", [output("ATTENTION", "attention")]),
    {
      ...machine("CNC-004", [output("OLD", "critical")]),
      communicationStatus: "OFFLINE",
    },
  ];
  assert.deepEqual(
    selectSignalOutputMachines(rows).map((row) => row.machine.id),
    ["CNC-002", "CNC-003", "CNC-001", "CNC-004"],
  );
  assert.deepEqual(selectSignalOutputMachines(rows, "CNC-001", "critical"), []);
  assert.equal(
    selectSignalOutputMachines(rows, "CNC-003", "attention")[0].outputs[0].code,
    "ATTENTION",
  );
  assert.equal(selectSignalOutputMachines(rows, "CNC-004")[0].stale, true);
});

test("older diagnostics remain visible and historical outputs come from the historical reading", () => {
  const legacy = {
    diagnostics: [
      {
        code: "PORTA_ABERTA_EMERGENCIA",
        severity: "EMERGENCIA",
        title: "Operação falha",
      },
    ],
  };
  assert.equal(signalOutputsFor(legacy)[0].level, "critical");
  const current = { ...machine("CNC-001", [output("NOW")]), name: "CNC" };
  const event = readingEvent(
    {
      id: "old",
      timestamp: "2026-11-03T12:00:00Z",
      states: { inativo: true },
      signal_outputs: [output("THEN")],
    },
    current,
  );
  assert.equal(event.signalOutputs[0].code, "THEN");
  assert.equal(event.status, "PARADA");
  assert.deepEqual(signalOutputsFor({}), []);
});
