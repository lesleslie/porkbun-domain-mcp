# Python Coding Standards

## Code Style

- Follow PEP 8 with 88 character line length
- Use type hints for all function parameters and returns
- Write docstrings for all public functions, classes, and modules
- Use f-strings for string formatting

## Type Hints

```python
from typing import Any

def process(item: dict[str, Any]) -> str:
    """Process an item and return a string."""
    return str(item)
```

## Error Handling

**DO:**
- Catch specific exceptions
- Log errors with context
- Clean up resources in finally blocks

**DON'T:**
- Use bare `except:` clauses
- Suppress exceptions with `pass`
- Use `# TODO` comments in production code

## Testing

- Write tests before implementation (TDD)
- Aim for 80%+ code coverage
- Use descriptive test names
- One assertion per test when possible

## Documentation

- Use Google-style docstrings
- Include examples in docstrings
- Keep README up to date
- Document public APIs
