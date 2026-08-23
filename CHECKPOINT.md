# 🎯 CHECKPOINT: Teapedia — Knowledge Graph v1

## Дата
23 августа 2026

## Статус
**Wave 0 / Schema-first начата и базовая модель зафиксирована.**

## Главная архитектурная идея
Teapedia развивается как **граф знаний**, а не как блог.

Основной путь:
`Tea → Cultivar / Region / TeaType / Brewing / Terminology`

Коммерческий слой отделён:
`Tea → TeaBatch → Product → marketplace listing / QR`.

## Канонические документы
- `SCHEMA.md` — технический контракт Knowledge Graph v1.
- `KNOWLEDGE_GRAPH_PLAN.md` — волны 0–3 и целевая entity-first модель.
- `TEAPEDIA_PLAN.md` — сохраняется как контентный backlog и тематический план.

## ✅ Что создано в Wave 0

### Schema v1
Зафиксированы:
- постоянные IDs в lowercase Latin kebab-case;
- типы сущностей;
- общий набор полей;
- направленные relations;
- генерация обратных связей индексатором;
- разделение Tea / TeaBatch / Product;
- структурная tasting-модель;
- правила источников и фактчека;
- версионирование схемы.

### 7 эталонных сущностей
1. `data/entities/province/fujian.yml`
2. `data/entities/region/anxi.yml`
3. `data/entities/cultivar/tieguanyin.yml`
4. `data/entities/tea_type/oolong.yml`
5. `data/entities/tea/tieguanyin.yml`
6. `data/entities/brewing/oolong-gongfu.yml`
7. `data/entities/terminology/hui-gan.yml`

## Проверенная связность эталона

```text
Tea: tieguanyin
├── HAS_TYPE → tea_type: oolong
├── MADE_FROM → cultivar: tieguanyin
├── GROWN_IN → region: anxi
├── BREW_GUIDE → brewing: oolong-gongfu
└── RELATED_TERM → terminology: hui-gan

region: anxi
└── PART_OF → province: fujian

cultivar: tieguanyin
└── ORIGINATES_IN → region: anxi
```

Таким образом уже представим путь:
`Tea → Region → Province` и связи Tea с типом, культиваром, завариванием и терминологией.

## Целевой фундамент
Около **140 сущностей**:
- TeaType — 8
- Region/Province/Terroir — 27
- Cultivar — 15
- Tea — 30
- Processing — 10
- Teaware — 10
- History — 8
- Brewing — 9
- Terminology — 25+

Ориентир: ~85 полноценных страниц + ~55 коротких справочных узлов.

## Волны

### Wave 0 — Schema
Сейчас.

### Wave 1 — 35 сущностей
6 категорий, 7 провинций, 5 терруарных/горных систем, 10 терминов, 7 brewing-guides.

### Wave 2 — 50 сущностей
20 культовых чаёв, 10 культиваров, 8 технологий, 12 регионов/деревень.

### Wave 3 — 55 сущностей
История, посуда, расширенный глоссарий, первые реальные TeaBatch/Product THE CHAI и QR-связи.

## Важные правила
- Не менять ID из-за изменения названия или URL.
- Не хранить обратные связи вручную.
- Не смешивать энциклопедический Tea с конкретной партией или SKU.
- Tasting конкретной партии хранить структурно на TeaBatch.
- Фактологически спорные данные не переводить в `published` без источников.
- Health/science claims требуют усиленного фактчека.

## Текущий риск / незавершённость
- 7 эталонных сущностей пока имеют статус `draft` и минимальные sources.
- Автоматический валидатор связей ещё не создан.
- Генератор обратного индекса ещё не создан.
- TeaBatch и Product описаны схемой, но эталонные файлы пока не заведены.

## Следующий шаг
**Завершить Wave 0 технически:**
1. добавить schema validation;
2. добавить link validator, проверяющий существование `type + id`;
3. создать генератор обратных связей/индекса;
4. завести тестовые `TeaBatch` и `Product`, чтобы пройти полный путь `Product → TeaBatch → Tea → Region → Province`;
5. только после этого начинать массовое наполнение Wave 1.

## Восстановление
При проблемах сверяться сначала с `SCHEMA.md`, затем `KNOWLEDGE_GRAPH_PLAN.md`, затем этим checkpoint. Предыдущий `TEAPEDIA_PLAN.md` не удалять: он остаётся тематическим backlog.

---
© 2026 Teapedia × THE CHAI
