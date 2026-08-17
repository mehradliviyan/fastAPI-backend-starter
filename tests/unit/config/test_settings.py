import pytest

from backend.config.settings import LogFormat, LogLevel, Settings


def test_settings_read_logging_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("APP_LOG_FORMAT", "json")

    settings = Settings(_env_file=None)

    assert settings.log_level is LogLevel.DEBUG
    assert settings.log_format is LogFormat.JSON