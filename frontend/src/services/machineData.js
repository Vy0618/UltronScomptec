import { buildTelemetryBuffer, markStale, readAnalog } from "./telemetry.js";

const errorText = result => result.status === "rejected" ? result.reason?.message || "Consulta indisponível" : null;

// A failed optional query must not discard a current machine status.
export async function loadMachines(request, previous = []) {
  const [cncsResult, devicesResult] = await Promise.allSettled([request("/cncs"), request("/devices")]);
  if (cncsResult.status === "rejected") throw cncsResult.reason;
  const devices = devicesResult.status === "fulfilled" ? devicesResult.value : [];
  return Promise.all(cncsResult.value.map(async cnc => {
    const cached = previous.find(machine => machine.backendId === cnc.id);
    const [statusResult, historyResult, utilizationResult] = await Promise.allSettled([
      request(`/cncs/${cnc.id}/status`), request(`/cncs/${cnc.id}/history?limit=100`),
      request(`/cncs/${cnc.id}/utilization`),
    ]);
    const device = devices.find(item => item.cnc_id === cnc.id);
    const metadataValue = (key, cachedKey) => devicesResult.status === "fulfilled" ? device?.[key] : cached?.[cachedKey];
    const metadata = {
      id: cnc.code, backendId: cnc.id, name: cnc.name, description: cnc.description,
      deviceId: metadataValue("code", "deviceId"),
      deviceBackendId: metadataValue("id", "deviceBackendId"),
      firmwareVersion: metadataValue("firmware_version", "firmwareVersion"),
      ipAddress: metadataValue("ip_address", "ipAddress"),
      macAddress: metadataValue("mac_address", "macAddress"),
      metadataError: errorText(devicesResult),
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
      communicationStatus: status.gateway_online ? "ONLINE" : "OFFLINE",
      current: readAnalog(analog, "current", "corrente"),
      voltage: readAnalog(analog, "voltage", "tensao"),
      temperature: readAnalog(analog, "temperature", "temperatura"),
      powerKw: readAnalog(analog, "power_kw", "powerKw", "potencia_kw"),
      currentLimit: 22, temperatureLimit: 65, powerAvg: null,
      digitalSignals: status.digital_signals || {}, voltage24v: status.voltage_24v,
      mesa: status.extra_signals?.mesa ?? null, telemetryBootId: status.extra_signals?.boot_id ?? null,
      rssi: status.extra_signals?.rssi ?? null, uptimeSeconds: status.extra_signals?.uptime_seconds ?? null,
      telemetryTimestamp: status.telemetry_timestamp,
      sensors: [...Object.keys(status.digital_signals || {}), ...Object.keys(analog)],
    };
  }));
}
