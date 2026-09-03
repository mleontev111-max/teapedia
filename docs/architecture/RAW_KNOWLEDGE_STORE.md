# Teapedia: RAW Knowledge Store and publishing architecture

**Status:** accepted architecture  
**Accepted:** 2026-09-03  
**Scope:** future ingestion and operational knowledge storage; the existing Knowledge Graph and GitHub Pages publishing path remain active.

## 1. Canonical flow

```text
Sources
  -> immutable RAW documents and assets
  -> processing jobs and document versions
  -> section-based semantic chunks
  -> claims + evidence + conflicts
  -> entities + multilingual names + relations
  -> curated Knowledge Graph (YAML/Git)
  -> editorial draft -> review -> published
  -> allowlisted public Teapedia on GitHub Pages

Later consumers:
  PostgreSQL + pgvector -> retrieval/RAG -> THE CHAI AI
```

The canonical knowledge object is an **entity**, never a `canonical_article`. An article is a reviewed editorial projection of entities, relations and supported claims.

## 2. System boundaries

### Immutable evidence layer

Collectors append source material to object storage and register it in PostgreSQL. They never rewrite an earlier capture. `source_versions` points to the exact RAW object, checksum and acquisition metadata. Re-fetching the same URL creates either a checksum-identical observation or a new version.

Assets are content-addressed by SHA-256. Binary files belong in S3-compatible storage (S3, R2 or B2), not in PostgreSQL. `rights_status` is independent from `publication_status`: owning or verifying a file does not automatically approve it for publication, and publication approval does not invent usage rights.

### Operational knowledge store

PostgreSQL is the operational source of truth for source history, processing lineage, extracted claims, evidence, conflicts, entity candidates and relations. Every derived record retains pointers to the source version and, where possible, a section/chunk locator.

Processing is repeatable and versioned. Cleaner, translator, extractor and classifier changes create new `document_versions`; they do not mutate RAW. Failed work is retained in `processing_jobs` with diagnostics and can be retried idempotently.

### Curated and public layers

`data/entities/**/*.yml` remains the curated Knowledge Graph contract. `content/articles/*.json` and `content/media/*.json` remain the Git-reviewed editorial layer. Promotion from PostgreSQL into Git is an explicit review step, not an automatic database export.

The existing safe Pages path is unchanged:

```text
curated YAML + editorial JSON
  -> validators/builders
  -> build/public explicit allowlist
  -> GitHub Pages
```

RAW objects, processing data, non-published articles, the local admin UI and database credentials must never enter `build/public`.

## 3. Language model

No language is universally canonical. A stable language-independent entity ID anchors names in `entity_names`:

- original script and source spelling are preserved;
- Russian, Chinese, English, pinyin and other forms are separate names;
- language, script, transliteration system and name role are explicit;
- a preferred name is selected per entity + language/context, not globally;
- translation never replaces original evidence.

English may be generated for interoperability, but it is not required for an entity to exist or become canonical.

## 4. Claims, evidence and conflicts

A claim is an atomic, attributable assertion: subject, predicate, value or object entity, qualifiers and confidence. Evidence links the claim to exact source versions and optional chunks. Multiple sources may support or dispute a claim.

Conflicting claims coexist in the operational store. Curation records their review state and resolution; it must not erase the losing evidence. A relation is a graph edge accepted from reviewed claims, with its provenance retained. Marketing text, supplier assertions and editorial conclusions must remain distinguishable.

## 5. Chunking and pgvector

Chunks follow semantic document sections (heading path, paragraphs, tables, captions) rather than arbitrary fixed token windows. Each chunk retains stable ordering, character offsets and its parent `document_version`.

Install the `vector` extension in the first PostgreSQL migration so schema evolution is ready for embeddings. Embedding generation and retrieval tuning are not MVP priorities: first establish reliable capture, lineage, claims, entity resolution and review. Vector columns/indexes can be added when a chosen embedding model and evaluation set exist.

## 6. MVP database contract

The executable proposal is `db/migrations/0001_raw_knowledge_store.sql`.

| Table | Responsibility |
| --- | --- |
| `sources` | Source identity, ownership and collector policy |
| `source_documents` | Stable logical URL/document within a source |
| `source_versions` | Immutable RAW capture with checksum and object key |
| `assets` | SHA-256-addressed binary metadata and separate rights/publication states |
| `processing_jobs` | Idempotent queued/running/completed/failed work |
| `document_versions` | Versioned clean/translated/derived documents |
| `document_chunks` | Ordered semantic sections with provenance |
| `entities` | Language-independent canonical entity identity |
| `entity_names` | Multilingual names, scripts and transliterations |
| `claims` | Atomic assertions and conflict/review state |
| `claim_evidence` | Support/dispute links to source versions/chunks |
| `relations` | Curated entity-to-entity edges with claim provenance |
| `article_sources` | Editorial article-to-evidence linkage |

UUIDs are internal database identifiers. Existing stable graph identifiers remain lowercase `kebab-case` and are stored in `entities.canonical_key`; the database must not force an ID migration in YAML.

## 7. MVP delivery sequence

1. Apply and validate the first schema migration in an isolated PostgreSQL environment; document backup, rollback and object-store configuration.
2. Implement a Teapedia collector that stores unchanged responses and capture metadata, then emits only versioned processing records.
3. Implement a TeaTerra collector with the same contract and source-specific rate/rights policy.
4. Ingest and manually audit the first 100 documents across both sources, measuring duplicate rate, extraction accuracy, provenance completeness and rights coverage.
5. Scale collectors and workers only after the audit gates pass; then introduce evaluated embeddings, pgvector retrieval/RAG and THE CHAI AI consumers.

## 8. Non-goals for the first migration

- replacing YAML or Git review;
- generating or publishing articles without editorial approval;
- changing the existing entity IDs or graph validator;
- routing GitHub Pages through PostgreSQL;
- bulk scraping before source terms, rate limits and asset rights are recorded;
- treating embeddings as facts or as a substitute for evidence.
