"""Time-weighted utilization; a sample is valid only until the offline timeout."""
from datetime import timedelta

from services.clock import OFFLINE_TIMEOUT_SECONDS, normalize_datetime
from services.machineState import IHM_SIGNALS, derive_status
from schemas.observation import Observation

STATES = ("OPERANDO", "PARADA", "ALARME", "EMERGENCIA", "MANUTENCAO", "DESLIGADA")


def calculate_utilization(readings, now, hours=24, timeout=OFFLINE_TIMEOUT_SECONDS):
    now = normalize_datetime(now)
    start = now - timedelta(hours=hours)
    buckets = [{
        "timestamp": (start + timedelta(hours=i)).isoformat() + "Z",
        "seconds": {state: 0.0 for state in STATES},
        "failure_causes": {signal: 0 for signal in IHM_SIGNALS},
        "samples": 0,
        "duration_seconds": 3600,
    } for i in range(hours)]
    # The query orders ties by ingestion; the final sample at a timestamp wins.
    readings = sorted(readings, key=lambda reading: reading.timestamp)
    previous_faults = set()
    previous_timestamp = None
    for index, reading in enumerate(readings):
        timestamp = normalize_datetime(reading.timestamp)
        if start <= timestamp <= now:
            bucket = min(hours - 1, int((timestamp - start).total_seconds() // 3600))
            buckets[bucket]["samples"] += 1
        # Only the final observation at a timestamp describes the state there.
        if index + 1 < len(readings) and normalize_datetime(readings[index + 1].timestamp) == timestamp:
            continue
        state = derive_status(Observation(
            machine_active=reading.machine_active,
            voltage_24v=reading.voltage_24v,
            digital_signals=reading.digital_signals or {},
        ))
        digital = {str(key).lower(): value for key, value in (reading.digital_signals or {}).items()}
        for canonical, alias in (("emergencia", "emergency"), ("alarme", "alarm")):
            if digital.get(alias) is True:
                digital[canonical] = True
        faults = {signal for signal in IHM_SIGNALS if digital.get(signal) is True} if state == "EMERGENCIA" else set()
        continuous = previous_timestamp is not None and timestamp - previous_timestamp <= timedelta(seconds=timeout)
        if start <= timestamp <= now:
            for signal in faults - (previous_faults if continuous else set()):
                buckets[bucket]["failure_causes"][signal] += 1
        previous_faults, previous_timestamp = faults, timestamp
        end = min(now, timestamp + timedelta(seconds=timeout))
        if index + 1 < len(readings):
            end = min(end, normalize_datetime(readings[index + 1].timestamp))
        cursor = max(start, timestamp)
        if cursor >= end:
            continue
        while cursor < end:
            bucket = int((cursor - start).total_seconds() // 3600)
            segment_end = min(end, start + timedelta(hours=bucket + 1))
            buckets[bucket]["seconds"][state] += (segment_end - cursor).total_seconds()
            cursor = segment_end
    return {"buckets": buckets, "as_of": now.isoformat() + "Z"}
