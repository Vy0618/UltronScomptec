export const CNC_SIGNALS = Object.freeze([
  { key: "ativo", label: "Em execução" },
  { key: "inativo", label: "Parada" },
  { key: "emergencia", label: "Emergência" },
  { key: "motor_ligado", label: "Motor ligado" },
  { key: "porta_aberta", label: "Porta aberta" },
  { key: "alarme", label: "Alerta / erro" },
]);

export function machineActiveFromStates(states = {}, fallback = false) {
  const digital = Object.fromEntries(
    Object.entries(states).map(([key, value]) => [key.toLowerCase(), value]),
  );
  if (digital.inativo === true) return false;
  if (Object.hasOwn(digital, "ativo")) return digital.ativo === true;
  return Boolean(
    fallback ||
    ["em_execucao", "ciclo", "cycle"].some((key) => digital[key] === true),
  );
}

// Preserve additional producer-defined states without knowing the source hardware.
export function observedStates(states = {}) {
  const known = new Set(CNC_SIGNALS.map((item) => item.key));
  return [
    ...CNC_SIGNALS,
    ...Object.keys(states)
      .filter((key) => !known.has(key))
      .map((key) => ({ key, label: key })),
  ];
}
