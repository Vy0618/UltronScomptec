import { signalOutputsFor } from "./signalOutputs.js";

const problems = new Set([
  "EMERGENCIA",
  "ALARME",
  "PARADA",
  "SEM_COMUNICACAO",
  "DADOS_DESATUALIZADOS",
]);
export const isMonitoringProblem = (status) => problems.has(status);
const diagnosticKey = (machine) =>
  (machine.diagnostics || [])
    .map((item) => item.code)
    .sort()
    .join(",");

export function monitoringAlerts(machines, previousAlerts = []) {
  return machines
    .filter(
      (machine) =>
        isMonitoringProblem(machine.status) || machine.diagnostics?.length,
    )
    .map((machine) => {
      const previous = previousAlerts.find(
        (alert) => alert.machineId === machine.id,
      );
      if (machine.dataStale && previous) return { ...previous, stale: true };
      const diagnostics = machine.diagnostics || [];
      const stale = Boolean(
        machine.dataStale ||
        machine.communicationStatus === "OFFLINE" ||
        machine.status === "DADOS_DESATUALIZADOS",
      );
      const occurredAt =
        diagnostics.length && !stale
          ? previous?.severity === machine.status &&
            diagnosticKey(previous) === diagnosticKey(machine)
            ? previous.occurredAt
            : machine.telemetryTimestamp || machine.stateSince
          : machine.stateSince;
      return {
        id: `api-${machine.backendId}`,
        severity: machine.status,
        machineId: machine.id,
        machineName: machine.name,
        companyName: "",
        unitName: "",
        occurredAt,
        stateSince: machine.stateSince,
        diagnostics,
        signalOutputs: signalOutputsFor(machine),
        time: occurredAt
          ? new Date(occurredAt).toLocaleTimeString("pt-BR")
          : "—",
        critical: machine.status === "EMERGENCIA",
        stale,
      };
    });
}

// Only confirmed observations enter the baseline, including across API outages.
export function monitoringTransitions(previous, machines) {
  const confirmed = new Map(previous.map((machine) => [machine.id, machine]));
  const notices = [];
  for (const machine of machines) {
    if (machine.dataStale || machine.statusError) continue;
    const before = confirmed.get(machine.id);
    confirmed.set(machine.id, machine);
    if (!before) continue;
    const freshSignals =
      !["SEM_COMUNICACAO", "DADOS_DESATUALIZADOS"].includes(machine.status) &&
      machine.communicationStatus !== "OFFLINE";
    const diagnosis =
      freshSignals &&
      (machine.diagnostics || []).find(
        (item) =>
          !(before.diagnostics || []).some(
            (previous) => previous.code === item.code,
          ),
      );
    if (before.status === machine.status && !diagnosis) continue;
    const resolved = Boolean(
      (isMonitoringProblem(before.status) || before.diagnostics?.length) &&
      !isMonitoringProblem(machine.status) &&
      !machine.diagnostics?.length,
    );
    if (
      !resolved &&
      !isMonitoringProblem(machine.status) &&
      !machine.diagnostics?.length
    )
      continue;
    const occurredAt =
      (diagnosis && machine.telemetryTimestamp) ||
      machine.stateSince ||
      machine.telemetryTimestamp ||
      new Date().toISOString();
    notices.push({
      id: `transition-${machine.backendId}-${machine.status}-${diagnosis?.code || "status"}-${occurredAt}`,
      machineId: machine.id,
      machineName: machine.name,
      severity: machine.status,
      occurredAt,
      resolved,
      companyName: "",
      unitName: "",
      title: resolved
        ? "Problema encerrado"
        : diagnosis
          ? diagnosis.title
          : machine.status === "EMERGENCIA"
            ? "Nova emergência detectada"
            : "Novo alerta de máquina",
    });
  }
  return {
    confirmed: [...confirmed.values()].filter((machine) =>
      machines.some((current) => current.id === machine.id),
    ),
    notices,
  };
}

export function monitoringWarning(machines) {
  const failures = machines.filter(
    (machine) =>
      machine.statusError || machine.historyError || machine.utilizationError,
  );
  return failures.length
    ? `Atualização parcial: ${failures.length} máquina(s) com consulta indisponível. Os estados disponíveis continuam sendo atualizados.`
    : null;
}
