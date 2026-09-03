# PROJECT_STATUS.md — Teapedia

Updated: 2026-09-03

Teapedia currently contains two deployed/curated layers: a static HTML/JavaScript presentation that reads `data/teas.json` and `data/ware.json`, and Knowledge Graph v1 entities under `data/entities/`. The graph is the structured model for new knowledge, but it is not yet automatically rendered into the legacy static catalog.

The accepted target architecture adds an upstream operational layer: sources -> immutable RAW documents/assets -> versioned processing and semantic chunks -> claims/evidence/conflicts -> entities/relations -> curated YAML/Git Knowledge Graph -> editorial publishing -> public Pages. PostgreSQL is the planned operational knowledge store; `docs/architecture/RAW_KNOWLEDGE_STORE.md` and `db/migrations/0001_raw_knowledge_store.sql` are the official contract and first migration proposal.

There is no deployed application database, Docker stack, `.env`, or runtime secret requirement yet. The migration proposal does not change the current static runtime or Pages deployment.

## Clean start

Use Python 3.12, create a local virtual environment, install `requirements.txt`, run the graph validator, database schema contract check and reverse-index builder, then serve the repository with `python -m http.server 8000` and open `http://127.0.0.1:8000/`.

Do not open the site only through `file://`, because the JavaScript fetches JSON files.

## Current verified baseline

Pre-Project-Ready main: `94c2bf63a0518a28c7707f255ea2f1d09a6f1dbb`.

Wave 0 is complete: stable IDs, Tea/TeaBatch/Product separation, directed relations, source/fact-check policy, validator, reverse-index builder and GitHub Actions validation exist. GitHub Pages also built that baseline successfully.

## Safety boundaries

Do not invent tea/batch/producer facts, edit generated reverse links as canonical data, or assume a graph edit automatically changes the static site. Old custom-domain instructions are not proof of current DNS state.

## Current limitations

- graph-to-static presentation generation is not implemented;
- legacy JSON and graph entities can drift;
- branch protection is not enabled on the audited baseline;
- Wave 0 is foundation rather than full content coverage.
- the editorial admin is Git-first and intentionally has no direct server-side save/authentication on GitHub Pages;
- the editorial admin, draft/review JSON and ingestion snapshots are excluded from an allowlisted Pages artifact and verified absent in CI;
- the first imported article remains a draft and its candidate image remains blocked pending separate license verification.
- PostgreSQL and object storage are architectural proposals, not deployed services;
- no collectors write into the operational schema yet;
- pgvector is included in the first migration for forward compatibility, while embedding generation is intentionally deferred.

## ONE NEXT ACTION

Apply and validate `0001_raw_knowledge_store.sql` in an isolated PostgreSQL environment, including backup/rollback and object-store configuration, before implementing collectors.
