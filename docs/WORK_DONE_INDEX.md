# WORK DONE INDEX

Resume-System-Version: 1.3

Historical lookup only. Current continuation comes from `PROJECT_STATE.json` / `ACTIVE_WORK.json`, not from this list.

## Verified on main

- **Knowledge Graph Wave 0** — stable IDs, Tea/TeaBatch/Product separation, directed relations, source/fact-check policy, validator and reverse-index builder are already implemented.
- **Safe editorial workflow** — draft/review/published states, licensed-media handling, Teapedia ingestion and an allowlisted GitHub Pages artifact are merged. Private editorial/admin inputs are intentionally absent from the public build.
- **Bai Hao Yin Zhen Russian article** — a draft already exists. Its candidate image remains blocked pending independent license verification. Do not recreate or publish it as a shortcut.

## Durable but unmerged

- **PR #5 — RAW knowledge store / editorial architecture** (`architecture/raw-knowledge-store`): PostgreSQL/pgvector-oriented RAW/provenance/versioning architecture and migration proposal already exist. During Resume Gate rollout it was exactly ahead 2 / behind 0 relative to `main`. Do not reimplement it from scratch; select it through `ACTIVE_WORK.json` and verify the exact current PR head first.

For exact historical commits and current observed WIP heads, use `MILESTONE_INDEX.json` and GitHub itself. Dynamic branch/PR heads must always be re-read before work.
