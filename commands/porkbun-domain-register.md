---
description: Renew (re-register) a domain in the configured Porkbun account for 1-10 years.
argument-hint: <domain> [--years N]
allowed-tools: mcp__porkbun-domain__renew_domain, mcp__porkbun-domain__get_domain_info, mcp__porkbun-domain__get_pricing
---

# /porkbun-domain-register

Renew a domain registration in the configured Porkbun account via the porkbun-domain MCP server.

## Usage

`/porkbun-domain-register <domain> [--years N]`

Arguments:

- `<domain>`: the domain to renew (e.g., `example.com`). Must already be in the configured account.
- `--years N`: optional renewal length, integer 1-10. Defaults to 1.

This command does NOT register a brand-new domain. It extends the registration of an existing domain in the account. For new registrations, use the Porkbun web UI directly.

## What it does

1. Calls `mcp__porkbun-domain__get_domain_info` to confirm the domain is in the account and to capture the current expiration date.
2. Calls `mcp__porkbun-domain__get_pricing` for the TLD so the renewal cost is reported before the user confirms.
3. After explicit confirmation, calls `mcp__porkbun-domain__renew_domain` with the domain and the supplied year count.
4. Reports the new expiration date and the renewal cost.

## Example

`/porkbun-domain-register example.com --years 2`
