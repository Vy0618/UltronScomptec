import { useMonitoring } from "../contexts/monitoringContext";

export function useMachines() {
  const { machines, loading, connectionError } = useMonitoring();
  return { machines, loading, error: connectionError, reload: () => {} };
}
export function useMachine(id) {
  const { allMachines, loading, connectionError } = useMonitoring();
  return {
    machine:
      allMachines.find(
        (machine) => machine.id === id || machine.backendId === id,
      ) || null,
    loading,
    error: connectionError,
  };
}
export function useDashboardSummary() {
  const { scopeSummary } = useMonitoring();
  return {
    summary: {
      ...scopeSummary,
      alarmsAndEmergencies: scopeSummary.alarms + scopeSummary.emergencies,
    },
    loading: false,
  };
}
