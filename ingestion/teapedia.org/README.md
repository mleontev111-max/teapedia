# teapedia.org ingestion

This directory contains reproducible source snapshots and import metadata. Run:

```bash
python scripts/import_teapedia.py --title "Bai Hao Yin Zhen"
```

The importer calls the public MediaWiki API, records source/revision metadata and
creates a `draft` scaffold. It never writes `review` or `published`, downloads no
images, and never edits the public manifest. Translation and editorial work are
deliberately separate human-reviewed steps.

Committed imports live under `ingestion/teapedia.org/imports/<slug>/`. Raw source
text is evidence for editing and must not be rendered on the public site.
