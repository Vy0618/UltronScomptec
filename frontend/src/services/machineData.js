import { buildTelemetryBuffer, markStale, readAnalog } from "./telemetry.js";

const errorText = result => result.status === "rejected" ? result.reason?.message || "Consulta indisponível" : null;

// A failed optional query must not discard a current machine status.
export async function loadMachines(request, previous = []) {
  const cncs = await request("/cncs");
  return Promise.all(cncs.map(async cnc => {
    const cached = previous.find(machine => machine.backendId === cnc.id);
    const [statusResult, historyResult, utilizationResult] = await Promise.allSettled([
      request(`/cncs/${cnc.id}/status`), request(`/cncs/${cnc.id}/history?limit=100`),
      request(`/cncs/${cnc.id}/utilization`),
    ]);
    const metadata = {
      id: cnc.code, backendId: cnc.id, name: cnc.name, description: cnc.description,
      historyError: errorText(historyResult), utilizationError: errorText(utilizationResult),
      statusError: errorText(statusResult),
    };
    const history = historyResult.status === "fulfilled" ? historyResult.value : null;
    const readings = history?.items ?? cached?.readings ?? [];
    const shared = {
      ...metadata, readings, historyTotal: history?.total ?? cached?.historyTotal ?? 0,
      telemetryBuffer: buildTelemetryBuffer(readings),
      utilization: utilizationResult.status === "fulfilled" ? utilizationResult.value : cached?.utilization,
    };
    if (statusResult.status === "rejected") {
      const fallback = cached || { current: null, voltage: null, temperature: null, powerKw: null,
        digitalSignals: {}, sensors: [], stateSince: null, lastCommunicationAt: null };
      return { ...markStale([fallback])[0], ...shared };
    }
    const status = statusResult.value;
    const analog = status.analog_signals || {};
    return {
      ...shared, status: status.status, state: status.status, dataStale: false,
      lastKnownStatus: status.last_known_status, stateSince: status.status_since,
      lastCommunicationAt: status.last_seen,
      communicationStatus: status.online ? "ONLINE" : "OFFLINE",
      current: readAnalog(analog, "current", "corrente"),
      voltage: readAnalog(analog, "voltage", "tensao"),
      temperature: readAnalog(analog, "temperature", "temperatura"),
      powerKw: readAnalog(analog, "power_kw", "powerKw", "potencia_kw"),
      currentLimit: 22, temperatureLimit: 65, powerAvg: null,
      digitalSignals: status.states || {}, voltage24v: status.voltage_24v,
      telemetryTimestamp: status.telemetry_timestamp,
      sensors: [...Object.keys(status.states || {}), ...Object.keys(analog)],
    };
  }));
}
