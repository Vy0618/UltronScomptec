import { useMemo, useRef } from "react";
import api from "../services/api";
import { buildTelemetryBuffer } from "../services/telemetry";
import { useApiQuery } from "./useApiQuery";

export function useMachineHistory(machine, demoMode) {
  const id = machine?.backendId;
  const query = useApiQuery(
    !demoMode && id ? `history:${id}` : null,
    (signal) => api.getMachineHistory(id, { limit: 100 }, { signal }),
    10000,
  );
  const readings = query.data?.items;
  const telemetryBuffer = useMemo(
    () => (readings ? buildTelemetryBuffer(readings) : []),
    [readings],
  );
  return {
    ...query,
    machine: demoMode
      ? machine
      : machine && {
          ...machine,
          readings: readings || [],
          telemetryBuffer,
          historyError: query.error,
        },
  };
}

export function useFleetUtilization(machines, demoMode) {
  const ids = machines.map((machine) => machine.backendId).filter(Boolean);
  const previous = useRef(new Map());
  const query = useApiQuery(
    !demoMode && ids.length ? `utilization:${ids.join(",")}` : null,
    async (signal) => {
      const queue = [...ids];
      const result = new Map();
      // Do not flood either the browser's connection pool or the database.
      await Promise.all(
        Array.from({ length: Math.min(4, ids.length) }, async () => {
          while (queue.length && !signal.aborted) {
            const id = queue.shift();
            try {
              const utilization = await api.getMachineUtilization(id, {
                signal,
              });
              result.set(id, { utilization });
            } catch (error) {
              if (signal.aborted) throw error;
              result.set(id, {
                utilization: previous.current.get(id)?.utilization,
                utilizationError: error.message,
              });
            }
          }
        }),
      );
      previous.current = result;
      return result;
    },
    60000,
  );
  if (query.data) previous.current = query.data;
  const enriched = useMemo(
    () =>
      demoMode
        ? machines
        : machines.map((machine) => ({
            ...machine,
            ...query.data?.get(machine.backendId),
          })),
    [machines, demoMode, query.data],
  );
  const partial = enriched.some((machine) => machine.utilizationError);
  return {
    ...query,
    machines: enriched,
    error:
      query.error ||
      (partial
        ? "Parte do histórico não pôde ser atualizada. Exibindo os últimos dados disponíveis."
        : null),
  };
}
