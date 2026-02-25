"""Configuration for Porkbun Domain MCP server.

Uses Oneiric for layered configuration and structured logging:
- Configuration: YAML files + environment variables
- Logging: structlog with JSON output

Configuration loading order (later overrides earlier):
1. Default values in field definitions
2. settings/porkbun-domain.yaml (committed, for production defaults)
3. settings/local.yaml (gitignored, for development)
4. Environment variables PORKBUN_DOMAIN_{FIELD}
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import httpx
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Oneiric logging imports
try:
    from oneiric.core.logging import LoggingConfig, configure_logging, get_logger

    ONEIRIC_LOGGING_AVAILABLE = True
except ImportError:
    ONEIRIC_LOGGING_AVAILABLE = False
    import logging

    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

    def configure_logging(*args: Any, **kwargs: Any) -> None:
        logging.basicConfig(level=logging.INFO)


class PorkbunDomainSettings(BaseSettings):
    """Settings for Porkbun Domain MCP server.

    Uses pydantic-settings for environment variable support with
    Oneiric-style layered configuration.

    Attributes:
        api_key: Porkbun API key (from PORKBUN_DOMAIN_API_KEY env var)
        secret_key: Porkbun secret key (from PORKBUN_DOMAIN_SECRET_KEY env var)
        base_url: Porkbun API base URL
        timeout: Request timeout in seconds
        enable_http_transport: Enable HTTP transport for MCP
        http_host: HTTP server bind address
        http_port: HTTP server port
    """

    model_config = SettingsConfigDict(
        env_prefix="PORKBUN_DOMAIN_",
        env_file=(".env",),
        extra="ignore",
        case_sensitive=False,
    )

    # API credentials
    api_key: str = Field(
        default="",
        description="Porkbun API key",
    )
    secret_key: str = Field(
        default="",
        description="Porkbun secret key",
    )

    # API configuration
    base_url: str = Field(
        default="https://porkbun.com/api/json/v3",
        description="Porkbun API base URL",
    )
    timeout: float = Field(
        default=30.0,
        ge=1.0,
        le=120.0,
        description="Request timeout in seconds",
    )
    max_retries: int = Field(
        default=3,
        ge=0,
        le=5,
        description="Maximum retry attempts on failure",
    )

    # HTTP transport configuration
    enable_http_transport: bool = Field(
        default=False,
        description="Enable HTTP transport for MCP server",
    )
    http_host: str = Field(
        default="127.0.0.1",
        description="HTTP server bind address",
    )
    http_port: int = Field(
        default=3043,
        ge=1,
        le=65535,
        description="HTTP server port",
    )

    # Logging configuration (Oneiric style)
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )
    log_json: bool = Field(
        default=True,
        description="Output logs as JSON for log aggregation",
    )

    @field_validator("base_url", mode="after")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """Validate and normalize base URL."""
        if not v:
            return "https://porkbun.com/api/json/v3"
        return v.rstrip("/")

    def has_credentials(self) -> bool:
        """Check if API credentials are configured."""
        return bool(self.api_key and self.secret_key)

    def get_masked_api_key(self) -> str:
        """Get masked API key for safe logging."""
        if not self.api_key:
            return "***"
        if len(self.api_key) <= 4:
            return "***"
        return f"...{self.api_key[-4:]}"

    def auth_payload(self) -> dict[str, str]:
        """Get authentication payload for Porkbun API."""
        return {
            "apikey": self.api_key,
            "secretapikey": self.secret_key,
        }

    def http_client_config(self) -> dict[str, Any]:
        """Get HTTP client configuration."""
        return {
            "base_url": self.base_url,
            "timeout": httpx.Timeout(self.timeout),
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "porkbun-domain-mcp/0.1.1",
            },
        }


def setup_logging(settings: PorkbunDomainSettings | None = None) -> None:
    """Configure logging using Oneiric patterns."""
    if settings is None:
        settings = get_settings()

    if ONEIRIC_LOGGING_AVAILABLE:
        config = LoggingConfig(
            level=settings.log_level,
            emit_json=settings.log_json,
            service_name="porkbun-domain-mcp",
        )
        configure_logging(config)
    else:
        logging.basicConfig(
            level=getattr(logging, settings.log_level.upper(), logging.INFO),
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )


@lru_cache
def get_settings() -> PorkbunDomainSettings:
    """Get cached settings instance."""
    return PorkbunDomainSettings()


def get_logger_instance(name: str = "porkbun-domain-mcp") -> Any:
    """Get a structured logger instance."""
    if ONEIRIC_LOGGING_AVAILABLE:
        return get_logger(name)
    return logging.getLogger(name)


__all__ = [
    "PorkbunDomainSettings",
    "get_settings",
    "setup_logging",
    "get_logger_instance",
    "ONEIRIC_LOGGING_AVAILABLE",
]
