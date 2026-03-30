## ADDED Requirements

### Requirement: Validate bootstrap dependency configuration

The bootstrap script MUST validate dependency configuration loaded from `pyproject.toml` before using it for installation.

#### Scenario: Use declared dependencies when configuration is valid

- **WHEN** `pyproject.toml` contains a valid `project.dependencies` list
- **THEN** the bootstrap script uses that list for dependency installation

#### Scenario: Fall back when dependencies are absent

- **WHEN** `pyproject.toml` does not define `project.dependencies`
- **THEN** the bootstrap script falls back to the built-in default dependency list

#### Scenario: Reject malformed TOML content

- **WHEN** `pyproject.toml` cannot be parsed as valid TOML
- **THEN** the bootstrap script exits with a clear error instead of silently using defaults

#### Scenario: Reject invalid dependency structures

- **WHEN** `project.dependencies` is present but is not a list of strings
- **THEN** the bootstrap script exits with a clear error instead of silently using defaults
