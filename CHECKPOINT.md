# 🎯 CHECKPOINT: Teapedia — Knowledge Graph Wave 0

## Дата
23 августа 2026

## Статус
**Wave 0 технически реализована. Перед окончательным закрытием требуется подтвердить зелёный прогон GitHub Actions.**

## Главный принцип
Teapedia развивается как **knowledge graph**, а не как блог. HTML-страницы являются представлением структурированных сущностей и их связей.

## ✅ Что уже зафиксировано

- `SCHEMA.md` — Knowledge Graph Schema v1 (`1.0.0`).
- `KNOWLEDGE_GRAPH_PLAN.md` — план развития графа примерно до 140 фундаментальных сущностей.
- `TEAPEDIA_PLAN.md` — тематический backlog контента.
- постоянные ID в lowercase Latin `kebab-case`.
- разделение `Tea → TeaBatch → Product`.
- направленные relations и автоматически вычисляемые обратные связи.
- tasting как структурированные поля, а не только проза.
- политика источников и статусов `draft/review/published/deprecated`.

## 🧩 Эталонный граф

Созданы базовые узлы:

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

Не подтверждённые сведения партии сохранены как неизвестные/непроверенные: конкретный сезон, деревня, высота, точный культивар партии и степень обжарки.

## 🔗 Проверяемая цепочка

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

## 🧪 Автоматическая проверка графа

Добавлены:

- `requirements.txt` — PyYAML;
- `scripts/validate_graph.py` — валидатор сущностей и связей;
- `scripts/build_graph_index.py` — генератор общего и обратного индекса;
- `.github/workflows/validate-knowledge-graph.yml` — GitHub Actions CI;
- `.gitignore` — `data/generated/` не коммитится вручную.

### Валидатор проверяет

- допустимые типы сущностей;
- обязательные поля;
- ID в `kebab-case`;
- соответствие `folder/type/id/filename`;
- версии схемы;
- допустимые статусы;
- допустимые relations;
- существование target entity для каждой связи;
- дублирующиеся сущности и relations.

### Reverse index

`build_graph_index.py` строит `data/generated/graph-index.json` из исходных YAML и автоматически вычисляет входящие связи. Обратные связи не хранятся вручную, чтобы избежать расхождений.

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

По мере Wave 1 добавляются предусмотренные Schema v1 типы: `processing`, `teaware`, `history` и другие.

## ⚠️ Что ещё не считаем завершённым

1. Нужно увидеть успешный CI-прогон `Validate Knowledge Graph` на `main`.
2. После зелёного CI создать стабильную контрольную ветку `checkpoint/knowledge-graph-wave0`.
3. Затем начинать Wave 1 и расширять фундаментальные сущности.

## ▶️ Следующий шаг

**Подтвердить CI → закрыть Wave 0 → начать Wave 1.**

Первая Wave 1 должна расширять граф системно: категории чая, ключевые провинции/регионы, базовые термины и гайды по завариванию — без массового HTML-дублирования.

---

© 2026 Teapedia × THE CHAI
