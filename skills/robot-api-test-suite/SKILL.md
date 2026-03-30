---
name: robot-api-test-suite
description: Create and update Robot Framework API test suites from OpenAPI routes using RequestsLibrary and FakerLibrary templates. Use when the user asks to generate or modify API scenarios, shared resources/keywords, route-level keyword files, or route-to-spec mappings under `openapi-specs/`.
---

# Robot Api Test Suite

## Overview
Create Robot Framework API suites with one scenario per route file, using shared resources plus route-scoped and utils keywords.

## Workflow
1. Identify scope from the request:
   - target routes (`path` + `method`) or tags
   - domain/resource name
   - create new files vs update existing files
2. Preflight runtime prerequisites:
   - Ensure `.venv` and Robot dependencies are available.
   - Resolve configuration only from `<project-root>/.env`.
   - Require `BASE_URL`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD` to be present and non-empty in the root `.env`.
   - If the root `.env` file is missing or incomplete, stop and instruct the user to fix `.env` before retrying.
   - If dependencies are missing, run:
     - `uv pip install robotframework robotframework-requests faker robotframework-faker python-dotenv`
   - If `uv` is not available, stop and warn the user to run `robot-env-bootstrap` first.
3. Resolve OpenAPI source:
   - Prefer `openapi-specs/` inputs first.
   - If only a full spec exists (for example project-root `openapi.json`), use `openapi-splitter` to produce route/tag specs and `openapi-specs/index.json`.
4. Resolve spec file per route in this order:
   - path/method entry from `openapi-specs/index.json`
   - tag entry from `openapi-specs/index.json`
   - full OpenAPI file fallback
5. Create or update files with templates:
   - scenario file: `tests/<domain>/<action>.robot`
   - resource file: `resources/<resource_name>_resources.robot`
   - route keywords: `keywords/<resource_name>/<action>_keywords.robot`
   - shared utils: `keywords/utils_keywords.robot`
6. Keep responsibilities separated:
   - scenario file: flow only
   - route keyword file: endpoint call + route assertions
   - utils keyword file: shared helpers/session/payload/assertions
   - resources file: variables, suite setup/teardown, shared imports/tags
7. Add/maintain `Documentation` in each scenario with the exact resolved spec path.
8. Modify only files related to requested routes/resources; do not refactor unrelated suites.

## Suite Structure
- Use `tests/<domain>/<action>.robot` with snake_case names.
- Use one scenario flow per file. Test case name mirrors the file name.
- Use shared files:
  - `resources/<resource_name>_resources.robot`
  - `keywords/<resource_name>/<action>_keywords.robot`
  - `keywords/utils_keywords.robot`
  - `variables/api_variables.robot` when suite variables become large

## Environment Variables
- Load test configuration from a project-root `.env` file.
- If using `robot-env-bootstrap`, use the `.env` it creates in the project root.
- Store values like `BASE_URL`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD` in `.env` and reference them from suite resources/variables.
- Do not read runtime configuration from nested `.env` files or alternate working directories.
- If the root `.env` file is missing or any required value is empty, stop and tell the user to fix `.env` before retrying.

## OpenAPI Specs
- Accept one of these spec inputs:
  - `openapi-specs/openapi.json`
  - `openapi-specs/path--<path>-<method>.json`
  - `openapi-specs/tag-<tag>.json`
- Use the `openapi-splitter` skill to produce tag/path specs and a `openapi-specs/index.json` manifest.
- Types 2 and 3 require `openapi-specs/index.json` to map route details to `file`.
- Path/method index uses `file`, `path`, `method` (lowercase).
- Tag index uses `file`, `tag`.
- Resolve index `file` values as `openapi-specs/<file>` unless a full path is provided.
- Add a `Documentation` line in each scenario that references the spec file used.

## Update Rules
- If target files already exist, preserve existing custom steps and only patch required sections.
- Keep file names and keyword names in snake_case.
- Keep imports relative and consistent with template structure.
- Do not rename existing files unless the user explicitly requests it.

## Shared vs Scenario Logic
- Put route-specific HTTP operations and assertions in `keywords/<resource_name>/<action>_keywords.robot`.
- Put non-route helpers (sessions, payload builders, common assertions) in `keywords/utils_keywords.robot`.
- Keep suite variables, tags, and setup/teardown in `resources/<resource_name>_resources.robot`.
- Scenario files import the resource-specific resources plus route keywords and utils keywords.
- Use scenario files only for flow steps and scenario-specific variables.

## Templates
- Use `assets/templates/scenario.robot` for each new route scenario.
- Use `assets/templates/api_resources.robot` to initialize shared resources per resource name.
- Use `assets/templates/api_keywords.robot` to initialize route keywords per resource/action.
- Use `assets/templates/utils_keywords.robot` to initialize shared utils keywords.

## Example Layout
- Route keywords: `keywords/users/create_user_keywords.robot`
- Utils keywords: `keywords/utils_keywords.robot`
- Scenario imports both route and utils keywords alongside resources.

Example imports (minimal):

```robot
*** Settings ***
Resource    ../../resources/users_resources.robot
Resource    ../../keywords/users/create_user_keywords.robot
Resource    ../../keywords/utils_keywords.robot
```

## References
- For RequestsLibrary and FakerLibrary usage patterns, see `references/robot_api_patterns.md`.
