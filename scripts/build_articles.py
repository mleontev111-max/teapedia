#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "content" / "articles"
MEDIA_DIR = ROOT / "content" / "media"
ENTITIES_DIR = ROOT / "data" / "entities"
GENERATED_DIR = ROOT / "data" / "generated"
STATUSES = {"draft", "review", "published"}
MEDIA_STATUSES = {"pending", "verified", "rejected"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def read_objects(directory: Path) -> tuple[list[dict[str, Any]], list[str]]:
    objects: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in sorted(directory.glob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{path.relative_to(ROOT)}: root must be an object")
            continue
        value["_path"] = str(path.relative_to(ROOT))
        objects.append(value)
    return objects, errors


def required(obj: dict[str, Any], fields: set[str], label: str, errors: list[str]) -> None:
    for field in sorted(fields):
        if field not in obj or obj.get(field) in (None, ""):
            errors.append(f"{label}: missing or empty '{field}'")


def validate() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    articles, errors = read_objects(ARTICLES_DIR)
    media, media_errors = read_objects(MEDIA_DIR)
    errors.extend(media_errors)
    article_ids: set[str] = set()
    media_by_id: dict[str, dict[str, Any]] = {}
    entity_keys = {(p.parent.name, p.stem) for p in ENTITIES_DIR.glob("*/*.yml")}

    for item in media:
        label = item.get("_path", "media")
        required(item, {"schema_version", "id", "verification_status", "source_page_url", "article_ids", "entity_refs"}, label, errors)
        media_id = item.get("id")
        if not isinstance(media_id, str) or not ID_RE.fullmatch(media_id):
            errors.append(f"{label}: invalid id")
        elif media_id in media_by_id:
            errors.append(f"{label}: duplicate media id '{media_id}'")
        else:
            media_by_id[media_id] = item
        if item.get("verification_status") not in MEDIA_STATUSES:
            errors.append(f"{label}: invalid verification_status")
        if item.get("verification_status") == "verified":
            required(item, {"author", "license", "license_url", "original_file_url", "local_path", "alt_ru"}, label, errors)
            local_path = item.get("local_path")
            if isinstance(local_path, str) and not (ROOT / local_path).is_file():
                errors.append(f"{label}: local_path does not exist: {local_path}")

    for article in articles:
        label = article.get("_path", "article")
        required(article, {"schema_version", "id", "status", "title_ru", "summary_ru", "sections", "entity_refs", "media_ids", "source", "review"}, label, errors)
        article_id = article.get("id")
        if not isinstance(article_id, str) or not ID_RE.fullmatch(article_id):
            errors.append(f"{label}: invalid id")
        elif article_id in article_ids:
            errors.append(f"{label}: duplicate article id '{article_id}'")
        else:
            article_ids.add(article_id)
        if article.get("status") not in STATUSES:
            errors.append(f"{label}: invalid status")
        for ref in article.get("entity_refs", []):
            if not isinstance(ref, dict) or (ref.get("type"), ref.get("id")) not in entity_keys:
                errors.append(f"{label}: unresolved entity_ref {ref!r}")
        for media_id in article.get("media_ids", []):
            linked = media_by_id.get(media_id)
            if linked is None:
                errors.append(f"{label}: unknown media id '{media_id}'")
            elif article.get("status") == "published" and linked.get("verification_status") != "verified":
                errors.append(f"{label}: published article references unverified media '{media_id}'")
        if article.get("status") == "published":
            review = article.get("review", {})
            if not review.get("editorial_approved") or not review.get("license_approved"):
                errors.append(f"{label}: published article requires editorial and license approval")
            source = article.get("source", {})
            required(source, {"title", "canonical_url", "revision_url", "license", "license_url", "adaptation_notice_ru"}, f"{label}.source", errors)

    for item in media:
        label = item.get("_path", "media")
        for article_id in item.get("article_ids", []):
            if article_id not in article_ids:
                errors.append(f"{label}: unknown article id '{article_id}'")
        for ref in item.get("entity_refs", []):
            if not isinstance(ref, dict) or (ref.get("type"), ref.get("id")) not in entity_keys:
                errors.append(f"{label}: unresolved entity_ref {ref!r}")
    return articles, media, errors


def clean(obj: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in obj.items() if key != "_path"}


def main() -> int:
    articles, media, errors = validate()
    if errors:
        print(f"Article validation FAILED: {len(errors)} problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    admin = {"schema_version": "1.0.0", "articles": [clean(x) for x in articles], "media": [clean(x) for x in media]}
    public_articles = [clean(x) for x in articles if x.get("status") == "published"]
    verified_ids = {x["id"] for x in media if x.get("verification_status") == "verified"}
    public_media = [clean(x) for x in media if x.get("id") in verified_ids and any(x["id"] in a.get("media_ids", []) for a in public_articles)]
    public = {"schema_version": "1.0.0", "articles": public_articles, "media": public_media}
    for name, payload in (("articles-admin.json", admin), ("articles-public.json", public)):
        (GENERATED_DIR / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Articles OK: {len(articles)} total, {len(public_articles)} published; media: {len(media)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
