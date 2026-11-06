export const FAILURE_CAUSES = Object.freeze([
  { key: "ativo", label: "Falha na execução", color: "#2563EB" },
  { key: "inativo", label: "Falha na parada", color: "#D97706" },
  { key: "emergencia", label: "Falha na emergência", color: "#E11D48" },
  { key: "motor_ligado", label: "Falha no motor", color: "#7C3AED" },
  { key: "porta_aberta", label: "Falha na porta", color: "#0891B2" },
  { key: "alarme", label: "Falha no alarme / erro", color: "#DB2777" },
]);

export function summarizeFailureCauses(machines = [], hours = 24) {
  const totals = Object.fromEntries(FAILURE_CAUSES.map(({ key }) => [key, 0]));
  let available = false;
  let samples = 0;
  for (const machine of machines) {
    for (const bucket of machine.utilization?.buckets?.slice(-hours) || []) {
      if (!bucket.failure_causes) continue;
      available = true;
      samples += bucket.samples || 0;
      for (const { key } of FAILURE_CAUSES) {
        const count = bucket.failure_causes[key];
        if (Number.isInteger(count) && count >= 0) totals[key] += count;
      }
    }
  }
  const total = Object.values(totals).reduce((sum, value) => sum + value, 0);
  const data = FAILURE_CAUSES.map((cause) => ({
    ...cause,
    count: totals[cause.key],
    percentage: total ? (totals[cause.key] / total) * 100 : 0,
  })).filter(({ count }) => count > 0).sort((a, b) => b.count - a.count);
  return { data, total, available, samples };
}
