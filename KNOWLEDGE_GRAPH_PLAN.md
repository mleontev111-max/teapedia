# Teapedia Knowledge Graph Plan

## Status
This document supersedes the blog-first interpretation of `TEAPEDIA_PLAN.md`. The earlier 129-article plan remains useful as a content backlog, but the primary architecture is now entity-first and schema-first.

As of 2026-09-03, this curated graph is the reviewed middle layer of the wider RAW Knowledge Store architecture documented in `docs/architecture/RAW_KNOWLEDGE_STORE.md`. PostgreSQL stores operational lineage, claims and candidates; promotion into YAML/Git remains explicit and reviewed.

There is no `canonical_article`. The canonical object is a stable, language-independent entity. Names in Russian, Chinese, English, pinyin and other languages are parallel records; English is not mandatory or globally canonical. Articles remain editorial projections.

## Foundation target
Approximately 140 foundational entities:
- TeaType: 8
- Region/Province/Terroir: 27
- Cultivar: 15
- Tea: 30
- Processing: 10
- Teaware: 10
- History: 8
- Brewing: 9
- Terminology: 25+

Expected mix: ~85 full pages + ~55 short reference nodes.

## Wave 0 — Schema
Goal: validate the data model before mass content production.

Reference entities:
- `province/fujian`
- `region/anxi`
- `cultivar/tieguanyin`
- `tea_type/oolong`
- `tea/tieguanyin`
- `brewing/oolong-gongfu`
- `terminology/hui-gan`

Rules:
- IDs are stable lowercase Latin kebab-case.
- Internal links are relations by entity type + ID, not URLs.
- Reverse links are generated, not duplicated manually.
- `Tea`, `TeaBatch`, and `Product` are separate layers.
- `Tasting` is structured primarily at TeaBatch level using controlled vocabulary.
- Disputed factual fields require sources before publication.
- Claims are atomic and preserve evidence, counter-evidence and unresolved conflicts.
- RAW documents and assets are immutable/versioned; derived processing never overwrites them.
- Assets use SHA-256 identity and keep rights approval separate from publication approval.
- Semantic chunks follow document sections and preserve source-version lineage.

## Wave 1 — 35 entities
- 6 tea categories
- 7 key provinces
- 5 mountain/terroir systems
- 10 core terminology nodes
- 7 brewing guides

## Wave 2 — 50 entities
- 20 iconic teas
- 10 cultivars
- 8 processing nodes
- 12 regions/villages

## Wave 3 — 55 entities
- history and legends
- teaware
- expanded glossary
- first live THE CHAI TeaBatch/Product/QR connections

## Success condition
A future product must be able to resolve a path such as:

`Product → TeaBatch → Tea → Region → Province`

and independently connect to:

`Tea → TeaType`, `Tea → Cultivar`, `Tea → Brewing`, `TeaBatch → Tasting`, `Product → marketplace listing`.

The canonical technical contract is `SCHEMA.md`.

For the operational ingestion layer, the canonical technical contract is `docs/architecture/RAW_KNOWLEDGE_STORE.md` plus the migration proposal under `db/migrations/`. These contracts extend rather than replace `SCHEMA.md`.
