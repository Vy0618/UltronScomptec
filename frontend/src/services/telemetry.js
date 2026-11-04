import { machineActiveFromStates } from "./cncSignals.js";

// Pure transformations shared by monitoring and its regression tests.
export function readAnalog(signals, ...keys) {
  for (const key of keys) {
    const value = signals?.[key];
    if (typeof value === "number" && Number.isFinite(value)) return value;
  }
  return null;
}

export function buildTelemetryBuffer(readings = []) {
  return [
    ...new Map(
      readings.map((reading) => [reading.id ?? reading.timestamp, reading]),
    ).values(),
  ]
    .filter((reading) => Number.isFinite(Date.parse(reading.timestamp)))
    .sort((a, b) => Date.parse(a.timestamp) - Date.parse(b.timestamp))
    .slice(-100)
    .map((reading) => ({
      timestamp: Date.parse(reading.timestamp),
      time: new Date(reading.timestamp).toLocaleTimeString("pt-BR"),
      current: readAnalog(reading.analog_signals, "current", "corrente"),
      voltage: readAnalog(reading.analog_signals, "voltage", "tensao"),
      temperature: readAnalog(
        reading.analog_signals,
        "temperature",
        "temperatura",
      ),
      powerKw: readAnalog(
        reading.analog_signals,
        "power_kw",
        "powerKw",
        "potencia_kw",
      ),
      machineActive:
        typeof reading.machine_active === "boolean"
          ? Number(reading.machine_active)
          : null,
      digital: Object.fromEntries(
        Object.entries(reading.states || reading.digital_signals || {}).map(
          ([key, value]) => [
            key,
            typeof value === "boolean" ? Number(value) : null,
          ],
        ),
      ),
    }));
}

export function readingStatus(reading) {
  const digital = Object.fromEntries(
    Object.entries(reading.states || reading.digital_signals || {}).map(
      ([key, value]) => [key.toLowerCase(), value],
    ),
  );
  if (reading.voltage_24v === false) return "DESLIGADA";
  if (digital.emergencia || digital.emergency) return "EMERGENCIA";
  if (digital.alarme || digital.alarm) return "ALARME";
  if (digital.manutencao || digital.maintenance) return "MANUTENCAO";
  if (machineActiveFromStates(digital, reading.machine_active))
    return "OPERANDO";
  return "PARADA";
}

export function readingEvent(reading, machine) {
  const status = readingStatus(reading);
  return {
    id: `telemetry-${reading.id}`,
    machineId: machine.id,
    machineName: machine.name,
    type: "TELEMETRY_SAMPLE",
    status,
    occurredAt: reading.timestamp,
    time: new Date(reading.timestamp).toLocaleTimeString("pt-BR"),
    text: `Leitura recebida: ${status}`,
    isActive: false,
    signalOutputs: reading.signal_outputs || [],
  };
}

export function markStale(machines) {
  return machines.map((machine) => ({
    ...machine,
    lastKnownStatus: machine.dataStale
      ? machine.lastKnownStatus
      : machine.status,
    status: "DADOS_DESATUALIZADOS",
    state: "DADOS_DESATUALIZADOS",
    communicationStatus: "UNKNOWN",
    dataStale: true,
  }));
}

// Schedule only after completion: requests never overlap and errors keep retrying.
export function startPolling(
  refresh,
  onError,
  interval = 5000,
  environment = globalThis.document,
) {
  let stopped = false;
  let timer;
  let running = false;
  let controller;
  async function run() {
    if (stopped || running || environment?.hidden) return;
    clearTimeout(timer);
    running = true;
    controller = new AbortController();
    try {
      await refresh(() => stopped, controller.signal);
    } catch (error) {
      if (!stopped) onError(error);
    } finally {
      running = false;
      if (!stopped) timer = setTimeout(run, interval);
    }
  }
  const visible = () => {
    if (!environment.hidden) run();
    else clearTimeout(timer);
  };
  environment?.addEventListener("visibilitychange", visible);
  run();
  return () => {
    stopped = true;
    clearTimeout(timer);
    controller?.abort();
    environment?.removeEventListener("visibilitychange", visible);
  };
}
