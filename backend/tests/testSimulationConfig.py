from pathlib import Path
import runpy
import json
import os

import pytest

import dotenv


def test_simulation_skips_dotenv_while_normal_startup_preserves_loading(monkeypatch):
    """Inspect the loader call without creating or reading a real .env file."""
    config_path = Path(__file__).resolve().parents[1] / "config.py"
    calls = []
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: calls.append((args, kwargs)))
    monkeypatch.setenv("ULTRON_SIMULATION", "true")
    config = runpy.run_path(str(config_path))
    assert calls == []
    # Prevent the real config.json from adding untracked process variables.
    for key in config["CONFIG_KEYS"]:
        if key not in os.environ:
            monkeypatch.setenv(key, "")
    monkeypatch.delenv("ULTRON_SIMULATION")
    runpy.run_path(str(config_path))
    assert calls == [((config_path.parent / ".env",), {"override": False})]


def test_json_config_fills_only_missing_environment_values(tmp_path, monkeypatch):
    config_path = Path(__file__).resolve().parents[1] / "config.py"
    example = json.loads((config_path.parent / "config.example.json").read_text())
    local = tmp_path / "config.json"
    local.write_text(json.dumps({**example, "DATABASE_URL": "sqlite:///from-json.db",
                                 "SQL_ECHO": True, "DEVICE_OFFLINE_TIMEOUT_SECONDS": 15}))
    monkeypatch.setenv("ULTRON_SIMULATION", "true")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///from-environment.db")
    for key in ("SQL_ECHO", "DEVICE_OFFLINE_TIMEOUT_SECONDS", "ADMIN_EMAIL"):
        monkeypatch.delenv(key, raising=False)
    loader = runpy.run_path(str(config_path))["load_json_config"]
    loader(local)
    assert os.environ["DATABASE_URL"] == "sqlite:///from-environment.db"
    assert os.environ["SQL_ECHO"] == "true"
    assert os.environ["DEVICE_OFFLINE_TIMEOUT_SECONDS"] == "15"
    assert os.environ["ADMIN_EMAIL"] == ""
    monkeypatch.setenv("SQL_ECHO", "false")
    loader(local)
    assert os.environ["SQL_ECHO"] == "false"


def test_invalid_json_config_stops_startup(tmp_path):
    config_path = Path(__file__).resolve().parents[1] / "config.py"
    loader = runpy.run_path(str(config_path))["load_json_config"]
    local = tmp_path / "config.json"
    local.write_text('{"UNEXPECTED_KEY": "value"}')
    with pytest.raises(RuntimeError, match="chaves desconhecidas"):
        loader(local)
    local.write_text('{invalid')
    with pytest.raises(RuntimeError, match="Configuração JSON inválida"):
        loader(local)
