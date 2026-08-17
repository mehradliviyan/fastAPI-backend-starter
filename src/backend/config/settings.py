from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvironment(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"

class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormat(StrEnum):
    CONSOLE = "console"
    JSON = "json"
    
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        case_sensitive=False,
        extra="ignore",
        frozen=True,
    )

    name: str = "Backend Starter"
    version: str = "0.1.0"
    environment: AppEnvironment = AppEnvironment.DEVELOPMENT
    debug: bool = False
    log_level: LogLevel = LogLevel.INFO
    log_format: LogFormat = LogFormat.CONSOLE