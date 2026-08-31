# Teapedia — Project Ready v1 checkpoint

Date: 2026-08-31

Status: IN PROGRESS until Project Ready changes reach `main` and the expanded CI passes there.

## Audited baseline

- baseline `main`: `94c2bf63a0518a28c7707f255ea2f1d09a6f1dbb`;
- Wave 0 checkpoint was already closed;
- historical Knowledge Graph CI evidence existed;
- GitHub Pages build/deployment on the baseline commit was successful;
- no open pull requests at audit start;
- no database, Docker stack or application secrets are required.

## Onboarding gap found

The root README still described the project primarily as the old static catalog of eight teas and instructed users to edit `data/teas.json`, while the later checkpoint established Knowledge Graph v1 as the architectural direction.

At the same time, `js/app.js` still reads `data/teas.json` and `data/ware.json` directly. Therefore both statements are partly true: the graph is the new structured knowledge model, while the deployed static UI remains legacy-JSON-driven.

Project Ready v1 makes this boundary explicit instead of pretending the graph already renders the website.

## CI gap found

The old `Validate Knowledge Graph` workflow used path filters. Documentation and static-site-only commits could therefore reach `main` without the repository validation workflow.

Project Ready v1 changes CI to run on every push/PR to `main` and validates both layers:

- Python syntax and pinned dependency install;
- Knowledge Graph schema/relations;
- reverse graph index generation;
- legacy JSON syntax;
- static HTTP smoke for core pages and JSON files;
- graph-index artifact upload.

## Project Ready additions

- rewritten root `README.md` as canonical onboarding entry point;
- new `PROJECT_STATUS.md` with current state and ONE NEXT ACTION;
- new `AGENTS.md` with session-start/session-end protocol;
- Python 3.12 marker;
- expanded CI covering the whole repository rather than graph-only paths.

No tea facts, product facts, supplier data, schema semantics or public content are intentionally changed by this Project Ready work.

## Remaining limitations

- graph-to-static-site generation is not implemented;
- legacy JSON can drift from graph entities;
- custom-domain state is not confirmed by this repository-only audit;
- `main` is not branch protected on the audited baseline;
- Wave 0 is foundation rather than broad encyclopedia coverage.

## ONE NEXT ACTION

Add or normalize the six base `tea_type` entities as the first small Wave 1 slice. Validate and rebuild the graph index, require green CI on the exact PR head, then merge before proceeding to provinces/regions/terminology.
