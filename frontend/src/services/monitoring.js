const problems = new Set(["EMERGENCIA", "ALARME", "PARADA", "SEM_COMUNICACAO", "DADOS_DESATUALIZADOS"]);
export const isMonitoringProblem = status => problems.has(status);

export function monitoringAlerts(machines, previousAlerts = []) {
  return machines.filter(machine => isMonitoringProblem(machine.status)).map(machine => {
    const previous = previousAlerts.find(alert => alert.machineId === machine.id);
    if (machine.dataStale && previous) return { ...previous, stale: true };
    return {
      id: `api-${machine.backendId}`, severity: machine.status,
      machineId: machine.id, machineName: machine.name, companyName: "", unitName: "",
      occurredAt: machine.stateSince, stateSince: machine.stateSince,
      time: machine.stateSince ? new Date(machine.stateSince).toLocaleTimeString("pt-BR") : "—",
      critical: machine.status === "EMERGENCIA", stale: Boolean(machine.dataStale),
    };
  });
}

// Only confirmed observations enter the baseline, including across API outages.
export function monitoringTransitions(previous, machines) {
  const confirmed = new Map(previous.map(machine => [machine.id, machine]));
  const notices = [];
  for (const machine of machines) {
    if (machine.dataStale || machine.statusError) continue;
    const before = confirmed.get(machine.id);
    confirmed.set(machine.id, machine);
    if (!before || before.status === machine.status) continue;
    const resolved = isMonitoringProblem(before.status) && !isMonitoringProblem(machine.status);
    if (!resolved && !isMonitoringProblem(machine.status)) continue;
    const occurredAt = machine.stateSince || machine.telemetryTimestamp || new Date().toISOString();
    notices.push({ id: `transition-${machine.backendId}-${machine.status}-${occurredAt}`,
      machineId: machine.id, machineName: machine.name, severity: machine.status,
      occurredAt, resolved, companyName: "", unitName: "",
      title: resolved ? "Problema encerrado" : machine.status === "EMERGENCIA" ? "Nova emergência detectada" : "Novo alerta de máquina",
    });
  }
  return { confirmed: [...confirmed.values()].filter(machine => machines.some(current => current.id === machine.id)), notices };
}

export function monitoringWarning(machines) {
  const failures = machines.filter(machine => machine.statusError || machine.historyError || machine.utilizationError || machine.metadataError);
  return failures.length ? `Atualização parcial: ${failures.length} máquina(s) com consulta indisponível. Os estados disponíveis continuam sendo atualizados.` : null;
}
