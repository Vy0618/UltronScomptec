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

test("asserted IHM parameters indicate emergency while partial and legacy readings stay supported", () => {
  for (const [states, status] of [
    [{ ativo: true, inativo: false }, "EMERGENCIA"],
    [{ ativo: false, inativo: true }, "EMERGENCIA"],
    [{ ativo: true, inativo: true }, "EMERGENCIA"],
    [{ ativo: false, em_execucao: true }, "PARADA"],
    [{ ativo: true, alarme: true }, "EMERGENCIA"],
    [{ porta_aberta: true, emergencia: true }, "EMERGENCIA"],
    [{ porta_aberta: true }, "EMERGENCIA"],
    [{ motor_ligado: true }, "EMERGENCIA"],
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

test("all 64 IHM snapshots agree with the zero operating / one emergency rule", () => {
  for (let mask = 0; mask < 64; mask++) {
    const states = Object.fromEntries(
      CNC_SIGNALS.map(({ key }, index) => [key, Boolean(mask & (1 << index))]),
    );
    const before = { ...states };
    for (const machine_active of [true, false]) {
      assert.equal(
        readingStatus({ states, machine_active }),
        mask === 0 ? "OPERANDO" : "EMERGENCIA",
        JSON.stringify(states),
      );
    }
    assert.deepEqual(states, before);
  }
  assert.equal(readingStatus({ states: {} }), "PARADA");
  assert.equal(readingStatus({ states: { porta_aberta: false } }), "PARADA");
});
