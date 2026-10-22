"""Optional real-MySQL checks, restricted to an explicitly named local test DB.

Set ULTRON_TEST_MYSQL_URL to mysql+pymysql://...@127.0.0.1:3307/ultron_test.
The normal DATABASE_URL is never used by these tests.
"""
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import sys
from threading import Barrier
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from database.models import Base, CNC, Device, Telemetry
from schemas.device import DeviceRegistration
from schemas.telemetry import TelemetryCreate
from services.clock import utcnow
from services.deviceService import register_device
from services.telemetry import create_telemetry


@pytest.fixture
def mysql_engine():
    value = os.getenv("ULTRON_TEST_MYSQL_URL")
    if not value:
        pytest.skip("ULTRON_TEST_MYSQL_URL ausente: teste opcional exige MySQL local isolado")
    url = make_url(value)
    if url.get_backend_name() != "mysql" or url.host not in {"127.0.0.1", "localhost", "::1"} or not (url.database or "").startswith("ultron_test"):
        pytest.fail("ULTRON_TEST_MYSQL_URL deve apontar para MySQL local e banco ultron_test...")
    engine = create_engine(url, pool_pre_ping=True, pool_size=10, max_overflow=0)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


def unique_mac():
    return "02:" + ":".join(f"{byte:02X}" for byte in uuid4().bytes[:5])


def remove_test_devices(engine, macs):
    # Remove only the synthetic pairs created by the current test; never drop tables.
    with Session(engine) as db:
        devices = db.scalars(select(Device).where(Device.mac_address.in_(macs))).all()
        for device in devices:
            db.delete(device.cnc)
        db.commit()


def concurrent_calls(action, count=8):
    barrier = Barrier(count)
    def worker(index):
        barrier.wait(timeout=30)
        return action(index)
    with ThreadPoolExecutor(max_workers=count) as executor:
        return list(executor.map(worker, range(count)))


def test_mysql_concurrent_same_mac_provisions_one_pair(mysql_engine):
    mac = unique_mac()
    def provision(_):
        with Session(mysql_engine) as db:
            response = register_device(DeviceRegistration(mac_address=mac, firmware_version="SIMULACAO-concurrency"), db)
            return response.device.id, response.cnc.id
    try:
        pairs = concurrent_calls(provision)
        assert len(set(pairs)) == 1
        with Session(mysql_engine) as db:
            assert db.scalar(select(func.count()).select_from(Device).where(Device.mac_address == mac)) == 1
    finally:
        remove_test_devices(mysql_engine, [mac])


def test_mysql_concurrent_new_devices_get_unique_codes(mysql_engine):
    macs = [unique_mac() for _ in range(8)]
    def provision(index):
        with Session(mysql_engine) as db:
            response = register_device(DeviceRegistration(mac_address=macs[index], firmware_version="SIMULACAO-concurrency"), db)
            return response.device.code, response.cnc.code
    try:
        codes = concurrent_calls(provision)
        assert len({device for device, cnc in codes}) == 8
        assert len({cnc for device, cnc in codes}) == 8
    finally:
        remove_test_devices(mysql_engine, macs)


def test_mysql_same_event_concurrently_is_persisted_once(mysql_engine):
    mac = unique_mac()
    with Session(mysql_engine) as db:
        response = register_device(DeviceRegistration(mac_address=mac, firmware_version="SIMULACAO-concurrency"), db)
        device_id = response.device.id
    payload = TelemetryCreate(event_id=str(uuid4()) + ":1", timestamp=utcnow(), machine_active=True,
                              voltage_24v=None, digital_signals={"ciclo": True}, analog_signals={})
    def send(_):
        with Session(mysql_engine) as db:
            return create_telemetry(device_id, payload, db).id
    try:
        ids = concurrent_calls(send)
        assert len(set(ids)) == 1
        with Session(mysql_engine) as db:
            assert db.scalar(select(func.count()).select_from(Telemetry).where(Telemetry.device_id == device_id)) == 1
    finally:
        remove_test_devices(mysql_engine, [mac])
