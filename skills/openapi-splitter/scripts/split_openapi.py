import argparse
import json
from copy import deepcopy
from pathlib import Path


HTTP_METHODS = {
    "get",
    "put",
    "post",
    "delete",
    "options",
    "head",
    "patch",
    "trace",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split an OpenAPI JSON file by tags or routes."
    )
    parser.add_argument(
        "--input",
        default=None,
        help="Input OpenAPI JSON file path (default: auto-detect openapi.json or openAPI.json).",
    )
    parser.add_argument(
        "--output",
        default="openapi-specs",
        help="Output directory (default: openapi-specs).",
    )
    parser.add_argument(
        "--mode",
        choices=["tags", "routes"],
        required=True,
        help="Split mode: tags or routes.",
    )
    parser.add_argument(
        "--routes-grouping",
        choices=["path", "path-method"],
        default="path",
        help="Routes grouping (default: path).",
    )
    return parser.parse_args()


def resolve_input_path(raw_input: str | None) -> Path:
    if raw_input:
        return Path(raw_input)

    lower = Path("openapi.json")
    legacy = Path("openAPI.json")
    if lower.exists():
        return lower
    return legacy


def load_openapi(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def cleanup_generated_outputs(output_dir: Path) -> None:
    for pattern in ("tag-*.json", "path-*.json"):
        for file_path in output_dir.glob(pattern):
            if file_path.is_file():
                file_path.unlink()
    index_path = output_dir / "index.json"
    if index_path.is_file():
        index_path.unlink()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("/", "-")
    value = value.replace("{", "").replace("}", "")
    value = value.replace(" ", "-")
    value = value.replace("--", "-")
    value = "".join(ch for ch in value if ch.isalnum() or ch in "-_")
    return value or "unnamed"


def base_document(source: dict) -> dict:
    return {key: deepcopy(value) for key, value in source.items() if key != "paths"}


def filter_tag_objects(base: dict, tag_name: str) -> dict:
    result = deepcopy(base)
    tags = result.get("tags")
    if isinstance(tags, list):
        filtered = [
            tag for tag in tags if isinstance(tag, dict) and tag.get("name") == tag_name
        ]
        if filtered:
            result["tags"] = filtered
        else:
            result.pop("tags", None)
    return result


def collect_routes(openapi: dict) -> dict:
    return openapi.get("paths", {}) if isinstance(openapi.get("paths"), dict) else {}


def split_by_tags(openapi: dict) -> tuple[list[dict], list[dict]]:
    paths = collect_routes(openapi)
    tag_map: dict[str, dict] = {}
    for path, methods in paths.items():
        if not isinstance(methods, dict):
            continue
        for method, operation in methods.items():
            if method.lower() not in HTTP_METHODS:
                continue
            if not isinstance(operation, dict):
                continue
            tags = operation.get("tags")
            if not tags:
                continue
            for tag in tags:
                if not isinstance(tag, str):
                    continue
                tag_paths = tag_map.setdefault(tag, {})
                path_entry = tag_paths.setdefault(path, {})
                path_entry[method] = deepcopy(operation)

    outputs = []
    manifest = []
    base = base_document(openapi)
    for tag, tag_paths in sorted(tag_map.items()):
        doc = filter_tag_objects(base, tag)
        doc["paths"] = tag_paths
        outputs.append({"name": f"tag-{slugify(tag)}.json", "doc": doc})
        manifest.append({"file": f"tag-{slugify(tag)}.json", "tag": tag})
    return outputs, manifest


def split_by_routes(openapi: dict, grouping: str) -> tuple[list[dict], list[dict]]:
    paths = collect_routes(openapi)
    outputs = []
    manifest = []
    base = base_document(openapi)

    for path, methods in sorted(paths.items()):
        if not isinstance(methods, dict):
            continue
        if grouping == "path":
            doc = deepcopy(base)
            doc["paths"] = {path: deepcopy(methods)}
            filename = f"path-{slugify(path)}.json"
            outputs.append({"name": filename, "doc": doc})
            manifest.append({"file": filename, "path": path})
        else:
            for method, operation in sorted(methods.items()):
                if method.lower() not in HTTP_METHODS:
                    continue
                if not isinstance(operation, dict):
                    continue
                doc = deepcopy(base)
                doc["paths"] = {path: {method: deepcopy(operation)}}
                filename = f"path-{slugify(path)}-{method.lower()}.json"
                outputs.append({"name": filename, "doc": doc})
                manifest.append(
                    {"file": filename, "path": path, "method": method.lower()}
                )
    return outputs, manifest


def write_outputs(output_dir: Path, outputs: list[dict], manifest: list[dict]) -> None:
    for item in outputs:
        out_path = output_dir / item["name"]
        with out_path.open("w", encoding="utf-8") as handle:
            json.dump(item["doc"], handle, indent=2, ensure_ascii=False)
            handle.write("\n")

    manifest_path = output_dir / "index.json"
    with manifest_path.open("w", encoding="utf-8") as handle:
        json.dump({"items": manifest}, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def main() -> None:
    args = parse_args()
    input_path = resolve_input_path(args.input)
    output_dir = Path(args.output)

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    openapi = load_openapi(input_path)
    if not isinstance(openapi, dict) or "paths" not in openapi:
        raise SystemExit("Invalid OpenAPI JSON: missing top-level 'paths'.")

    ensure_output_dir(output_dir)
    cleanup_generated_outputs(output_dir)

    if args.mode == "tags":
        outputs, manifest = split_by_tags(openapi)
    else:
        outputs, manifest = split_by_routes(openapi, args.routes_grouping)

    if not outputs:
        raise SystemExit("No outputs generated. Check your OpenAPI file contents.")

    write_outputs(output_dir, outputs, manifest)
    print(f"Wrote {len(outputs)} files to {output_dir}")


if __name__ == "__main__":
    main()
