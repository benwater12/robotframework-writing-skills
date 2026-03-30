## Why

Environment-variable handling is currently described as project-root `.env` based, but some flows appear to read configuration inconsistently. This creates avoidable setup drift and makes failures harder to diagnose when `.env` is missing or required variables are unset.

## What Changes

- Define a single configuration contract: environment variables must be read from the repository root `.env`.
- Standardize environment-loading behavior across the affected scripts and skills so they resolve the same `.env` path.
- Require the procedure to stop when the root `.env` file is missing and instruct the user to fix `.env` before retrying.
- Require the procedure to stop when expected variables are missing or empty and instruct the user to fix `.env` before retrying.

## Capabilities

### New Capabilities
- `root-env-loading`: Ensure tooling reads configuration from the repository root `.env` and stops with a fix-first message when the file or required variables are missing.

### Modified Capabilities
- None.

## Impact

Affected areas include Robot Framework bootstrap and execution workflows, any shared configuration-loading helpers, and skill documentation that describes how runtime configuration is sourced.
