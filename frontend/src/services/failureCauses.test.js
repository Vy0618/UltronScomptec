import test from "node:test";
import assert from "node:assert/strict";
import { FAILURE_CAUSES, summarizeFailureCauses } from "./failureCauses.js";

const machine = (entries) => ({ utilization: { buckets: Array.from({ length: 24 }, (_, i) => ({
  samples: entries[i] ? 1 : 0, failure_causes: entries[i] || {},
})) } });

test("failure causes combine the scoped machines and rank by occurrences with stable colors", () => {
  const result = summarizeFailureCauses([
    machine({ 23: { inativo: 2, ativo: 1 } }),
    machine({ 23: { inativo: 1, porta_aberta: 2 } }),
  ]);
  assert.equal(result.total, 6);
  assert.equal(result.available, true);
  assert.deepEqual(result.data.map(({ key, count }) => [key, count]), [
    ["inativo", 3], ["porta_aberta", 2], ["ativo", 1],
  ]);
  assert.equal(result.data[0].label, "Falha na parada");
  assert.equal(result.data[0].percentage, 50);
  assert.ok(Math.abs(result.data.reduce((sum, item) => sum + item.percentage, 0) - 100) < 1e-10);
  assert.equal(result.data[0].color, FAILURE_CAUSES.find(({ key }) => key === "inativo").color);
  assert.equal(new Set(FAILURE_CAUSES.map(({ color }) => color)).size, 6);
});

test("failure causes follow the same 8/12/24 hour window as the existing chart", () => {
  const machines = [machine({ 0: { ativo: 5 }, 12: { inativo: 2 }, 23: { porta_aberta: 1 } })];
  assert.equal(summarizeFailureCauses(machines, 24).total, 8);
  assert.equal(summarizeFailureCauses(machines, 12).total, 3);
  assert.equal(summarizeFailureCauses(machines, 8).total, 1);
});

test("no fault occurrences are distinct from unavailable history and raw snapshots do not become counts", () => {
  assert.deepEqual(summarizeFailureCauses([]), { data: [], total: 0, available: false, samples: 0 });
  assert.equal(summarizeFailureCauses([{ digitalSignals: { inativo: true }, readings: [{ states: { inativo: true } }] }]).total, 0);
  assert.equal(summarizeFailureCauses([{ utilization: { buckets: [{ seconds: { EMERGENCIA: 60 } }] } }]).available, false);
  assert.equal(summarizeFailureCauses([machine({})]).available, true);
  assert.deepEqual(summarizeFailureCauses([machine({})]).data, []);
});
