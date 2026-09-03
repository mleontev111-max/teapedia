#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "build" / "public"
PUBLIC_FILES = (
    "index.html",
    "tea.html",
    "ware.html",
    "robots.txt",
    "sitemap.xml",
    "data/teas.json",
    "data/ware.json",
    "data/generated/articles-public.json",
)
PUBLIC_DIRS = ("css", "js", "encyclopedia")


def copy_path(relative: str, output: Path) -> None:
    source = ROOT / relative
    destination = output / relative
    if source.is_dir():
        shutil.copytree(source, destination)
    elif source.is_file():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    else:
        raise FileNotFoundError(f"required public path does not exist: {relative}")


def referenced_media_paths() -> list[str]:
    manifest_path = ROOT / "data" / "generated" / "articles-public.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    paths: list[str] = []
    for media in payload.get("media", []):
        relative = media.get("local_path")
        if not isinstance(relative, str):
            raise ValueError(f"verified public media {media.get('id')!r} has no local_path")
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != "media":
            raise ValueError(f"public media local_path must be below media/: {relative!r}")
        paths.append(relative)
    return sorted(set(paths))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the allowlisted GitHub Pages artifact")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or ROOT not in output.parents:
        raise ValueError("output must be a subdirectory of the repository")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for relative in (*PUBLIC_FILES, *PUBLIC_DIRS, *referenced_media_paths()):
        copy_path(relative, output)
    (output / ".nojekyll").touch()
    count = sum(1 for path in output.rglob("*") if path.is_file())
    print(f"Public site built at {output.relative_to(ROOT)}: {count} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
