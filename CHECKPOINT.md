# CHECKPOINT: 2026-09-03 — RAW Knowledge Store architecture

## Status

Accepted as the official target architecture. This checkpoint extends the
existing Knowledge Graph and editorial pipeline; it does not replace them or
change the allowlisted GitHub Pages deploy.

## Git evidence

- exact `origin/main` SHA before work: `79c73aef572092b3f7c1ad3fb2189f98af3bd9ec`
- working branch: `architecture/raw-knowledge-store`
- architecture implementation SHA: `f47bb392a24c3c9f2efc1c7d2e8955e25304c2bc`
- pull request: `#5` — https://github.com/mleontev111-max/teapedia/pull/5

## Accepted decisions

- canonical entity, not `canonical_article`;
- multilingual names without mandatory canonical English;
- explicit claims, evidence and conflict handling;
- immutable/versioned RAW documents and derived document versions;
- assets addressed by SHA-256, with rights and publication states separated;
- PostgreSQL as the operational knowledge store;
- YAML/Git as the curated graph/editorial layer;
- semantic chunks based on document sections;
- pgvector installed early, embeddings deferred behind provenance and quality;
- roadmap order: schema/migration, Teapedia collector, TeaTerra collector,
  first 100 audited documents, then scale.

## Safety invariants

The existing YAML entity contract, editorial `draft -> review -> published`
gate and `build/public` allowlist remain unchanged. No RAW, database or private
editorial content is added to the Pages artifact.

---

# 🎯 CHECKPOINT: Teapedia — Knowledge Graph Wave 0

## Дата
23 августа 2026

## Статус
**✅ Wave 0 закрыта. Knowledge Graph v1 проверен автоматическим CI.**

## Главный принцип
Teapedia развивается как **knowledge graph**, а не как блог. HTML-страницы являются представлением структурированных сущностей и их связей.

## Канонические документы
- `SCHEMA.md` — Knowledge Graph Schema v1 (`1.0.0`).
- `KNOWLEDGE_GRAPH_PLAN.md` — entity-first план развития примерно до 140 фундаментальных сущностей.
- `TEAPEDIA_PLAN.md` — тематический backlog контента.

## ✅ Что реализовано в Wave 0

- постоянные ID в lowercase Latin `kebab-case`;
- разделение `Tea → TeaBatch → Product`;
- направленные relations;
- автоматические обратные связи через generated index;
- tasting как структурированные поля;
- source/fact-check policy;
- статусы `draft/review/published/deprecated`;
- автоматический validator;
- автоматический reverse-index builder;
- GitHub Actions CI.

## 🧩 Эталонные сущности

1. `province/fujian`
2. `region/anxi`
3. `cultivar/tieguanyin`
4. `tea_type/oolong`
5. `tea/tieguanyin`
6. `brewing/oolong-gongfu`
7. `terminology/hui-gan`

## 🛍️ Первый реальный граф THE CHAI

Добавлены:
- `producer/anxi-yaohui-tea-shop`
- `tea_batch/tieguanyin-anxi-nongxiang-2026-yaohui`
- `product/tieguanyin-nongxiang-7g-piece`
- `product/tieguanyin-nongxiang-loose`

Розничная модель:
- пакет **7 г** продаётся как `piece`;
- чай из исходной упаковки **250 г** продаётся по граммам (`sale_unit: gram`);
- 250 г не является фиксированной розничной фасовкой.

Не подтверждённые сведения партии оставлены неизвестными/непроверенными: сезон, конкретная деревня, высота, точный культивар партии, степень обжарки.

## 🔗 Проверенная цепочка

```text
Product 7g ─┐
            ├→ TeaBatch → Tea: Tieguanyin → TeaType: Oolong
Loose tea ──┘               │
                            ├→ Region: Anxi → Province: Fujian
                            ├→ Cultivar: Tieguanyin
                            ├→ Brewing: Oolong Gongfu
                            └→ Terminology: Hui Gan

TeaBatch → Producer/Supplier: Anxi Yaohui
```

## 🧪 Автоматическая проверка

Файлы:
- `requirements.txt`
- `scripts/validate_graph.py`
- `scripts/build_graph_index.py`
- `.github/workflows/validate-knowledge-graph.yml`
- `.gitignore`

Валидатор проверяет:
- типы сущностей;
- обязательные поля;
- `kebab-case` ID;
- соответствие `folder/type/id/filename`;
- schema version;
- статусы;
- допустимые relations;
- существование target entity;
- дубликаты сущностей и relations.

`build_graph_index.py` строит `data/generated/graph-index.json` и вычисляет incoming/reverse links из прямых YAML-связей.

## ✅ CI-подтверждение

Технический PR `#1` использован для реального теста pipeline.

Workflow: `Validate Knowledge Graph`  
Run: `32665804648`  
Result: **SUCCESS**

Успешно прошли шаги:
- установка зависимостей;
- валидация сущностей и relations;
- генерация reverse graph index;
- проверка summary;
- загрузка generated graph artifact.

PR #1 после зелёного CI объединён в `main`.

## 📁 Текущая data-архитектура

```text
data/entities/
├── province/
├── region/
├── cultivar/
├── tea_type/
├── tea/
├── tea_batch/
├── product/
├── producer/
├── brewing/
└── terminology/
```

В Wave 1 будут добавляться предусмотренные Schema v1 типы, включая `processing`, `teaware`, `history`.

## ▶️ Следующий этап: Wave 1

Цель — расширить фундамент графа без массового HTML-дублирования.

Приоритет Wave 1:
1. 6 базовых категорий чая;
2. 7 ключевых провинций;
3. ключевые регионы/терруары;
4. 10 базовых терминов;
5. базовые гайды по завариванию;
6. все новые узлы проходят CI до попадания в стабильный checkpoint.

---

© 2026 Teapedia × THE CHAI
