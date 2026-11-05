"""Human-readable outputs from a single observation; raw inputs stay unchanged."""
from math import isfinite

from services.machineState import IHM_SIGNALS, derive_diagnostics, machine_active_from_states

SIGNALS = IHM_SIGNALS
LABELS = ("ativo", "inativo", "emergência", "motor ligado", "alarme / erro", "porta aberta")
FAULT_LABELS = {
    "ativo": "Falha na execução",
    "inativo": "Falha na parada",
    "emergencia": "Falha na emergência",
    "motor_ligado": "Falha no motor",
    "alarme": "Falha no alarme / erro",
    "porta_aberta": "Falha na porta",
}
LEVEL_ORDER = {"critical": 0, "attention": 1, "info": 2}

PAIRS = (
    ("EMERGENCIA_COM_ALARME", ("emergencia", "alarme"), "critical", "Emergência e alarme simultâneos", "Os dois sinais estão em 1 e indicam emergência."),
    ("EMERGENCIA_COM_ATIVIDADE", ("emergencia", "ativo"), "critical", "Emergência com atividade informada", "Ativo e emergência foram recebidos juntos em 1 e indicam emergência."),
    ("ALARME_COM_ATIVIDADE", ("alarme", "ativo"), "attention", "Atividade com alarme", "Ativo e alarme estão em 1 e indicam emergência."),
    ("ALARME_COM_INATIVIDADE", ("alarme", "inativo"), "attention", "Inatividade com alarme", "Inativo e alarme estão em 1 e indicam emergência."),
    ("PORTA_ABERTA_COM_ALARME", ("porta_aberta", "alarme"), "attention", "Porta aberta com alarme", "Porta aberta e alarme foram recebidos juntos em 1 e indicam emergência."),
    ("ATIVIDADE_COM_PORTA_ABERTA", ("ativo", "porta_aberta"), "attention", "Atividade com porta aberta", "Os sinais ativo e porta aberta estão em 1 e indicam emergência."),
    ("INATIVIDADE_COM_PORTA_ABERTA", ("inativo", "porta_aberta"), "info", "Inatividade com porta aberta", "Inativo e porta aberta estão em 1 e indicam emergência."),
    ("ATIVIDADE_COM_MOTOR", ("ativo", "motor_ligado"), "info", "Atividade com motor ligado", "Ativo e motor ligado estão em 1 e indicam emergência."),
    ("INATIVIDADE_COM_MOTOR", ("inativo", "motor_ligado"), "info", "Inatividade com motor ligado", "Inativo e motor ligado estão acionados. Motor ligado isoladamente não confirma execução."),
)


def derive_signal_outputs(data) -> list[dict]:
    if data is None:
        return []
    digital = {str(key).lower(): value for key, value in (data.digital_signals or {}).items()}
    for canonical, alias in (("emergencia", "emergency"), ("alarme", "alarm")):
        # Match status priority: an asserted legacy alias must remain visible
        # even when a producer also sends the canonical signal as false.
        if digital.get(alias) is True:
            digital[canonical] = True
        elif canonical not in digital and isinstance(digital.get(alias), bool):
            digital[canonical] = digital[alias]
    outputs = []

    def add(code, level, title, message, signals):
        outputs.append({"code": code, "level": level, "title": title, "message": message, "signals": list(signals)})

    for diagnostic in derive_diagnostics(digital):
        add(diagnostic["code"], "critical" if diagnostic["severity"] == "EMERGENCIA" else "attention",
            diagnostic["title"], diagnostic["message"], diagnostic["signals"])
    for code, signals, level, title, message in PAIRS:
        if all(digital.get(signal) is True for signal in signals):
            add(code, level, title, message, signals)

    singles = (
        ("emergencia", "EMERGENCIA_ACIONADA", "critical", "Emergência acionada", "O sinal de emergência está acionado. Não há combinação adicional reconhecida para esse sinal."),
        ("alarme", "ALARME_ACIONADO", "attention", "Alarme / erro acionado", "O sinal de alarme / erro está acionado."),
        ("ativo", "ATIVIDADE_INFORMADA", "info", "Atividade informada", "O sinal ativo está acionado; os demais sinais recebidos continuam preservados."),
        ("inativo", "INATIVIDADE_INFORMADA", "info", "Inatividade informada", "O sinal inativo está acionado. Inatividade não significa máquina desligada."),
        ("motor_ligado", "MOTOR_SEM_ATIVIDADE_CONFIRMADA", "info", "Motor ligado sem atividade confirmada", "Motor ligado isoladamente não comprova atividade da máquina."),
        ("porta_aberta", "PORTA_ABERTA", "info", "Porta aberta", "O sinal de porta aberta está acionado e indica emergência pela regra dos parâmetros da IHM."),
    )
    for signal, code, level, title, message in singles:
        if digital.get(signal) is True and not any(signal in output["signals"] for output in outputs):
            add(code, level, title, message, (signal,))

    if all(digital.get(signal) is False for signal in SIGNALS):
        add("SEM_SINAIS_ACIONADOS", "info", "Máquina operando: parâmetros da IHM em 0", "Os seis parâmetros da IHM foram recebidos em 0. A máquina está operando.", SIGNALS)
    missing = [label for signal, label in zip(SIGNALS, LABELS) if not isinstance(digital.get(signal), bool)]
    if missing:
        add("SINAIS_NAO_INFORMADOS", "info", "Leitura parcial dos sinais", "Não informados: " + ", ".join(missing) + ". Ausência não significa sinal desacionado.",
            [signal for signal in SIGNALS if not isinstance(digital.get(signal), bool)])
    if "ativo" not in digital and machine_active_from_states(digital, getattr(data, "machine_active", False)):
        add("ATIVIDADE_LEGADA", "info", "Atividade no formato anterior", "A execução foi informada pelo indicador de atividade ou por um nome legado; o sinal ativo não foi fabricado.",
            [key for key in ("em_execucao", "ciclo", "cycle") if digital.get(key) is True])

    analog = getattr(data, "analog_signals", None) or {}
    current = next((analog[key] for key in ("current", "corrente") if isinstance(analog.get(key), (int, float))
                    and not isinstance(analog[key], bool) and isfinite(analog[key]) and analog[key] >= 0), None)
    if current is not None:
        source = (getattr(data, "extra_signals", None) or {}).get("current_input")
        simulated = isinstance(source, dict) and source.get("source") == "simulated"
        origin = "simulada" if simulated else "recebida; origem física não confirmada"
        if digital.get("inativo") is True:
            code, title, condition = "CORRENTE_COM_INATIVIDADE", "Corrente com inatividade informada", "O valor não substitui o sinal inativo nem confirma execução."
        elif machine_active_from_states(digital, getattr(data, "machine_active", False)):
            code, title, condition = "CORRENTE_COM_ATIVIDADE", "Corrente com atividade informada", "O valor não modifica a prioridade do estado operacional."
        else:
            code, title, condition = "CORRENTE_RECEBIDA", "Corrente recebida", "O valor isolado não comprova atividade da máquina."
        add(code, "info", title, f"Corrente {current:g} A ({origin}). {condition}", ("current",))
    asserted = [signal for signal in SIGNALS if digital.get(signal) is True]
    if asserted:
        labels = dict(zip(SIGNALS, LABELS))
        parameters = ", ".join(f"{labels[signal]} ({signal})" for signal in asserted)
        outputs.insert(0, {
            "code": "PARAMETROS_IHM_ACIONADOS", "level": "critical",
            "title": "; ".join(FAULT_LABELS[signal] for signal in asserted),
            "message": f"Parâmetros da IHM em 1: {parameters}. Qualquer parâmetro em 1 indica emergência.",
            "signals": asserted,
        })
    return sorted(outputs, key=lambda output: LEVEL_ORDER[output["level"]])
