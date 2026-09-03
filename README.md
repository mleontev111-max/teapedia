# Teapedia

Teapedia — энциклопедия китайского чая и структурированный knowledge graph для THE CHAI.

Цель Project Ready: новый человек или ИИ должен без истории чатов понять, что является текущим сайтом, что является новым knowledge graph, как всё проверить и какое одно действие делать дальше.

## Обязательный старт рабочего сеанса

Перед изменениями:

```bash
git fetch origin
git status --short --branch
git log -1 --oneline
```

Затем прочитать:

1. `README.md`;
2. `PROJECT_STATUS.md`;
3. `AGENTS.md`;
4. `SCHEMA.md` — если работа касается graph entities;
5. `CHECKPOINT.md` и планы — только для исторического/продуктового контекста.

GitHub `origin/main` — канонический код. Исторические checkpoint SHA не заменяют проверку текущего HEAD.

## Архитектура: два слоя

### 1. Текущий статический сайт

Сайт — обычные HTML/CSS/JavaScript-файлы без серверной БД, Docker и application secrets.

Основные файлы:

```text
index.html
tea.html
ware.html
css/
js/app.js
data/teas.json
data/ware.json
encyclopedia/
```

`js/app.js` сейчас напрямую загружает:

- `data/teas.json` — legacy presentation catalog чая;
- `data/ware.json` — presentation catalog посуды.

Поэтому изменение YAML knowledge graph **само по себе пока не меняет публичный HTML-каталог**.

### 2. Knowledge Graph v1

Новая каноническая модель структурированных знаний находится в:

```text
data/entities/<entity-type>/<id>.yml
```

Schema source of truth:

- `SCHEMA.md` — schema v1;
- `scripts/validate_graph.py` — executable validation rules;
- `scripts/build_graph_index.py` — generated reverse/incoming relations index;
- `KNOWLEDGE_GRAPH_PLAN.md` — expansion plan.

Wave 0 закрыла базовую модель `Tea → TeaBatch → Product`, relations, fact-check/source policy и автоматическую валидацию.

Важно: **сейчас это две связанные, но ещё не автоматически синхронизированные модели.** Не копировать сведения между YAML и legacy JSON наугад. Если задача требует синхронизации graph → site, это отдельный этап архитектуры.

## Clean start

Требования:

- Git;
- Python 3.12 для graph validators;
- браузер;
- `pip`.

БД, Docker, Node.js и `.env` для текущего проекта не требуются.

```bash
git clone <repository-url>
cd teapedia
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Проверить graph:

```bash
python scripts/validate_graph.py
python scripts/build_graph_index.py
python -m json.tool data/teas.json >/dev/null
python -m json.tool data/ware.json >/dev/null
```

Запустить статический сайт:

```bash
python -m http.server 8000
```

Открыть:

```text
http://127.0.0.1:8000/
```

Не открывать `index.html` через `file://`: браузер может блокировать `fetch()` JSON-файлов. Использовать локальный HTTP server.

## CI

GitHub CI должен выполняться на каждом PR в `main` и каждом push в `main`, а не только при изменении YAML graph.

CI проверяет:

- установку pinned Python dependencies;
- Python syntax;
- Knowledge Graph schema/relations;
- генерацию reverse graph index;
- валидность legacy JSON;
- статический HTTP smoke для основных страниц/data files;
- generated graph artifact.

CI не использует secrets и не делает внешних data writes.

## GitHub Pages

Репозиторий публикуется через GitHub Pages. На baseline `main` `94c2bf63...` GitHub Pages build/deployment завершился SUCCESS.

Ожидаемый repository Pages URL:

```text
https://mleontev111-max.github.io/teapedia/
```

README старой версии содержал инструкцию по будущему `teapedia.ru`; **не считать custom domain настроенным только по этой инструкции**. Текущую привязку домена всегда проверять в GitHub/DNS перед изменениями.

## Secrets, БД и контейнеры

Для текущей архитектуры:

- application secrets: нет;
- `.env`: не нужен;
- database: нет;
- Docker containers: нет;
- persistent runtime state: нет.

Все канонические данные лежат в Git как JSON/YAML/content files.

## Как добавлять знания

Для новых graph entities:

1. сначала определить entity type по `SCHEMA.md`;
2. использовать стабильный lowercase `kebab-case` ID;
3. отделять подтвержденный факт от неизвестного;
4. добавлять relations только к существующим targets;
5. запускать validator и index builder;
6. не дублировать массово HTML вручную, если задача относится именно к Knowledge Graph.

Для legacy UI (`data/teas.json`, `data/ware.json`) помнить, что это текущий presentation layer и он пока не generated из YAML graph.

## Редакционные статьи и импорт

Статьи хранятся в `content/articles/*.json`, а метаданные изображений — в
`content/media/*.json`. Команда `python scripts/build_articles.py` проверяет их и
создаёт два разных файла:

- `articles-admin.json` — все статусы для редакционной страницы `/admin/`;
- `articles-public.json` — только одобренные статьи со статусом `published`.

Админка даёт предпросмотр, выбор `draft → review → published` и скачивает
обновлённый JSON. Из-за статической архитектуры GitHub Pages она не записывает
данные на сервер: файл нужно проверить и закоммитить. Это намеренный барьер от
случайной публикации. Сборка отклонит публикацию без редакционного и
лицензионного одобрения или с непроверенным изображением.

Политика источников описана в `SOURCE_POLICY.md`, словарь перевода — в
`TRANSLATION_GLOSSARY.yml`, воспроизводимые импорты — в
`ingestion/teapedia.org/`. Импортёр всегда создаёт только черновик и не скачивает
изображения.

## Safety / что нельзя делать

- Не придумывать происхождение, высоту, сезон, культивар, обработку или supplier facts ради заполнения поля.
- Не считать marketing copy подтвержденным фактом без источника.
- Не менять ID существующей entity без анализа входящих relations.
- Не редактировать generated reverse index как source of truth — он пересобирается script'ом.
- Не считать legacy `teas.json` новым knowledge-graph source of truth.
- Не считать старый README/план доказательством текущего deploy/domain state.
- Не обходить validator, чтобы «починить» CI.

## Текущее состояние и следующий шаг

См. `PROJECT_STATUS.md`.

Выбранный ONE NEXT ACTION после Project Ready: **начать Wave 1 с шести базовых `tea_type` entities как одного небольшого, CI-проверяемого slice, не переходя сразу к массовому наполнению всех ~140 сущностей.**
