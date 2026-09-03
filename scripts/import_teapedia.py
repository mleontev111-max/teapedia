#!/usr/bin/env python3
"""Create a non-publishing Teapedia import snapshot and draft scaffold."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("title must contain Latin letters or digits")
    return slug


def fetch_page(title: str) -> dict:
    query = urllib.parse.urlencode({"action": "query", "prop": "extracts|info|revisions", "inprop": "url", "rvprop": "ids|timestamp", "explaintext": 1, "redirects": 1, "titles": title, "format": "json", "formatversion": 2})
    request = urllib.request.Request(f"https://teapedia.org/eng/api.php?{query}", headers={"User-Agent": "THE-CHAI-Teapedia-importer/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["query"]["pages"][0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--accessed", default=dt.date.today().isoformat())
    args = parser.parse_args()
    page = fetch_page(args.title)
    if page.get("missing"):
        raise SystemExit(f"Teapedia page not found: {args.title}")
    slug = slugify(page["title"])
    revision = (page.get("revisions") or [{}])[0]
    revision_id = revision.get("revid")
    canonical = page.get("canonicalurl") or f"https://teapedia.org/en/{urllib.parse.quote(page['title'].replace(' ', '_'))}"
    revision_url = f"https://teapedia.org/eng/index.php?title={urllib.parse.quote(page['title'].replace(' ', '_'))}&oldid={revision_id}"
    destination = ROOT / "ingestion" / "teapedia.org" / "imports" / slug
    destination.mkdir(parents=True, exist_ok=True)
    snapshot = {"provider": "teapedia.org", "title": page["title"], "canonical_url": canonical, "revision_url": revision_url, "revision_id": revision_id, "page_last_edited": revision.get("timestamp"), "accessed": args.accessed, "text_license": "CC BY-SA 3.0", "text_license_url": "https://creativecommons.org/licenses/by-sa/3.0/", "image_policy": "not-imported-until-separately-verified", "import_status": "draft", "raw_extract": page.get("extract", "")}
    (destination / "source.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    draft_path = ROOT / "content" / "articles" / f"{slug}.json"
    if not draft_path.exists():
        draft = {"schema_version": "1.0.0", "id": slug, "status": "draft", "title_ru": page["title"], "subtitle_ru": "", "summary_ru": "Требуется перевод и редактура.", "sections": [{"heading_ru": "Черновик", "paragraphs_ru": ["Перевод ещё не подготовлен."]}], "entity_refs": [], "media_ids": [], "source": {"provider": "teapedia.org", "title": page["title"], "canonical_url": canonical, "revision_url": revision_url, "accessed": args.accessed, "license": "CC BY-SA 3.0", "license_url": "https://creativecommons.org/licenses/by-sa/3.0/", "adaptation_notice_ru": "Перевод и адаптация материала Teapedia."}, "review": {"editorial_approved": False, "license_approved": False, "notes_ru": ["Проверить перевод, факты и лицензии изображений."]}, "updated_at": args.accessed}
        draft_path.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created safe draft import: {destination.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
