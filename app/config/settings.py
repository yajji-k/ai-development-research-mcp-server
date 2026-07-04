from enum import Enum
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Transport(str, Enum):
    """Supported MCP server transports."""

    STDIO = "stdio"
    HTTP = "http"


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.

    Defaults are provided for local development and can be overridden
    using environment variables or a .env file.
    """

    server_name: str = "MCP Server"
    server_version: str = "0.1.0"
    log_level: str = "INFO"

    transport: Transport = Transport.STDIO
    http_host: str = "0.0.0.0"
    http_port: int = 8000

    api_key: str = "change-me"
    workspace_root: Path = Path.cwd()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    The settings are loaded once and reused throughout the application.
    """
    return Settings()
