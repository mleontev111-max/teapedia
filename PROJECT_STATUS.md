# PROJECT_STATUS.md — Teapedia

Updated: 2026-09-03

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
- the editorial admin is Git-first and intentionally has no direct server-side save/authentication on GitHub Pages;
- the first imported article remains a draft and its candidate image remains blocked pending separate license verification.

## ONE NEXT ACTION

Review the Russian Bai Hao Yin Zhen draft, independently verify its factual claims and the source image license, then move it to `review` without publishing it yet.
