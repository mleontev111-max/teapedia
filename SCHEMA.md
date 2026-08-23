# Teapedia Knowledge Graph — Schema v1

**Schema version:** 1.0.0  
**Status:** active  
**Created:** 2026-08-23

## 1. Principle

Teapedia is a knowledge graph, not a blog. Content pages are projections of structured entities and their relations.

## 2. ID rules

- IDs are permanent and language-independent.
- Format: lowercase Latin `kebab-case`.
- IDs are unique inside an entity type namespace.
- Renaming Russian/Chinese display names must not change an ID.
- URLs may change; IDs must not.

Examples: `tieguanyin`, `oolong`, `fujian`, `oolong-gongfu`, `hui-gan`.

## 3. Core entity types

### province
Administrative province-level node.
Required: `type`, `id`, `name_ru`, `name_zh`, `pinyin`, `schema_version`, `status`.

### region
Tea-growing region, mountain system, county, village or terroir zone.
Required: core fields + `region_kind` + at least one relation to a parent geography where known.

### cultivar
Tea plant cultivar / recognized plant variety used for tea production.
Required: core fields. Optional origin, botanical notes and aliases must be source-verified before publication.

### tea_type
Taxonomic/processing category used by Teapedia (green, white, yellow, oolong, red, dark; plus defined subtypes).

### tea
Timeless encyclopedic tea concept. It must not contain stock, price or batch-specific claims.

### tea_batch
Concrete harvest/lot/batch of a tea. May contain year, season, producer, processing parameters and tasting observations.

### product
Commercial THE CHAI SKU or offer. Connects commerce to `tea_batch` or, when batch-level data is unavailable, to `tea`.

### processing
Processing method or stage.

### brewing
Reusable brewing guide or protocol.

### teaware
Teaware object/material/type.

### terminology
Glossary concept.

### history
Historical person, text, event or period.

### producer
Producer, factory, master or organization. Reserved in v1 for future population.

## 4. Common fields

```yaml
type: tea
id: tieguanyin
schema_version: 1.0.0
status: draft
name_ru: Те Гуань Инь
name_zh: 铁观音
pinyin: Tiě Guānyīn
aliases: []
tags: []
summary: ""
relations: []
sources: []
```

### Status values
- `draft`
- `review`
- `published`
- `deprecated`

## 5. Relations

Relations are directed edges stored on the source entity.

Allowed v1 relations:
- `PART_OF`
- `CONTAINS`
- `HAS_TYPE`
- `HAS_SUBTYPE`
- `MADE_FROM`
- `GROWN_IN`
- `ORIGINATES_IN`
- `USES_PROCESS`
- `BREW_WITH`
- `BREW_GUIDE`
- `RELATED_TERM`
- `RELATED_TEA`
- `PRODUCED_BY`
- `REPRESENTS`
- `BATCH_OF`
- `SOLD_AS`
- `ASSOCIATED_WITH`

Relation object:

```yaml
- relation: GROWN_IN
  type: region
  id: anxi
```

## 6. Reverse links

Reverse links are **not manually duplicated**. A build/index step will derive them from all forward relations. This prevents drift and contradictions.

Example: if `tea/tieguanyin` has `GROWN_IN -> region/anxi`, the generated Anxi page may automatically show Tieguanyin in a “Teas grown here” section.

## 7. Tasting model

Tasting is structured primarily on `tea_batch`, not on timeless `tea` entities.

Controlled fields:

```yaml
tasting:
  sweetness: medium-high
  astringency: low
  bitterness: low
  body: medium
  aroma: [floral, orchid]
  hui_gan: long
  sheng_jin: medium
  finish: long
```

Controlled scalar values where applicable:
`none`, `very-low`, `low`, `medium-low`, `medium`, `medium-high`, `high`, `very-high`.

Descriptors such as aroma tags must come from a controlled vocabulary maintained in the terminology layer.

## 8. Source and fact-check policy

Every factual field that can be disputed or varies by source should be supported before `published` status.

Recommended source object:

```yaml
sources:
  - title: "Source title"
    url: "https://..."
    accessed: 2026-08-23
    supports: [name_zh, origin]
```

Rules:
- no invented Chinese names, cultivars, origin claims or historical dates;
- uncertain facts remain `draft`/`review`;
- commercial descriptions do not overwrite encyclopedic data;
- health/science claims require especially strong sourcing.

## 9. Tea → TeaBatch → Product separation

```text
Tea (timeless concept)
  ↓ BATCH_OF / inverse derived
TeaBatch (harvest / lot)
  ↓ REPRESENTS / SOLD_AS
Product (THE CHAI SKU)
```

A discontinued product must not remove or invalidate the Tea entity.

## 10. Folder layout

```text
data/entities/
├── province/
├── region/
├── cultivar/
├── tea_type/
├── tea/
├── tea_batch/
├── product/
├── processing/
├── brewing/
├── teaware/
├── terminology/
├── history/
└── producer/
```

## 11. URL policy

Public pages may be generated from entities, for example:
- `/tea/tieguanyin/`
- `/regions/anxi/`
- `/cultivars/tieguanyin/`

The routing layer maps entity type + ID to URLs. Internal relations must use IDs, never hard-coded public URLs.

## 12. Schema versioning

Every entity carries `schema_version`.
- backward-compatible additions: increment minor version (1.1.0)
- breaking field/relation changes: increment major version (2.0.0)
- migrations must be documented before changing existing entity files.

## 13. Wave 0 acceptance criteria

Wave 0 is complete when:
1. Schema v1 is committed.
2. Seven reference entities exist.
3. All reference relations resolve to existing entity IDs where intended.
4. A future `Product → TeaBatch → Tea → Region → Province → TeaType → Brewing` path can be represented without schema changes.
5. Reverse-link generation strategy is fixed.
6. IDs and controlled tasting vocabularies are fixed for v1.
