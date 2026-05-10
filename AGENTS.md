# Repository Guidelines

## Project Structure & Module Organization

- `porkbun_domain_mcp/` contains the server package, API client logic, tool implementations, and schema helpers.
- `docs/` and root docs should hold operator-facing guidance; `tests/` should mirror the package structure for registration, renewal, and domain-management coverage.
- Generated artifacts in `dist/` should remain build output.

## Build, Test, and Development Commands

- `uv sync --group dev` installs development dependencies.
- Use the documented local server commands for stdio or HTTP smoke tests.
- `uv run pytest` runs the test suite.
- `uv run ruff check porkbun_domain_mcp tests` and `uv run ruff format porkbun_domain_mcp tests` cover linting and formatting.
- Run project quality checks through Crackerjack before landing changes.

## Coding Style & Naming Conventions

- Use explicit type hints, validated inputs, and small composable helpers around the Porkbun API.
- Keep modules snake_case and tool responses structured and predictable.

## Testing Guidelines

- Add tests for domain lookups, lifecycle operations, and API error handling.
- Prefer mocked API interactions over live-network tests.

## Commit & Pull Request Guidelines

- Use focused commits such as `feat(domains): add transfer lock status tool`.
- PRs should describe tool impact, commands run, and any new auth or config expectations.

## Security & Configuration Tips

- Never commit Porkbun credentials.
- Scrub sensitive domain and billing-related details from shared logs or examples.
