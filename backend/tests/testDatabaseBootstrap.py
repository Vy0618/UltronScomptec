from pathlib import Path
import sys
from unittest.mock import MagicMock

import pytest
from sqlalchemy.dialects import mysql, sqlite
from sqlalchemy.engine import make_url
from sqlalchemy.exc import OperationalError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from database import connection


def configured_engine(dialect, url):
    engine = MagicMock()
    engine.dialect = dialect
    engine.url = make_url(url)
    return engine


def test_missing_mysql_database_is_created_before_tables(monkeypatch):
    engine = configured_engine(mysql.dialect(), "mysql+pymysql://user:pass@127.0.0.1/cnc-monitor")
    engine.connect.side_effect = OperationalError("connect", {}, Exception(1049, "Unknown database"))
    server_engine = MagicMock()
    server_engine.connect.return_value.execution_options.return_value.__enter__.return_value = connection_handle = MagicMock()
    created = []
    monkeypatch.setattr(connection, "engine", engine)
    monkeypatch.setattr(connection, "create_engine", lambda url, **kwargs: created.append(url) or server_engine)
    monkeypatch.setattr(connection.Base.metadata, "create_all", lambda bind: created.append(bind))

    connection.create_tables()

    assert created[0].database is None
    assert created[1] is engine
    assert connection_handle.exec_driver_sql.call_args.args[0].startswith(
        "CREATE DATABASE IF NOT EXISTS `cnc-monitor` CHARACTER SET utf8mb4"
    )
    server_engine.dispose.assert_called_once()


@pytest.mark.parametrize("dialect,url", [
    (mysql.dialect(), "mysql+pymysql://user:pass@127.0.0.1/cnc_monitor"),
    (sqlite.dialect(), "sqlite://"),
])
def test_existing_database_or_sqlite_does_not_create_database(monkeypatch, dialect, url):
    engine = configured_engine(dialect, url)
    create_server = MagicMock()
    create_tables = MagicMock()
    monkeypatch.setattr(connection, "engine", engine)
    monkeypatch.setattr(connection, "create_engine", create_server)
    monkeypatch.setattr(connection.Base.metadata, "create_all", create_tables)

    connection.create_tables()

    create_server.assert_not_called()
    create_tables.assert_called_once_with(bind=engine)


def test_mysql_auth_failure_is_not_treated_as_missing_database(monkeypatch):
    engine = configured_engine(mysql.dialect(), "mysql+pymysql://user:pass@127.0.0.1/cnc_monitor")
    engine.connect.side_effect = error = OperationalError("connect", {}, Exception(1045, "Access denied"))
    monkeypatch.setattr(connection, "engine", engine)
    create_server = MagicMock()
    monkeypatch.setattr(connection, "create_engine", create_server)

    with pytest.raises(OperationalError) as raised:
        connection.create_tables()

    assert raised.value is error
    create_server.assert_not_called()
