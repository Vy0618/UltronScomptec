import UtilizationChart from "./utilizationChart";
import { useFleetUtilization } from "../../hooks/useMachineResources";
import { utilizationSeries } from "../../data/mockData";

export default function FleetHealth({ machines, demoMode, loading, error }) {
  const query = useFleetUtilization(machines, demoMode);
  return (
    <UtilizationChart
      machines={query.machines}
      data={demoMode ? utilizationSeries : undefined}
      loading={loading || query.loading}
      error={error || query.error}
    />
  );
}
