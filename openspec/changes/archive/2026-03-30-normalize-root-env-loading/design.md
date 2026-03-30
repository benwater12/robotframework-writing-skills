## Context

This repository already describes a consistent runtime contract: Robot Framework bootstrap and test execution should use a `.env` file in the project root. In practice, that contract is distributed across multiple skills and scripts, which makes it easy for individual flows to drift in how they resolve configuration, when they stop, and which variables they treat as required.

The affected paths are cross-cutting but lightweight: bootstrap creates the root `.env`, test-running instructions consume the same values, and any generated or maintained helper code should follow the same lookup rule. The change needs a single design so implementation does not fix one flow while leaving others inconsistent.

## Goals / Non-Goals

**Goals:**
- Define one canonical `.env` location: `<project-root>/.env`.
- Ensure all environment-variable readers resolve that same path instead of relying on the current working directory of an individual script or ad hoc assumptions.
- Standardize validation for required variables such as `BASE_URL`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD`.
- Stop the procedure with a clear fix-first message when the root `.env` file is missing or when required variables are missing or empty.

**Non-Goals:**
- Introducing support for multiple `.env` files, layered environment resolution, or directory-specific overrides.
- Replacing existing bootstrap defaults such as `example.env`.
- Introducing fallback configuration sources when the root `.env` contract is not satisfied.

## Decisions

1. Resolve `.env` from project root, not caller-relative locations.
   Rationale: the repository skills already describe project-root `.env` behavior, and bootstrap creates `.env` in the current project root. Aligning all consumers to that single location removes ambiguity and makes generated instructions consistent.
   Alternative considered: allowing each script to load `.env` from its own working directory. Rejected because it preserves drift and makes behavior depend on how the tool is invoked.

2. Define a shared required-variable set for Robot API workflows.
   Rationale: `BASE_URL`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD` appear repeatedly in bootstrap and test-runner guidance, so they should be validated as one contract instead of per-flow guesswork.
   Alternative considered: letting each flow decide its own required keys. Rejected because it creates partial validation and inconsistent warnings.

3. Prefer a shared helper or shared logic pattern for env loading and validation.
   Rationale: this is a small repo, but the problem is cross-cutting. Centralizing root path resolution and missing-variable detection reduces repeated bugs and keeps warning text uniform even if the implementation remains minimal.
   Alternative considered: patching each flow independently. Rejected because it is the most likely way to reintroduce inconsistency later.

4. Stop on missing `.env` and missing values with actionable messages.
   Rationale: the user intent is to prevent partially configured runs. The failure message should identify the expected path and list missing keys, then instruct the user to fix `.env` before retrying.
   Alternative considered: warning-only behavior. Rejected because it still allows the workflow to proceed into indirect failures.

## Risks / Trade-offs

- Hard-stop behavior is less forgiving for partially configured local experiments -> Keep the stop message explicit and actionable so users can repair `.env` quickly.
- Introducing a shared helper adds a small maintenance surface -> Limit the helper to path resolution and validation only, without building a broader configuration framework.
- Existing users may rely on environment variables already exported in the shell -> Continue to treat root `.env` as the canonical source for this workflow and document any precedence rule clearly during implementation.

## Migration Plan

1. Identify every skill or script that reads or documents runtime env variables for Robot API workflows.
2. Update implementation to resolve `<project-root>/.env` consistently and validate the shared required keys.
3. Normalize user-facing stop messages for missing file and missing variables.
4. Update related skill documentation so the implementation and instructions describe the same behavior.
5. Verify bootstrap and test-runner flows still work when `.env` exists, and stop with the expected fix-first message when it does not.

## Open Questions

- Should shell-exported environment variables override values from the root `.env`, or should `.env` always win for these workflows?
