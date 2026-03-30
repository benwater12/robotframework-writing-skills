---
name: robot-beginner-test-guide
description: "Guide a beginner with no Robot Framework experience through a complete API test flow using existing skills. Use when a user needs step-by-step help to verify or bootstrap environment setup, prepare and split OpenAPI specs, define test requirements, generate suites, and run Robot tests."
---

# Robot Beginner Test Guide

## Overview

Guide a first-time user from setup verification to a successful Robot test run. Use existing skills as building blocks and gate each phase before moving forward.

## Workflow

1. Ask whether the user already bootstrapped the Robot environment.
2. If not bootstrapped, run `robot-env-bootstrap`, then remind the user to prepare `openapi.json` for reference.
3. If bootstrapped, verify required environment artifacts.
4. If verification passes, split OpenAPI and replace old split outputs.
5. Collect test requirements from the user.
6. Build/update tests with `robot-api-test-suite`.
7. Run tests with `robot-test-runner`.

## Step 1: Ask bootstrap status

- Ask: "Have you already bootstrapped this Robot project environment?"
- If answer is no or unknown, run `robot-env-bootstrap`.
- After bootstrap, explicitly remind the user to provide `openapi.json` in project root or `openapi-specs/openapi.json`.

## Step 2: Verify environment when user says bootstrapped

Check all of these before continuing:
- `.venv` exists in project root
- `uv` is available on PATH
- `.env` exists in project root
- `.env` contains non-empty `BASE_URL`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD`
- `openapi.json` exists (project root or `openapi-specs/openapi.json`)

If any check fails:
- Stop and report exactly what is missing.
- For `.env` issues, tell the user to fix the root `.env` before retrying.
- Instruct user to run `robot-env-bootstrap` only when the environment has not been bootstrapped yet.
- Instruct the user to prepare `openapi.json` for the spec issue.

## Step 3: Split OpenAPI and replace old outputs

- Use `openapi-splitter` only after environment/spec checks pass.
- Replace old split outputs by recreating the output folder before splitting:
  - remove old `openapi-specs/` split artifacts
  - generate fresh `openapi-specs/index.json` and split files
- Prefer `openapi.json` as source; if both name variants exist, use lowercase `openapi.json`.

## Step 4: Gather requirements

Ask only for details needed to implement tests:
- target routes (path + method)
- expected status codes
- auth/header behavior
- required payload fields and key assertions
- any tag/filter to run specific tests

## Step 5: Generate tests with skills

- Use `robot-api-test-suite` to create or update scenario/resources/keywords files.
- Keep changes scoped to requested routes/resources.
- Keep reusable logic in shared keywords and route logic in route keyword files.

## Step 6: Run Robot tests

- Use `robot-test-runner` to execute the target suite/file.
- Ensure run artifacts are produced:
  - `output.xml`
  - `log.html`
  - `report.html`
- Ensure run record is saved in output dir (`run-command.txt`), including command and `.env` snapshot.

## Completion Checklist

- Environment ready (`.venv`, `uv`, `.env`)
- OpenAPI ready and split outputs regenerated
- Test requirements captured
- Robot test files created/updated
- Test run completed and artifacts reported
