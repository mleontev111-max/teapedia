# Teapedia Knowledge Graph Plan

## Status
This document supersedes the blog-first interpretation of `TEAPEDIA_PLAN.md`. The earlier 129-article plan remains useful as a content backlog, but the primary architecture is now entity-first and schema-first.

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
