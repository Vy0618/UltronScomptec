"""Interpret observed machine states independently of their producer."""


def machine_active_from_states(states, fallback=False) -> bool:
    """Explicit activity signals take precedence; never infer a missing complement."""
    digital = {str(key).lower(): value for key, value in (states or {}).items()}
    if digital.get("inativo") is True:
        return False
    if "ativo" in digital:
        return digital["ativo"] is True
    return bool(fallback or any(digital.get(key) is True for key in ("em_execucao", "ciclo", "cycle")))


def derive_diagnostics(states) -> list[dict]:
    """Describe combinations in one complete observation, without changing raw signals."""
    digital = {str(key).lower(): value for key, value in (states or {}).items()}
    diagnostics = []
    if digital.get("porta_aberta") is True and (digital.get("emergencia") is True or digital.get("emergency") is True):
        diagnostics.append({
            "code": "PORTA_ABERTA_EMERGENCIA", "severity": "EMERGENCIA",
            "title": "Operação falha",
            "message": "Porta aberta e emergência acionada na mesma leitura.",
            "signals": ["porta_aberta", "emergencia"],
        })
    if digital.get("ativo") is True and digital.get("inativo") is True:
        diagnostics.append({
            "code": "ATIVIDADE_CONFLITANTE", "severity": "ALARME",
            "title": "Sinais de atividade conflitantes",
            "message": "Ativo e inativo estão acionados na mesma leitura.",
            "signals": ["ativo", "inativo"],
        })
    return diagnostics


def derive_status(data) -> str:
    digital = {str(key).lower(): value for key, value in (data.digital_signals or {}).items()}
    if data.voltage_24v is False:
        return "DESLIGADA"
    if digital.get("emergencia") or digital.get("emergency"):
        return "EMERGENCIA"
    if digital.get("alarme") or digital.get("alarm"):
        return "ALARME"
    if digital.get("manutencao") or digital.get("maintenance"):
        return "MANUTENCAO"
    if machine_active_from_states(digital, data.machine_active):
        return "OPERANDO"
    return "PARADA"

