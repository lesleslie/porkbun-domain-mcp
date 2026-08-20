---
description: List all domains in the configured Porkbun account along with status, expiration, and renewal flags.
argument-hint: (no arguments)
allowed-tools: mcp__porkbun-domain__list_domains, mcp__porkbun-domain__get_domain_info, mcp__porkbun-domain__get_pricing
---

# /porkbun-domain-list

List every domain in the configured Porkbun account via the porkbun-domain MCP server.

## Usage

`/porkbun-domain-list`

No arguments. The configured account credentials (PORKBUN_DOMAIN_API_KEY,
PORKBUN_DOMAIN_SECRET_KEY) determine which domains are returned.

## What it does

1. Calls `mcp__porkbun-domain__list_domains` to retrieve the full domain inventory.
2. For each domain that is near expiration (within 30 days) or has auto-renew disabled, calls `mcp__porkbun-domain__get_domain_info` to surface the precise expiration date.
3. If the user asks about renewal costs, calls `mcp__porkbun-domain__get_pricing` for the relevant TLDs.
4. Reports a compact table: domain, TLD, status, expiration date, and auto-renew flag.

## Example

`/porkbun-domain-list`
