# Porkbun Domain MCP Server

[![Code style: crackerjack](https://img.shields.io/badge/code%20style-crackerjack-000042)](https://github.com/lesleslie/crackerjack)
[![Runtime: oneiric](https://img.shields.io/badge/runtime-oneiric-6e5494)](https://github.com/lesleslie/oneiric)
[![Framework: FastMCP](https://img.shields.io/badge/framework-FastMCP-0ea5e9)](https://github.com/jlowin/fastmcp)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python: 3.13+](https://img.shields.io/badge/python-3.13%2B-green)](https://www.python.org/downloads/)

MCP server for Porkbun domain-management workflows.

**Version:** 0.2.0
**Status:** Internal Bodai integration component

## Quick Links

- [Overview](#overview)
- [Capabilities](#capabilities)
- [Quick Start](#quick-start)
- [MCP Server Configuration](#mcp-server-configuration)
- [Tool Reference](#tool-reference)
- [Configuration](#configuration)
- [Development](#development)

## Quality & CI

Crackerjack is the standard quality-control and CI/CD gate for Porkbun Domain MCP changes. Local verification should mirror the Crackerjack workflow used across the Bodai ecosystem.

______________________________________________________________________

## Overview

Porkbun Domain MCP exposes domain-registration workflows through a FastMCP server. It is focused on account domain inventory, domain metadata, transfer authorization, renewal, and pricing operations while keeping provider credentials and request validation in a narrow integration boundary.

This server focuses on registration and lifecycle workflows (inventory, metadata, transfer authorization, renewal, pricing). Record-level DNS changes are out of scope.

## Capabilities

Implemented tool surface:

- **Domain inventory**: list all domains in the configured Porkbun account
- **Domain details**: inspect status, TLD, registration date, expiration date, privacy, and auto-renew flags
- **Transfer authorization**: retrieve EPP authorization codes
- **Renewal workflow**: renew a domain for a selected number of years
- **Pricing lookup**: retrieve registration, renewal, and transfer pricing by TLD
- **Credential health metadata**: report whether API credentials are configured
- **HTTP health routes**: `/health` and `/healthz` for MCP client and process supervision checks

## Quick Start

### Prerequisites

- Python 3.13+
- UV package manager
- Porkbun API key and secret key

### Local Setup

```bash
git clone https://github.com/lesleslie/porkbun-domain-mcp.git
cd porkbun-domain-mcp
uv sync --group dev
```

### Run With Credentials

```bash
export PORKBUN_DOMAIN_API_KEY="your-api-key"
export PORKBUN_DOMAIN_SECRET_KEY="your-secret-key"
uv run porkbun-domain-mcp start
uv run porkbun-domain-mcp health
```

The default HTTP bind is `127.0.0.1:3043`.

## CLI Commands

The CLI is built with `mcp-common` and provides the standard lifecycle command surface used by Bodai MCP servers.

```bash
uv run porkbun-domain-mcp start      # Start the HTTP MCP server
uv run porkbun-domain-mcp stop       # Stop the managed server process (requires pid_file wiring)
uv run porkbun-domain-mcp restart    # Restart the managed server process (requires pid_file wiring)
uv run porkbun-domain-mcp status     # Show process status (requires pid_file wiring)
uv run porkbun-domain-mcp health     # Run the local health probe
```

> **Note (0.2.0):** `stop`, `restart`, and `status` rely on `mcp-common`'s `MCPServerCLIFactory` lifecycle, which requires `pid_file` and `log_file` to be configured on the lifecycle settings class. The current `porkbun_domain_mcp.cli.PorkbunDomainSettings` does not define either field, so these commands may report "not configured" at runtime. `start` and `health` work without the lifecycle wiring.

## MCP Server Configuration

### Claude / Codex Style Configuration

Add the server to an MCP client configuration:

```json
{
  "mcpServers": {
    "porkbun-domain": {
      "command": "uv",
      "args": ["run", "porkbun-domain-mcp", "start"],
      "cwd": "/Users/les/Projects/porkbun-domain-mcp",
      "env": {
        "PORKBUN_DOMAIN_API_KEY": "your-api-key",
        "PORKBUN_DOMAIN_SECRET_KEY": "your-secret-key"
      }
    }
  }
}
```

Use your secret manager for live credentials rather than committing them to client config.

### Health Checks

```bash
curl http://127.0.0.1:3043/health
curl http://127.0.0.1:3043/healthz
```

## Tool Reference

| Tool | Purpose | Required Inputs |
|------|---------|-----------------|
| `list_domains` | List domains in the Porkbun account | none |
| `get_domain_info` | Retrieve domain metadata | `domain` |
| `get_auth_code` | Retrieve transfer authorization code | `domain` |
| `renew_domain` | Renew a domain registration | `domain` |
| `get_pricing` | Retrieve TLD pricing | none |

Tool responses follow a consistent `ToolResponse` shape:

```json
{
  "success": true,
  "message": "Found 12 domains in your account",
  "data": {},
  "error": null,
  "next_steps": []
}
```

## Configuration

Committed defaults live in `settings/porkbun-domain.yaml`. Runtime overrides should come from environment variables or a local `.env` file that is not committed.

| Setting | Environment Variable | Default |
|---------|----------------------|---------|
| API key | `PORKBUN_DOMAIN_API_KEY` | empty |
| Secret key | `PORKBUN_DOMAIN_SECRET_KEY` | empty |
| Base URL | `PORKBUN_DOMAIN_BASE_URL` | `https://porkbun.com/api/json/v3` |
| Timeout | `PORKBUN_DOMAIN_TIMEOUT` | `30.0` |
| Max retries | `PORKBUN_DOMAIN_MAX_RETRIES` | `3` |
| HTTP host | `PORKBUN_DOMAIN_HTTP_HOST` | `127.0.0.1` |
| HTTP port | `PORKBUN_DOMAIN_HTTP_PORT` | `3043` |
| Log level | `PORKBUN_DOMAIN_LOG_LEVEL` | `INFO` |
| JSON logs | `PORKBUN_DOMAIN_LOG_JSON` | `true` |

> **Notes (0.2.0):**
>
> - The `porkbun_domain_mcp.config.PorkbunDomainSettings` model is configured with `env_prefix="PORKBUN_DOMAIN_"` and uses field names such as `log_json`, `log_level`, `http_host`, `timeout`, and `max_retries`. With pydantic-settings defaults, environment-variable names above match the model binding **only when the field has a single-word name** (e.g. `api_key` → `PORKBUN_DOMAIN_API_KEY`). Some env vars listed above may not bind without explicit aliases on the corresponding `Field(...)` declarations. Treat the table as the intent; if an override does not take effect, set the value in `settings/local.yaml` (gitignored) instead.
> - `PORKBUN_DOMAIN_HTTP_HOST` is loaded by `PorkbunDomainSettings` but is **not yet consumed** by the `start` command — `porkbun_domain_mcp.cli.start_server_handler` currently hardcodes `host="127.0.0.1"` when launching `uvicorn`. Override the bind address in `settings/local.yaml` (via `http_host`) and re-check the `start` command in a follow-up release.

## Project Structure

```text
porkbun_domain_mcp/
  cli.py                 # mcp-common lifecycle CLI
  client.py              # Porkbun domain API client boundary
  config.py              # Pydantic settings and logging
  models.py              # Typed domain and pricing models
  server.py              # FastMCP application factory
  tools/domain_tools.py  # Registered MCP tools
settings/
  porkbun-domain.yaml    # Committed defaults
tests/
```

## Development

```bash
uv sync --group dev
uv run pytest
uv run ruff check porkbun_domain_mcp tests
uv run ruff format porkbun_domain_mcp tests
```

Use targeted tests when isolating domain workflows:

```bash
uv run pytest tests -k domain -v
```

> **Note (0.2.0):** The `tests/` directory exists at the repo root but is currently empty — there are no test files yet, so the `uv run pytest` invocations above are placeholders for the incoming test suite. The 0.2.0 release dropped `--cov-fail-under` for exactly this reason. Run `uv run pytest --collect-only` to confirm the empty collection before treating a green test run as coverage evidence.

## Security Notes

- Do not commit Porkbun API keys, secret keys, billing-sensitive information, transfer authorization codes, or real account exports.
- Treat `get_auth_code` and `renew_domain` as privileged tools.
- Review generated transfer and renewal calls before exposing them to unattended agent workflows.
- Scrub real domain details from fixtures, screenshots, and troubleshooting logs.
