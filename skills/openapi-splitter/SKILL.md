---
name: openapi-splitter
description: Split OpenAPI JSON into readable chunks by tags or routes; use when segmenting large OpenAPI specs or generating per-tag/per-route specs for tooling and test generation.
---

# OpenAPI Splitter

## Overview
Split a single OpenAPI JSON file into smaller specs by tag or by route, and emit an `index.json` manifest that maps outputs to tags and paths.

## Workflow
1. Identify the source OpenAPI file and an output directory (default: `openapi-specs/`).
   - Default source auto-detection order: `openapi.json` then `openAPI.json`.
2. Run the splitter in `tags` or `routes` mode.
   - Before writing new outputs, remove prior generated split artifacts in output directory: `index.json`, `tag-*.json`, and `path-*.json`.
3. Use the generated `index.json` plus `tag-*.json` or `path-*.json` outputs for downstream tooling.

## CLI Usage
- `python scripts/split_openapi.py --mode tags`
- `python scripts/split_openapi.py --mode routes`

## Outputs
- `index.json` with `items` containing file/tag/path metadata.
- `tag-*.json` per tag when using `--mode tags`.
- `path-*.json` per route when using `--mode routes`.

## References
- See `references/README.md` for full CLI options and examples.
