export const OUTPUT_LEVELS = {
  critical: {
    label: "Crítico",
    tone: "border-rose-500/30 bg-rose-500/10 text-rose-500",
  },
  attention: {
    label: "Atenção",
    tone: "border-amber-500/30 bg-amber-500/10 text-amber-600",
  },
  info: {
    label: "Informativo",
    tone: "border-base-border bg-base-surface/60 text-text-secondary",
  },
};
const priority = { critical: 0, attention: 1, info: 2 };

export function signalOutputsFor(machine) {
  const outputs = machine.signalOutputs?.length
    ? machine.signalOutputs
    : (machine.diagnostics || []).map((item) => ({
        ...item,
        level: item.severity === "EMERGENCIA" ? "critical" : "attention",
      }));
  return [...new Map(outputs.map((item) => [item.code, item])).values()].sort(
    (a, b) => (priority[a.level] ?? 2) - (priority[b.level] ?? 2),
  );
}

export function signalOutputsStale(machine) {
  return Boolean(
    machine.dataStale ||
    machine.communicationStatus !== "ONLINE" ||
    ["SEM_COMUNICACAO", "DADOS_DESATUALIZADOS", "RECONNECTING"].includes(
      machine.status,
    ),
  );
}

export function selectSignalOutputMachines(
  machines,
  machineId = "",
  level = "",
) {
  return machines
    .filter((machine) => !machineId || machine.id === machineId)
    .map((machine) => ({
      machine,
      stale: signalOutputsStale(machine),
      outputs: signalOutputsFor(machine).filter(
        (output) => !level || output.level === level,
      ),
    }))
    .filter((row) => row.outputs.length)
    .sort(
      (a, b) =>
        Number(a.stale) - Number(b.stale) ||
        (priority[a.outputs[0].level] ?? 2) -
          (priority[b.outputs[0].level] ?? 2) ||
        a.machine.id.localeCompare(b.machine.id, "pt-BR", { numeric: true }),
    );
}
