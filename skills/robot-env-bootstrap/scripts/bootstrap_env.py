#!/usr/bin/env python3
"""
Bootstrap a Robot Framework API test environment.

Actions:
- Ensure uv is installed (auto-install with pip --user if missing).
- Create pyproject.toml and example.env if missing.
- Create .venv with Python 3.13.
- Install dependencies into .venv using uv.
- Copy example.env to .env if .env is missing.
- Validate the project-root .env contract before finishing.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_PYPROJECT = """[build-system]
requires = [\"setuptools>=68\"]
build-backend = \"setuptools.build_meta\"

[project]
name = \"robot-api-tests\"
version = \"0.1.0\"
description = \"Robot Framework API test suite\"
requires-python = \">=3.13\"
dependencies = [
  \"robotframework>=6.1\",
  \"robotframework-requests>=0.9\",
  \"robotframework-faker>=5.0\",
  \"python-dotenv>=1.0\",
]
"""

DEFAULT_EXAMPLE_ENV = """BASE_URL=http://localhost:8000
ADMIN_USERNAME=admin@example.com
ADMIN_PASSWORD=change-me
"""

DEFAULT_DEPS = [
    "robotframework>=6.1",
    "robotframework-requests>=0.9",
    "robotframework-faker>=5.0",
    "python-dotenv>=1.0",
]

REQUIRED_ENV_VARS = (
    "BASE_URL",
    "ADMIN_USERNAME",
    "ADMIN_PASSWORD",
)


def run(cmd: list[str], title: str) -> None:
    print(f"{title}: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def ensure_file(path: Path, content: str) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")
    print(f"Created {path}")


def ensure_uv() -> None:
    if shutil.which("uv"):
        return

    response = input("uv not found. Install uv now? [y/N]: ").strip().lower()
    if response != "y":
        print("uv installation skipped. Please install uv, then re-run.")
        print("  https://astral.sh/uv")
        raise SystemExit(1)

    print("Attempting install via official installer.")
    if sys.platform == "win32":
        result = subprocess.run(
            [
                "powershell",
                "-ExecutionPolicy",
                "ByPass",
                "-Command",
                "irm https://astral.sh/uv/install.ps1 | iex",
            ]
        )
    else:
        result = subprocess.run(
            ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"]
        )

    if result.returncode == 0 and shutil.which("uv"):
        return

    print("uv installer did not complete. Attempting pip --user install.")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "--user", "uv"])
    if result.returncode != 0:
        print("uv install command failed. Continuing to fallback message.")

    if shutil.which("uv"):
        return

    print("uv still not found after installation.")
    print("Install uv with one of these commands, then re-run:")
    print("  python -m pip install --user uv")
    print("  brew install uv  # macOS")
    raise SystemExit(1)


def read_dependencies(pyproject_path: Path) -> list[str]:
    try:
        import tomllib  # Python 3.11+
    except ModuleNotFoundError:
        return DEFAULT_DEPS

    try:
        data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise SystemExit(f"Invalid pyproject.toml: {exc}") from exc

    project = data.get("project", {})
    if not isinstance(project, dict):
        raise SystemExit("Invalid pyproject.toml: 'project' must be a table.")

    deps = project.get("dependencies")
    if not deps:
        return DEFAULT_DEPS

    if not isinstance(deps, list) or not all(
        isinstance(dep, str) for dep in deps
    ):
        raise SystemExit(
            "Invalid pyproject.toml: 'project.dependencies' must be a list of strings."
        )

    return list(deps)


def parse_env_file(env_path: Path) -> dict[str, str]:
    env_values: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key:
            env_values[key] = value
    return env_values


def build_missing_env_file_message(env_path: Path) -> str:
    return (
        f"Missing required root .env file: {env_path}\n"
        "Fix .env before retrying."
    )


def build_missing_env_vars_message(env_path: Path, missing_vars: list[str]) -> str:
    missing_list = ", ".join(missing_vars)
    return (
        f"Missing required values in root .env ({env_path}): {missing_list}\n"
        "Fix .env before retrying."
    )


def validate_root_env(env_path: Path) -> dict[str, str]:
    if not env_path.exists():
        raise SystemExit(build_missing_env_file_message(env_path))

    env_values = parse_env_file(env_path)
    missing_vars = [
        key for key in REQUIRED_ENV_VARS if not env_values.get(key, "").strip()
    ]
    if missing_vars:
        raise SystemExit(build_missing_env_vars_message(env_path, missing_vars))
    return env_values


def main() -> None:
    project_root = Path.cwd()
    pyproject_path = project_root / "pyproject.toml"
    example_env_path = project_root / "example.env"
    env_path = project_root / ".env"
    venv_path = project_root / ".venv"
    if sys.platform == "win32":
        venv_python = venv_path / "Scripts" / "python.exe"
    else:
        venv_python = venv_path / "bin" / "python"

    ensure_uv()

    ensure_file(pyproject_path, DEFAULT_PYPROJECT)
    ensure_file(example_env_path, DEFAULT_EXAMPLE_ENV)

    if not venv_path.exists():
        run(["uv", "venv", "--python", "3.13"], "Creating .venv")
    else:
        print(".venv already exists. Skipping creation.")

    deps = read_dependencies(pyproject_path)
    if deps:
        run(
            ["uv", "pip", "install", "--python", str(venv_python)] + deps,
            "Installing dependencies",
        )

    if not env_path.exists():
        shutil.copyfile(example_env_path, env_path)
        print("Created .env from example.env")
    else:
        print(".env already exists. Skipping creation.")

    validate_root_env(env_path)
    print(f"Validated root .env: {env_path}")
    print("Bootstrap complete.")


if __name__ == "__main__":
    main()
