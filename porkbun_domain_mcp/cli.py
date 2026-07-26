"""Unified CLI for Porkbun Domain MCP server using mcp-common.

Provides standard lifecycle commands (start, stop, restart, status, health).
"""

from __future__ import annotations

import os
import warnings

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
warnings.filterwarnings("ignore", message=".*PyTorch.*TensorFlow.*Flax.*")

import uvicorn  # noqa: E402
from mcp_common import MCPServerCLIFactory  # noqa: E402
from mcp_common.cli.health import RuntimeHealthSnapshot  # noqa: E402
from oneiric.core.config import OneiricMCPConfig  # noqa: E402

from porkbun_domain_mcp import __version__  # noqa: E402


class PorkbunDomainSettings(OneiricMCPConfig):
    """Porkbun Domain MCP server settings extending OneiricMCPConfig."""

    server_name: str = "porkbun-domain-mcp"
    http_port: int = 3043
    startup_timeout: int = 10
    shutdown_timeout: int = 10
    force_kill_timeout: int = 5


def start_server_handler() -> None:
    """Start handler that launches the Porkbun Domain MCP server in HTTP mode."""
    settings = PorkbunDomainSettings()
    print(f"Starting Porkbun Domain MCP server on port {settings.http_port}...")
    uvicorn.run(
        "porkbun_domain_mcp.server:http_app",
        host="127.0.0.1",
        port=settings.http_port,
        log_level="info",
    )


def health_probe_handler() -> RuntimeHealthSnapshot:
    """Health probe handler for Porkbun Domain MCP server."""
    from porkbun_domain_mcp.config import get_settings

    settings = get_settings()
    return RuntimeHealthSnapshot(
        orchestrator_pid=os.getpid(),
        watchers_running=False,
        remote_enabled=False,
        lifecycle_state={
            "server_name": "porkbun-domain-mcp",
            "status": "healthy",
            "version": __version__,
        },
        activity_state={
            "credentials_configured": settings.has_credentials(),
            "api_url": settings.base_url,
        },
    )


factory = MCPServerCLIFactory(
    server_name="porkbun-domain-mcp",
    settings=None,  # Auto-load via MCPServerSettings.load(server_name)
    start_handler=start_server_handler,
    health_probe_handler=health_probe_handler,
)

app = factory.create_app()


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
