## Context

`read_dependencies()` currently treats import failures, file parsing failures, and invalid dependency shapes as equivalent by falling back to `DEFAULT_DEPS`. This preserves execution flow but conceals broken project configuration.

## Goals / Non-Goals

**Goals:**

- Keep a sensible fallback when dependency metadata is genuinely absent
- Surface malformed `pyproject.toml` content as an explicit failure
- Validate that `project.dependencies` is a list of strings before use

**Non-Goals:**

- Changing the default dependency list
- Reworking the overall bootstrap flow
- Adding new CLI options or configuration files

## Decisions

### Decision 1: Distinguish missing configuration from invalid configuration

The script will keep using `DEFAULT_DEPS` when dependency metadata is absent, but it will stop silently recovering from malformed TOML or invalid dependency structures. Those cases represent user configuration errors and should be reported clearly.

### Decision 2: Keep compatibility fallback limited to parser availability

If `tomllib` is unavailable in the interpreter, the script can still fall back to `DEFAULT_DEPS`. That is an environment limitation, not a project configuration problem.
