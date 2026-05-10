# Porkbun Domain MCP Server

[![Code style: crackerjack](https://img.shields.io/badge/code%20style-crackerjack-000042)](https://github.com/lesleslie/crackerjack)
[![Runtime: oneiric](https://img.shields.io/badge/runtime-oneiric-6e5494)](https://github.com/lesleslie/oneiric)
[![Framework: FastMCP](https://img.shields.io/badge/framework-FastMCP-0ea5e9)](https://github.com/jlowin/fastmcp)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python: 3.13+](https://img.shields.io/badge/python-3.13%2B-green)](https://www.python.org/downloads/)

MCP server for Porkbun domain-management workflows.

## Overview

This repository exposes domain-focused Porkbun operations through FastMCP, including lookup, renewal-oriented lifecycle actions, and domain metadata workflows. It is separate from the DNS server so domain operations and DNS record operations can evolve independently.

## Installation

```bash
uv sync --group dev
```

## Usage

### Stdio Mode

```bash
uv run porkbun-domain-mcp
```

### HTTP Mode

```bash
uv run porkbun-domain-mcp serve --http --port 3043
```

## Development

```bash
uv run pytest
uv run ruff check porkbun_domain_mcp tests
uv run ruff format porkbun_domain_mcp tests
```

## Project Structure

- `porkbun_domain_mcp/`: server package, provider client, tools, and schemas
- `tests/`: domain workflow and provider error handling coverage
- `docs/`: operational notes and examples

## Security Notes

- Never commit Porkbun credentials or billing-sensitive information.
- Scrub real domain details from fixtures, screenshots, and troubleshooting logs.
