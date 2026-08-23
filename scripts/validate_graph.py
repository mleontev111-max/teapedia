#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ENTITIES_DIR = ROOT / "data" / "entities"

ALLOWED_TYPES = {
    "province",
    "region",
    "cultivar",
    "tea_type",
    "tea",
    "tea_batch",
    "product",
    "processing",
    "brewing",
    "teaware",
    "terminology",
    "history",
    "producer",
}

ALLOWED_STATUSES = {"draft", "review", "published", "deprecated"}

ALLOWED_RELATIONS = {
    "PART_OF",
    "CONTAINS",
    "HAS_TYPE",
    "HAS_SUBTYPE",
    "MADE_FROM",
    "GROWN_IN",
    "ORIGINATES_IN",
    "USES_PROCESS",
    "BREW_WITH",
    "BREW_GUIDE",
    "RELATED_TERM",
    "RELATED_TEA",
    "PRODUCED_BY",
    "REPRESENTS",
    "BATCH_OF",
    "SOLD_AS",
    "ASSOCIATED_WITH",
}

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SCHEMA_RE = re.compile(r"^\d+\.\d+\.\d+$")

BASE_REQUIRED = {"type", "id", "schema_version", "status", "name_ru"}
TYPE_REQUIRED = {
    "province": {"name_zh", "pinyin"},
    "region": {"name_zh", "pinyin", "region_kind"},
    "cultivar": {"name_zh", "pinyin"},
    "tea_type": {"name_zh", "pinyin"},
    "tea": {"name_zh", "pinyin"},
    "tea_batch": {"year"},
    "product": {"brand", "sale_unit"},
    "brewing": set(),
    "terminology": set(),
    "producer": set(),
    "processing": set(),
    "teaware": set(),
    "history": set(),
}


def load_entities() -> tuple[dict[tuple[str, str], tuple[Path, dict[str, Any]]], list[str]]:
    entities: dict[tuple[str, str], tuple[Path, dict[str, Any]]] = {}
    errors: list[str] = []

    if not ENTITIES_DIR.exists():
        return entities, [f"Entities directory does not exist: {ENTITIES_DIR}"]

    files = sorted(list(ENTITIES_DIR.glob("*/*.yml")) + list(ENTITIES_DIR.glob("*/*.yaml")))
    if not files:
        return entities, ["No entity YAML files found"]

    for path in files:
        rel = path.relative_to(ROOT)
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{rel}: YAML parse error: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{rel}: root must be a mapping/object")
            continue

        entity_type = data.get("type")
        entity_id = data.get("id")
        if not isinstance(entity_type, str) or not isinstance(entity_id, str):
            errors.append(f"{rel}: type and id must be strings")
            continue

        key = (entity_type, entity_id)
        if key in entities:
            other = entities[key][0].relative_to(ROOT)
            errors.append(f"{rel}: duplicate entity {entity_type}/{entity_id}; already defined in {other}")
            continue
        entities[key] = (path, data)

    return entities, errors


def validate_entity(path: Path, data: dict[str, Any], all_keys: set[tuple[str, str]]) -> list[str]:
    rel = path.relative_to(ROOT)
    errors: list[str] = []

    entity_type = data.get("type")
    entity_id = data.get("id")

    if entity_type not in ALLOWED_TYPES:
        errors.append(f"{rel}: unsupported type {entity_type!r}")
        return errors

    expected_folder = entity_type
    if path.parent.name != expected_folder:
        errors.append(f"{rel}: folder '{path.parent.name}' must match type '{entity_type}'")

    if isinstance(entity_id, str):
        if not ID_RE.fullmatch(entity_id):
            errors.append(f"{rel}: id '{entity_id}' must be lowercase Latin kebab-case")
        if path.stem != entity_id:
            errors.append(f"{rel}: filename '{path.stem}' must equal id '{entity_id}'")

    required = BASE_REQUIRED | TYPE_REQUIRED.get(entity_type, set())
    for field in sorted(required):
        if field not in data:
            errors.append(f"{rel}: missing required field '{field}'")
        elif data[field] is None or data[field] == "":
            errors.append(f"{rel}: required field '{field}' is empty")

    schema_version = data.get("schema_version")
    if not isinstance(schema_version, str) or not SCHEMA_RE.fullmatch(schema_version):
        errors.append(f"{rel}: schema_version must use semantic version form x.y.z")

    status = data.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"{rel}: status {status!r} is not allowed")

    relations = data.get("relations", [])
    if relations is None:
        relations = []
    if not isinstance(relations, list):
        errors.append(f"{rel}: relations must be a list")
        return errors

    seen_edges: set[tuple[str, str, str]] = set()
    for idx, edge in enumerate(relations, start=1):
        prefix = f"{rel}: relation #{idx}"
        if not isinstance(edge, dict):
            errors.append(f"{prefix} must be an object")
            continue

        relation = edge.get("relation")
        target_type = edge.get("type")
        target_id = edge.get("id")

        if relation not in ALLOWED_RELATIONS:
            errors.append(f"{prefix}: relation {relation!r} is not allowed")
        if target_type not in ALLOWED_TYPES:
            errors.append(f"{prefix}: target type {target_type!r} is not allowed")
        if not isinstance(target_id, str) or not ID_RE.fullmatch(target_id):
            errors.append(f"{prefix}: target id {target_id!r} is not valid kebab-case")
            continue

        if target_type in ALLOWED_TYPES:
            target_key = (target_type, target_id)
            if target_key not in all_keys:
                errors.append(f"{prefix}: unresolved target {target_type}/{target_id}")

        edge_key = (str(relation), str(target_type), target_id)
        if edge_key in seen_edges:
            errors.append(f"{prefix}: duplicate edge {relation} -> {target_type}/{target_id}")
        seen_edges.add(edge_key)

    return errors


def main() -> int:
    entities, errors = load_entities()
    all_keys = set(entities)

    for _, (path, data) in sorted(entities.items()):
        errors.extend(validate_entity(path, data, all_keys))

    if errors:
        print(f"Teapedia graph validation FAILED: {len(errors)} problem(s)\n")
        for error in errors:
            print(f"- {error}")
        return 1

    edge_count = 0
    type_counts: dict[str, int] = {}
    for (entity_type, _), (_, data) in entities.items():
        type_counts[entity_type] = type_counts.get(entity_type, 0) + 1
        relations = data.get("relations") or []
        if isinstance(relations, list):
            edge_count += len(relations)

    print("Teapedia graph validation OK")
    print(f"Entities: {len(entities)}")
    print(f"Relations: {edge_count}")
    for entity_type in sorted(type_counts):
        print(f"  {entity_type}: {type_counts[entity_type]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
