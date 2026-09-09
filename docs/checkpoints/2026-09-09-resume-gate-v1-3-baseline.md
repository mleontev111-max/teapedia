# Checkpoint — Resume Gate v1.3 rollout baseline

Date: 2026-09-09
Status: rollout candidate
Main baseline: `79c73aef572092b3f7c1ad3fb2189f98af3bd9ec`

## Current main state

The current main editorial continuation is the Bai Hao Yin Zhen draft review/license-verification step. Safe editorial workflow and Pages privacy allowlist are already merged and must not be reconstructed.

## Unmerged work discovered during rollout

PR #5 `architecture/raw-knowledge-store` is durable unmerged architecture work.

Observed head during rollout: `0116df411be5ff078bf89220bc3e9020503ccb79`.
Observed divergence: ahead 2 / behind 0 relative to main `79c73aef...`.

The PR already contains the accepted Sources -> immutable RAW -> processing versions -> claims/entities/relations -> curated Knowledge Graph -> editorial publishing architecture, a PostgreSQL/pgvector-oriented schema proposal, provenance/versioning rules and CI contract checks. Do not reimplement it from scratch.

## Resume-system continuation

Before merging this rollout, require Project Ready Guard + Resume Guard and ordinary Teapedia validation CI on the exact rollout head. After merge, synchronize the resume layer into PR #5 without losing its architecture changes, create/refresh `docs/workstreams/raw-knowledge-store/STATE.md`, and require exact-head continuity + validation PASS before any merge decision on the architecture PR.

## Safety

No publication, no article status change, no image approval, no ingestion write, no database deployment, and no Pages visibility change are part of this rollout.
