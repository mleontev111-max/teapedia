# PROJECT_STATUS.md — Teapedia

Updated: 2026-08-31

Teapedia currently contains two layers: a static HTML/JavaScript presentation that reads `data/teas.json` and `data/ware.json`, and Knowledge Graph v1 entities under `data/entities/`. The graph is the structured model for new knowledge, but it is not yet automatically rendered into the legacy static catalog.

There is no application database, Docker stack, `.env`, or runtime secret requirement.

## Clean start

Use Python 3.12, create a local virtual environment, install `requirements.txt`, run the graph validator and reverse-index builder, then serve the repository with `python -m http.server 8000` and open `http://127.0.0.1:8000/`.

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

## ONE NEXT ACTION

Add or normalize the six base `tea_type` entities as the first small Wave 1 slice, validate them, rebuild the graph index, and require green CI on the exact PR head before merge.
