import test from "node:test";
import assert from "node:assert/strict";
import {
  CNC_SIGNALS,
  observedStates,
  machineActiveFromStates,
} from "./cncSignals.js";
import { readingStatus } from "./telemetry.js";

test("six monitoring signals remain independent and unknown signals are retained", () => {
  assert.deepEqual(
    CNC_SIGNALS.map((item) => item.key),
    [
      "ativo",
      "inativo",
      "emergencia",
      "motor_ligado",
      "porta_aberta",
      "alarme",
    ],
  );
  assert.deepEqual(
    CNC_SIGNALS.map((item) => item.label),
    ["Em execução", "Parada", "Emergência", "Motor ligado", "Porta aberta", "Alerta / erro"],
  );
  const states = { ativo: true, sensor_extra: false };
  assert.equal(observedStates(states).at(-1).key, "sensor_extra");
  assert.equal(Object.hasOwn(states, "inativo"), false);
});

test("new activity signals agree with backend priority and do not infer activity from motor or door", () => {
  for (const [states, status] of [
    [{ ativo: true, inativo: false }, "OPERANDO"],
    [{ ativo: false, inativo: true }, "PARADA"],
    [{ ativo: true, inativo: true }, "PARADA"],
    [{ ativo: false, em_execucao: true }, "PARADA"],
    [{ ativo: true, alarme: true }, "ALARME"],
    [{ porta_aberta: true, emergencia: true }, "EMERGENCIA"],
    [{ porta_aberta: true }, "PARADA"],
    [{ motor_ligado: true }, "PARADA"],
    [{ inativo: false }, "PARADA"],
    [{ em_execucao: true }, "OPERANDO"],
  ])
    assert.equal(readingStatus({ states }), status, JSON.stringify(states));
  assert.equal(machineActiveFromStates({ ativo: false }, true), false);
  assert.equal(machineActiveFromStates({ inativo: true }, true), false);
  assert.equal(
    readingStatus({ machine_active: true, states: { ativo: false } }),
    "PARADA",
  );
});
