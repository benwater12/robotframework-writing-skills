## Why

The bootstrap script currently falls back to default dependencies for any exception while reading `pyproject.toml`. That keeps execution moving, but it also hides malformed TOML and invalid dependency structures that should be surfaced to the user.

## What Changes

- Narrow fallback behavior to expected compatibility cases
- Surface malformed `pyproject.toml` content as a clear user-facing error
- Validate that `project.dependencies` has the expected list shape before using it

## Capabilities

### New Capabilities

- `bootstrap-dependency-validation`: Validate and load bootstrap dependencies from `pyproject.toml` with explicit parsing and shape checks.

### Modified Capabilities

## Impact

- `skills/robot-env-bootstrap/scripts/bootstrap_env.py`: tighten dependency parsing and error handling
