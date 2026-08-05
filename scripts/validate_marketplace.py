#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".github" / "plugin" / "marketplace.json"
KEBAB = re.compile(r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
REPOSITORY = re.compile(r"^ma-nakaya/[A-Za-z0-9_.-]+$")
SHA = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    raise ValueError(message)


def validate_url(value: object, label: str) -> None:
    if not isinstance(value, str):
        fail(f"{label} must be a string")
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.netloc != "github.com":
        fail(f"{label} must be an https://github.com URL")


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("marketplace manifest must be an object")

    allowed_top = {"name", "owner", "metadata", "plugins"}
    if set(data) - allowed_top:
        fail(f"unexpected top-level fields: {sorted(set(data) - allowed_top)}")
    if not isinstance(data.get("name"), str) or not KEBAB.fullmatch(data["name"]):
        fail("marketplace name must be kebab-case")
    owner = data.get("owner")
    if not isinstance(owner, dict) or owner.get("name") != "ma-nakaya":
        fail("marketplace owner must be ma-nakaya")

    plugins = data.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail("plugins must be a non-empty array")

    names: set[str] = set()
    sources: set[tuple[str, str]] = set()
    for index, plugin in enumerate(plugins):
        label = f"plugins[{index}]"
        if not isinstance(plugin, dict):
            fail(f"{label} must be an object")
        name = plugin.get("name")
        if not isinstance(name, str) or len(name) > 64 or not KEBAB.fullmatch(name):
            fail(f"{label}.name is invalid")
        if name in names:
            fail(f"duplicate plugin name: {name}")
        names.add(name)

        description = plugin.get("description")
        if not isinstance(description, str) or not 1 <= len(description) <= 1024:
            fail(f"{label}.description must contain 1-1024 characters")
        version = plugin.get("version")
        if not isinstance(version, str) or not version:
            fail(f"{label}.version is required")

        source = plugin.get("source")
        if not isinstance(source, dict) or source.get("source") != "github":
            fail(f"{label}.source must be a GitHub source object")
        repo = source.get("repo")
        sha = source.get("sha")
        if not isinstance(repo, str) or not REPOSITORY.fullmatch(repo):
            fail(f"{label}.source.repo must be a ma-nakaya repository")
        if not isinstance(sha, str) or not SHA.fullmatch(sha):
            fail(f"{label}.source.sha must be a full lowercase commit SHA")
        source_key = (repo.lower(), sha)
        if source_key in sources:
            fail(f"duplicate source: {repo}@{sha}")
        sources.add(source_key)

        validate_url(plugin.get("homepage"), f"{label}.homepage")
        validate_url(plugin.get("repository"), f"{label}.repository")
        author = plugin.get("author")
        if not isinstance(author, dict) or author.get("name") != "ma-nakaya":
            fail(f"{label}.author.name must be ma-nakaya")

    print(f"Validated {len(plugins)} marketplace plugins.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
