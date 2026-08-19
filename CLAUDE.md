# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

For a shorter, tool-neutral bootstrap document, start with `AGENTS.md`.

## Project Overview

MCP server for Porkbun domain management.

## Development Guidelines

### Code Quality

This project uses Crackerjack for quality assurance. Follow these patterns:

**Type Hints:**

```python
from typing import Any

def process_domain(domain: str) -> dict[str, Any]:
    """Process a domain name.

    Args:
        domain: The domain name to process

    Returns:
        Dictionary with processing results
    """
    return {"domain": domain}
```

**Error Handling:**

```python
# DO - Specific exception handling
try:
    result = api_call()
except APIError as e:
    logger.error(f"API error: {e}")
    raise

# DON'T - Bare except
try:
    result = api_call()
except Exception:
    pass  # Never suppress errors
```

**Docstrings:**

- Use Google-style docstrings
- Include Args, Returns, Raises sections
- Document non-obvious behavior

### Testing

- Target: 80%+ code coverage
- Use pytest markers: `@pytest.mark.unit`, `@pytest.mark.integration`
- Write tests in `tests/` directory mirroring source structure

### Running Quality Checks

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Run tests with coverage
pytest

# Security scan
bandit -r porkbun_domain_mcp

# Check for unused dependencies
creosote
```

<!-- CRACKERJACK_START -->

## Tool Profile System

This server adopts the mcp-common 0.18.0 tool profile dispatcher. The
default profile is `FULL` (all 5 tools + `health_check` + `discover_tools`).
Set `PORKBUN_DOMAIN_TOOL_PROFILE=minimal` to expose only `health_check` +
`discover_tools` (useful for control-plane / health-probe deployments
where the Porkbun-bound tools would fail without credentials). Bogus
env values raise `InvalidProfileError` at startup.

The production path is **async** — `create_app()` awaits the W0 helper
directly. The sync `apply_tool_profile()` wrapper from mcp-common raises
`RuntimeError` in event loops, so the async path is the only correct
entry point for any async caller. Tests cover this with an AST guard
(`test_server_awaits_apply_porkbun_domain_tool_profile`) that would fail
if `await` is removed.

See `docs/architecture/tool-profile-rationale.md` for the full design.

## Crackerjack Integration

This project is integrated with Crackerjack for automated quality assurance:

- **MCP Server:** Crackerjack server running on localhost:8676
- **Skill System:** Access to 12 specialized AI agents
- **Quality Tracking:** Automated metrics and CI/CD integration

### Available Skills

The project can use Crackerjack's AI agent skills via MCP:

- `RefactoringAgent` - Code refactoring and cleanup
- `PerformanceAgent` - Performance optimization
- `SecurityAgent` - Security vulnerability analysis
- `TestingAgent` - Test generation and improvement
- `DocumentationAgent` - Documentation generation
- `CodeReviewAgent` - Automated code reviews
- `ComplexityAgent` - Complexity reduction
- `ErrorHandlingAgent` - Error handling improvements
- `APIDesignAgent` - API design review
- `TypeHintsAgent` - Type annotation improvements
- `NamingAgent` - Naming convention suggestions
- `TestingStrategyAgent` - Testing strategy consultation

### MCP Integration

This project can be accessed via Crackerjack's MCP server for real-time quality monitoring and intelligent fix suggestions.

<!-- CRACKERJACK_END -->
