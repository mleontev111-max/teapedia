# Checkpoint — current editorial continuation

Date: 2026-09-03
Status: current product checkpoint
Main baseline: `79c73aef572092b3f7c1ad3fb2189f98af3bd9ec`

## Verified current state

Teapedia has two content layers: legacy browser-facing JSON and Knowledge Graph entities. A Git-first editorial workflow is merged with `draft -> review -> published`, licensed-media handling, Teapedia ingestion, and an explicit public-site allowlist that excludes editorial/admin/private inputs.

The first Russian Bai Hao Yin Zhen article already exists as a **draft**. Its candidate image is **not approved for publication** because the source/license still requires independent verification.

## ONE NEXT ACTION

Review the existing Russian Bai Hao Yin Zhen draft, independently verify its factual claims and the source-image license, then move the article to `review` without publishing it yet.

## Safety

- Do not recreate the article as a new draft merely because a new session cannot find it at first.
- Do not move it directly to `published`.
- Do not publish or approve the candidate image until license/provenance is verified.
- Do not invent tea/history/producer facts to fill gaps.
- Keep private editorial/admin inputs outside the public Pages artifact.

## Parallel unmerged work

Architecture PR #5 (`architecture/raw-knowledge-store`) is separate durable work. It proposes the RAW/provenance/PostgreSQL-pgvector architecture and must not be confused with the current editorial NEXT ACTION or reimplemented from scratch.
