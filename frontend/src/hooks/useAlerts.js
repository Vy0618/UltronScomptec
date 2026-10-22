import { useMonitoring } from "../contexts/monitoringContext";
export function useAlerts() { const { alerts, loading, connectionError, dataWarning } = useMonitoring(); return { alerts, loading, error: connectionError || dataWarning, reload: () => {} }; }
