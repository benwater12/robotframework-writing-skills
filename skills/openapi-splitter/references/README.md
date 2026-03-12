# OpenAPI Splitter

Small CLI tool to split an OpenAPI JSON file into smaller parts for easier study.

## Requirements

- Python 3.9+

## Usage

Defaults auto-detect input in this order: `openapi.json`, then `openAPI.json`,
and output to `openapi-specs/`.

```bash
python split_openapi.py --mode tags
python split_openapi.py --mode routes
```

### Options

- `--input` Path to the OpenAPI JSON file (default: auto-detect `openapi.json` then `openAPI.json`).
- `--output` Output directory (default: `openapi-specs`).
- `--mode` Split mode: `tags` or `routes` (required).
- `--routes-grouping` When `--mode routes`, choose `path` (default) or `path-method`.

### Examples

```bash
python split_openapi.py --mode tags
python split_openapi.py --mode routes --routes-grouping path-method
python split_openapi.py --input myapi.json --output my_specs --mode tags
```

## Output

- On each execution, the tool replaces previously generated split artifacts in the output folder by removing `index.json`, `tag-*.json`, and `path-*.json` before writing new files.
- `openapi-specs/index.json` lists generated files and their tag/path metadata.
- `tag-*.json` contains only operations with that tag.
- `path-*.json` contains one file per route (or per method if `path-method`).

## Sample Input/Output

Sample input (`openapi.json`):

```json
{
  "openapi": "3.0.0",
  "info": {"title": "Pets", "version": "1.0.0"},
  "paths": {
    "/pets": {
      "get": {"tags": ["pets"], "summary": "List pets"},
      "post": {"tags": ["pets"], "summary": "Create pet"}
    },
    "/owners": {
      "get": {"tags": ["owners"], "summary": "List owners"}
    }
  }
}
```

Output (tags mode):

```text
openapi-specs/
  index.json
  tag-owners.json
  tag-pets.json
```
