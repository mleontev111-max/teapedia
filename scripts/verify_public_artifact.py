#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

FORBIDDEN_PARTS = {"admin", "content", "ingestion", "scripts", "tools", ".github", "docs"}
FORBIDDEN_NAMES = {"articles-admin.json", "source.json"}
ALLOWED_TOP_LEVEL = {
    ".nojekyll",
    "css",
    "data",
    "encyclopedia",
    "index.html",
    "js",
    "media",
    "robots.txt",
    "sitemap.xml",
    "tea.html",
    "ware.html",
}
ALLOWED_DATA_FILES = {
    Path("data/teas.json"),
    Path("data/ware.json"),
    Path("data/generated/articles-public.json"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Reject private/editorial files in a Pages artifact")
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    root = args.artifact.resolve()
    errors: list[str] = []
    if not root.is_dir():
        errors.append(f"artifact directory does not exist: {root}")
    else:
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root)
            if path.is_symlink():
                errors.append(f"symbolic links are not allowed: {relative}")
            if relative.parts[0] not in ALLOWED_TOP_LEVEL:
                errors.append(f"unexpected top-level path: {relative}")
            if FORBIDDEN_PARTS.intersection(relative.parts) or path.name in FORBIDDEN_NAMES:
                errors.append(f"private/editorial path is present: {relative}")
            if path.is_file() and relative.parts[0] == "data" and relative not in ALLOWED_DATA_FILES:
                errors.append(f"non-public data file is present: {relative}")
        manifest_path = root / "data" / "generated" / "articles-public.json"
        if not manifest_path.is_file():
            errors.append("public article manifest is missing")
        else:
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            for article in payload.get("articles", []):
                if article.get("status") != "published":
                    errors.append(f"non-published article in public manifest: {article.get('id')!r}")
            for media in payload.get("media", []):
                if media.get("verification_status") != "verified":
                    errors.append(f"unverified media in public manifest: {media.get('id')!r}")
            declared_media = {Path(item["local_path"]) for item in payload.get("media", []) if isinstance(item.get("local_path"), str)}
            actual_media = {path.relative_to(root) for path in (root / "media").rglob("*") if path.is_file()} if (root / "media").is_dir() else set()
            if actual_media != declared_media:
                errors.append(f"public media files do not match manifest: declared={sorted(map(str, declared_media))}, actual={sorted(map(str, actual_media))}")
    if errors:
        print(f"Public artifact FAILED: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    files = sum(1 for path in root.rglob("*") if path.is_file())
    print(f"Public artifact OK: {files} files; no private/editorial paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
