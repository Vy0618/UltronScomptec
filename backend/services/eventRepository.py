"""Unified read view over machine events and pre-existing telemetry history.

Only this compatibility layer joins old readings to collectors. All new events
belong directly to machines. No destructive database migration is required.
"""
from types import SimpleNamespace
from sqlalchemy import select, literal, union_all, exists, case, func
from database.models import MachineEvent, Telemetry, TelemetryOrder, Device

FIELDS = ("id", "device_id", "timestamp", "received_at", "machine_active",
          "voltage_24v", "digital_signals", "analog_signals", "extra_signals")


def event_table(machine_id):
    current = select(
        *(getattr(MachineEvent, key) for key in FIELDS),
        MachineEvent.machine_id,
        case((MachineEvent.generation == 0, func.coalesce(MachineEvent.legacy_order, MachineEvent.sequence)),
             else_=MachineEvent.sequence).label("arrival_order"),
        MachineEvent.generation,
    ).where(MachineEvent.machine_id == machine_id)
    legacy = select(
        *(getattr(Telemetry, key) for key in FIELDS),
        Device.cnc_id.label("machine_id"), TelemetryOrder.id.label("arrival_order"),
        literal(0).label("generation"),
    ).join(Device).outerjoin(TelemetryOrder).where(
        Device.cnc_id == machine_id,
        ~exists(select(MachineEvent.id).where(MachineEvent.id == Telemetry.id)),
    )
    return union_all(current, legacy).subquery()


def ordered_query(table, descending=True):
    fields = (table.c.timestamp, table.c.received_at, table.c.generation, table.c.arrival_order, table.c.id)
    return select(table).order_by(*(column.desc() if descending else column.asc() for column in fields))


def observation(row):
    values = dict(row._mapping)
    values["states"] = values["digital_signals"] or {}
    return SimpleNamespace(**values)


def latest_event(db, machine_id):
    table = event_table(machine_id)
    row = db.execute(ordered_query(table).limit(1)).first()
    return observation(row) if row else None


def preserve_legacy_history(db, device):
    """Keep old machine history when a collector is removed or reassigned."""
    readings = db.scalars(select(Telemetry).outerjoin(TelemetryOrder).where(
        Telemetry.device_id == device.id,
        ~exists(select(MachineEvent.id).where(MachineEvent.id == Telemetry.id)),
    ).order_by(Telemetry.timestamp, Telemetry.received_at, TelemetryOrder.id)).all()
    for reading in readings:
        db.add(MachineEvent(machine_id=device.cnc_id, generation=0,
                            legacy_order=reading.ingestion_order.id if reading.ingestion_order else None,
                            **{key: getattr(reading, key) for key in FIELDS}))
    db.flush()
