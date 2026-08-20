---
description: Get Porkbun pricing for a single TLD (or all TLDs) — registration, renewal, and transfer costs.
argument-hint: "[<tld>] (e.g., com, net, org)"
allowed-tools: mcp__porkbun-domain__get_pricing
---

# /porkbun-domain-pricing

Look up Porkbun TLD pricing for registration, renewal, and transfer via the porkbun-domain MCP server.

## Usage

`/porkbun-domain-pricing <tld>`

Arguments:

- `<tld>`: optional. The TLD to look up (e.g., `com`, `net`, `org`). If omitted, returns pricing for all TLDs that Porkbun publishes.

## What it does

1. Calls `mcp__porkbun-domain__get_pricing` with the supplied `tld` (or `None` for the full catalog).
2. Reports a table of TLDs and their registration, renewal, and transfer costs.
3. Highlights the typical 1-year registration cost so the user can quickly compare.

## Example

`/porkbun-domain-pricing com`
