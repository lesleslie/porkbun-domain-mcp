# porkbun-domain-mcp

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
