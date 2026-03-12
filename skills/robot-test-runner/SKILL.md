---
name: robot-test-runner
description: Run Robot Framework test suites with a project `.venv`, deterministic output directory naming, and command logging. Use when the user asks to run Robot tests, rerun a failing suite/file, execute a specific tag, or collect `output.xml`, `log.html`, and `report.html` artifacts for API test validation.
---

# Robot Test Runner

## Overview

Run Robot Framework tests with the interpreter in `.venv`, save artifacts to a deterministic output directory, and persist the exact command in `run-command.txt`.

## Workflow

1. Resolve test target from the user request:
   - Folder run: `<target-dir>`
   - Single file run: `<target-file>.robot`
2. Ensure project-root `.env` exists and is usable:
   - Require `.env` at project root.
   - If `.env` is missing, ask for `BASE_URL`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD`, then create `.env` in project root with those values.
   - If `.env` exists but is missing required keys, ask for missing values and update `.env`.
   - Use `.env` values as the primary source for Robot `--variable` arguments.
3. Resolve Python path from `.venv`:
   - Windows: `.venv\Scripts\python`
   - macOS/Linux: `.venv/bin/python`
4. Ensure runtime dependencies are available:
   - If `.venv` or required packages are missing, try:
     - `uv pip install robotframework robotframework-requests faker robotframework-faker python-dotenv`
   - If `uv` is not available in the environment, stop and warn the user to run the `robot-env-bootstrap` skill first.
5. Resolve output directory:
   - Use user-provided output dir when present.
   - Otherwise create `data_YYYY-MM-DD_HH-mm_<summary>`.
6. Build `<summary>` from target:
   - Normalize separators for summary generation only.
   - Replace non-alphanumeric characters with `-`.
   - Append `-file` for `.robot` targets and `-dir` for folder targets.
7. Build the Robot command:
   - Base: `<venv-python> -m robot --outputdir "<outputdir>" <target>`
   - Append variables as needed:
     - `--variable BASE_URL:<value>`
     - `--variable ADMIN_USERNAME:<value>`
     - `--variable ADMIN_PASSWORD:<value>`
   - Include optional filters (`--include`, `--exclude`, `--test`) only when requested.
8. Execute command from project root.
9. Write `<outputdir>/run-command.txt` with a reproducible run record:
   - Include the exact executed command.
   - Include the full content of project-root `.env` used for the run.
10. Report artifact paths from `<outputdir>`:
   - `output.xml`
   - `log.html`
   - `report.html`

## Cross-Platform Notes

- Accept both `/` and `\` in input paths.
- Do not rewrite the user target path except for summary derivation.
- Quote paths that contain spaces.
- Use the `.venv` interpreter directly instead of global `python` or `robot`.
- Keep `.env` in project root so both generation and run flows use the same runtime configuration.

## Examples

- Folder target `tests/api/robot`:
  - Output dir: `data_YYYY-MM-DD_HH-mm_robot-dir`
  - Windows:
    - `.venv\Scripts\python -m robot --outputdir "data_YYYY-MM-DD_HH-mm_robot-dir" --variable BASE_URL:http://example/api --variable ADMIN_USERNAME:admin --variable ADMIN_PASSWORD:password tests/api/robot`
  - macOS/Linux:
    - `.venv/bin/python -m robot --outputdir "data_YYYY-MM-DD_HH-mm_robot-dir" --variable BASE_URL:http://example/api --variable ADMIN_USERNAME:admin --variable ADMIN_PASSWORD:password tests/api/robot`

- File target `tests/api/robot/login_test.robot`:
  - Output dir: `data_YYYY-MM-DD_HH-mm_login-test-file`
  - Command:
    - `<venv-python> -m robot --outputdir "data_YYYY-MM-DD_HH-mm_login-test-file" tests/api/robot/login_test.robot`
