"""Porkbun Domain MCP - MCP server for Porkbun domain management.

This package provides an MCP (Model Context Protocol) server for managing
domains through the Porkbun API.

Modules:
    models: Pydantic models for API request/response validation
    config: Configuration with Oneiric logging support
    client: HTTP client for Porkbun API communication
    server: FastMCP server implementation
"""

from porkbun_domain_mcp.client import PorkbunDomainClient
from porkbun_domain_mcp.config import PorkbunDomainSettings, get_settings, setup_logging
from porkbun_domain_mcp.models import (
    AuthCode,
    Domain,
    DomainInfo,
    PricingInfo,
    PorkbunError,
    RenewalResult,
)

__version__ = "0.1.1"

__all__ = [
    "PorkbunDomainClient",
    "PorkbunDomainSettings",
    "get_settings",
    "setup_logging",
    "Domain",
    "DomainInfo",
    "AuthCode",
    "RenewalResult",
    "PricingInfo",
    "PorkbunError",
    "__version__",
]
