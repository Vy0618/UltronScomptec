export const CNC_SIGNALS = Object.freeze([
  { key: "em_execucao", label: "Em execução" },
  { key: "pausa", label: "Pausa" },
  { key: "parada", label: "Parada" },
  { key: "emergencia", label: "Emergência" },
  { key: "motor_ligado", label: "Motor ligado" },
  { key: "automatico", label: "Automático" },
  { key: "manual", label: "Manual" },
  { key: "alarme", label: "Alarme / erro" },
]);

// Preserve additional producer-defined states without knowing the source hardware.
export function observedStates(states = {}) {
  const known = new Set(CNC_SIGNALS.map(item => item.key));
  return [...CNC_SIGNALS, ...Object.keys(states).filter(key => !known.has(key))
    .map(key => ({ key, label: key }))];
}
