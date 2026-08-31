# AGENTS.md — Teapedia working protocol

This repository must be understandable without previous chat history.

## Session start

Before changing anything:

```bash
git fetch origin
git status --short --branch
git log -1 --oneline
```

Read in order:

1. `README.md`;
2. `PROJECT_STATUS.md`;
3. this `AGENTS.md`;
4. `SCHEMA.md` for graph work;
5. `CHECKPOINT.md`, `ROADMAP.md`, `KNOWLEDGE_GRAPH_PLAN.md` only when historical/product context is needed.

GitHub `origin/main` is canonical code. A dated checkpoint is historical evidence, not a live branch ref.

## Architecture boundary

Teapedia currently has two data models:

- browser-facing legacy JSON: `data/teas.json`, `data/ware.json`;
- structured Knowledge Graph: `data/entities/**/*.yml`.

Do not assume one automatically updates the other. There is no graph-to-site generation pipeline yet.

## Graph editing rules

- Follow `SCHEMA.md` and `scripts/validate_graph.py`.
- Entity IDs are stable lowercase `kebab-case`.
- Prefer unknown/unverified to invented facts.
- Relations must target existing entities.
- Never hand-edit generated reverse/incoming links as canonical data; rebuild the index.
- Changing an existing entity ID requires checking all relations first.

## Static-site editing rules

The current UI loads legacy JSON through browser `fetch()`.

After static UI/data changes, verify through a local HTTP server, not only `file://`:

```bash
python -m http.server 8000
```

Then inspect the main catalog and any changed page in a browser.

## Verification gate

Before a meaningful commit:

```bash
python scripts/validate_graph.py
python scripts/build_graph_index.py
python -m json.tool data/teas.json >/dev/null
python -m json.tool data/ware.json >/dev/null
```

GitHub CI must be green on the exact PR/main SHA before considering a milestone verified.

Do not weaken schema checks or remove relations just to make CI pass without understanding the data problem.

## Secrets / infrastructure

Current application architecture has no database, no Docker stack, no `.env`, and no application secrets.

Do not add private supplier credentials, personal data, API tokens, or unpublished commercial information to public repository content.

GitHub Pages is the deployment mechanism. A historical instruction mentioning a custom domain is not enough to prove current DNS/domain configuration; verify it before changes.

## Session end

Meaningful work is not considered saved until:

1. checks are run;
2. `git status`/diff is understood;
3. changes are committed and pushed;
4. CI is checked on the exact SHA;
5. `PROJECT_STATUS.md` is updated if current state or ONE NEXT ACTION changed;
6. a dated checkpoint is added for a major milestone.

Do not leave the only record of progress in a chat or a local unpushed branch.
