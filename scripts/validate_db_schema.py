#!/usr/bin/env python3
"""Static contract check for the PostgreSQL MVP migration."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "db" / "migrations" / "0001_raw_knowledge_store.sql"
REQUIRED_TABLES = {
    "sources", "source_documents", "source_versions", "assets",
    "processing_jobs", "document_versions", "document_chunks", "entities",
    "entity_names", "claims", "claim_evidence", "relations", "article_sources",
}


def main() -> int:
    sql = MIGRATION.read_text(encoding="utf-8")
    tables = set(re.findall(r"(?im)^CREATE TABLE\s+([a-z_]+)\s*\(", sql))
    errors = []
    if missing := sorted(REQUIRED_TABLES - tables):
        errors.append(f"missing tables: {', '.join(missing)}")
    for extension in ("pgcrypto", "vector"):
        if not re.search(rf"(?im)^CREATE EXTENSION IF NOT EXISTS {extension};$", sql):
            errors.append(f"missing extension: {extension}")
    assets = sql[sql.index("CREATE TABLE assets"):sql.index("CREATE TABLE processing_jobs")]
    if "sha256 char(64) NOT NULL UNIQUE" not in assets:
        errors.append("assets must be addressed by unique SHA-256")
    for column in ("rights_status rights_status", "publication_status publication_status"):
        if column not in assets:
            errors.append(f"assets missing independent column: {column.split()[0]}")
    for trigger in ("source_versions_are_immutable", "document_versions_are_immutable"):
        if f"CREATE TRIGGER {trigger}" not in sql:
            errors.append(f"missing immutability trigger: {trigger}")
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    print(f"Database schema contract valid: {len(tables)} tables")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
