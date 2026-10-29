"""Interpret observed machine states independently of their producer."""


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
    if data.machine_active or digital.get("em_execucao") or digital.get("ciclo") or digital.get("cycle"):
        return "OPERANDO"
    return "PARADA"

