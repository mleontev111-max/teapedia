#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ENTITIES_DIR = ROOT / "data" / "entities"
OUTPUT = ROOT / "data" / "generated" / "graph-index.json"


def main() -> int:
    entities: dict[str, dict[str, Any]] = {}
    incoming: dict[str, list[dict[str, str]]] = defaultdict(list)

    files = sorted(list(ENTITIES_DIR.glob("*/*.yml")) + list(ENTITIES_DIR.glob("*/*.yaml")))
    for path in files:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        entity_type = data.get("type")
        entity_id = data.get("id")
        if not entity_type or not entity_id:
            continue

        key = f"{entity_type}/{entity_id}"
        entities[key] = {
            "type": entity_type,
            "id": entity_id,
            "name_ru": data.get("name_ru"),
            "name_zh": data.get("name_zh"),
            "status": data.get("status"),
            "path": str(path.relative_to(ROOT)),
            "relations": data.get("relations") or [],
        }

    for source_key, entity in entities.items():
        source_type, source_id = source_key.split("/", 1)
        for edge in entity.get("relations", []):
            if not isinstance(edge, dict):
                continue
            target_type = edge.get("type")
            target_id = edge.get("id")
            relation = edge.get("relation")
            if not target_type or not target_id or not relation:
                continue
            target_key = f"{target_type}/{target_id}"
            incoming[target_key].append(
                {
                    "relation": relation,
                    "source_type": source_type,
                    "source_id": source_id,
                }
            )

    output = {
        "schema_version": "1.0.0",
        "entity_count": len(entities),
        "entities": entities,
        "incoming": {key: sorted(value, key=lambda x: (x["relation"], x["source_type"], x["source_id"])) for key, value in sorted(incoming.items())},
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)} with {len(entities)} entities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
