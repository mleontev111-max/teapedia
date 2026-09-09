# AGENTS.md — Teapedia working protocol

This repository must be understandable without previous chat history.

## 0. Mandatory Resume Gate — before any answer/plan/action

Before any project answer, plan, task choice, content proposal, code review, code change, ingestion action, graph/database architecture action, or publication suggestion:

1. read `START_HERE_FOR_AI.md` first;
2. establish exact branch/HEAD and refresh `origin`;
3. read `PROJECT_STATE.json`, `ACTIVE_WORK.json`, `CHECKPOINT_INDEX.json`;
4. run `python3 tools/project_resume.py`;
5. if continuity or Project Ready Guard reports BLOCKER, stop and repair/report continuity before feature/editorial work.

Do not use chat history or a dated checkpoint as the current source when the machine current-state layer disagrees.

## 1. Session start

```bash
git fetch origin
git status --short --branch
git log -1 --oneline
python3 tools/project_resume.py
```

Then read the selected current source/checkpoint. For merged editorial work this is normally `PROJECT_STATUS.md`; for a registered WIP branch/PR use `ACTIVE_WORK.json` and its branch-owned `STATE.md`.

GitHub exact refs are canonical. A historical checkpoint is evidence, not a live branch ref.

## 2. Architecture boundary

Teapedia currently has two content/data layers on main:

- browser-facing legacy JSON: `data/teas.json`, `data/ware.json`;
- structured Knowledge Graph: `data/entities/**/*.yml`.

Do not assume one automatically updates the other. There is no graph-to-site generation pipeline yet.

Architecture PR #5 contains separate durable RAW/PostgreSQL-pgvector proposal work. Do not recreate it from scratch; select it via `ACTIVE_WORK.json` and verify exact current PR head first.

## 3. Graph editing rules

- Follow `SCHEMA.md` and `scripts/validate_graph.py`.
- Entity IDs are stable lowercase `kebab-case`.
- Prefer unknown/unverified to invented facts.
- Relations must target existing entities.
- Never hand-edit generated reverse/incoming links as canonical data; rebuild the index.
- Changing an existing entity ID requires checking all relations first.

## 4. Editorial/publication rules

- Draft/review content is not public merely because it exists in Git.
- Never move content to `published` without the required editorial/fact checks.
- Never approve/publish an image while source/license/provenance is unresolved.
- The Bai Hao Yin Zhen Russian draft already exists; do not recreate it as a shortcut.
- The editorial admin and ingestion snapshots are private/editorial inputs and must remain excluded from the public Pages artifact.

## 5. Static-site editing rules

After static UI/data changes, build and verify the public artifact, then test that artifact through a local HTTP server, not only `file://`:

```bash
python scripts/build_articles.py
python scripts/build_public_site.py
python scripts/verify_public_artifact.py build/public
python -m http.server 8000 --directory build/public
```

Then inspect the main catalog and any changed page in a browser.

## 6. Verification gate

Before a meaningful commit:

```bash
python scripts/validate_graph.py
python scripts/build_graph_index.py
python -m json.tool data/teas.json >/dev/null
python -m json.tool data/ware.json >/dev/null
```

Also run any new verifier required by the selected workstream, such as the DB schema contract check in architecture PR #5.

Project Ready/Resume Guard and ordinary GitHub validation CI must be green on the exact relevant PR/main SHA before considering a milestone verified. Do not weaken schema/privacy checks just to make CI pass.

## 7. Secrets / infrastructure

Current main application architecture has no runtime database, Docker stack, `.env`, or application secrets.

Do not add private supplier credentials, personal data, API tokens, or unpublished commercial information to public repository content.

GitHub Pages is the deployment mechanism. It must deploy only `build/public`, created by the explicit allowlist in `scripts/build_public_site.py`. Never deploy the repository root. A historical custom-domain instruction is not proof of current DNS/domain state; verify before changes.

## 8. PR protocol

Before merge:

1. re-read current `main` SHA;
2. re-read exact PR HEAD;
3. check divergence;
4. synchronize safely when needed without losing branch work;
5. refresh branch-owned `STATE.md` after all scoped changes;
6. require exact-head Project Ready/Resume Guard + ordinary CI PASS;
7. only then discuss merge.

## 9. Session end

Meaningful work is not considered saved until checks are run, diff is understood, changes are committed/pushed, CI is checked on the exact SHA, machine/current-state pointers are updated when continuation changes, and one exact next action or blocker is recorded.

For unmerged work, current branch-owned `STATE.md` is mandatory and must remain fresh relative to the workstream `scope_paths`. Do not leave the only record of progress in chat or a local branch.
