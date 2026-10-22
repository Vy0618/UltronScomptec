import os

import config  # Também permite importar o banco diretamente com o .env carregado.

from sqlalchemy import create_engine, event
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.models import Base

# Exemplo: mysql+pymysql://root:SUA_SENHA@127.0.0.1:3306/cnc_monitor
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:@127.0.0.1:3306/cnc_monitor?charset=utf8mb4",
)

engine_options = {"echo": os.getenv("SQL_ECHO", "false").lower() == "true", "pool_pre_ping": True, "pool_recycle": 1800}
if DATABASE_URL.startswith("sqlite:"):
    # Optional local simulation only; the default above remains MySQL.
    engine_options["connect_args"] = {"check_same_thread": False}
    if DATABASE_URL in {"sqlite://", "sqlite:///:memory:"}:
        engine_options["poolclass"] = StaticPool
engine = create_engine(DATABASE_URL, **engine_options)
if engine.dialect.name == "sqlite":
    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def create_tables():
    if engine.dialect.name == "mysql":
        try:
            with engine.connect():
                pass
        except OperationalError as error:
            # PyMySQL 1049: Unknown database. Other connection errors must surface.
            if not error.orig.args or error.orig.args[0] != 1049:
                raise
            database_name = engine.url.database
            if not database_name:
                raise
            url = engine.url
            server_url = URL.create(
                drivername=url.drivername, username=url.username, password=url.password,
                host=url.host, port=url.port, query=url.query,
            )
            server_engine = create_engine(server_url, pool_pre_ping=True)
            try:
                quoted_name = engine.dialect.identifier_preparer.quote(database_name)
                with server_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
                    connection.exec_driver_sql(
                        f"CREATE DATABASE IF NOT EXISTS {quoted_name} "
                        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                    )
            finally:
                server_engine.dispose()
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
