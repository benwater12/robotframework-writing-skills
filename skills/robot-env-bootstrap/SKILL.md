---
name: robot-env-bootstrap
description: Initialize an empty Robot Framework API test workspace using uv with Python 3.13. Use to create pyproject.toml, .venv, and a project-root .env with BASE_URL, ADMIN_USERNAME, and ADMIN_PASSWORD aligned to robot-api-test-suite.
---

# Robot Env Bootstrap

## Overview
Bootstrap a clean Robot Framework API testing environment with uv, Python 3.13, and a project-root .env aligned to robot-api-test-suite.

## Workflow
1. Start in an empty project root.
2. Create `pyproject.toml` using `assets/pyproject.toml` (or let the bootstrap script generate it).
3. Create `example.env` using `assets/example.env` (or let the bootstrap script generate it).
4. Run `scripts/bootstrap_env.py` from the project root to install uv (if missing), create `.venv`, and install dependencies.
5. Copy `example.env` to `.env` if it does not exist and update credentials.

## Defaults
- `BASE_URL` defaults to `http://localhost:8000`.
- Use `ADMIN_USERNAME` and `ADMIN_PASSWORD` for auth.

## Notes
- `.env` must live in the project root so `robot-api-test-suite` can load it.
- `.venv` is the Python environment location only.

## Resources
- `assets/pyproject.toml` - Template project config with dependencies.
- `assets/example.env` - Example env file with required keys.
- `scripts/bootstrap_env.py` - Cross-platform bootstrap script (macOS/Windows/Linux).
