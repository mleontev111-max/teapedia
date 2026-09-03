# Source and licensing policy

Teapedia treats imported pages as source material, not as publication-ready copy.
Every import is stored as `draft`; a human reviewer must explicitly move it to
`review` and then `published` in a committed content file.

## Text from teapedia.org

Teapedia pages state that their text is available under CC BY-SA unless a page
says otherwise. For each adaptation we preserve:

- page title, canonical URL and permanent revision URL;
- access date and the license name/link;
- an indication that the Russian text is a translation and adaptation;
- a list of claims that still need independent verification.

CC BY-SA 3.0 permits sharing and adaptation with attribution and ShareAlike.
Adapted text must therefore remain under CC BY-SA 3.0 (or a compatible license)
and must not be presented as an original THE CHAI text. Page-specific notices
override the site-wide footer.

## Images

An article license never automatically clears an image. Each image is a separate
media record with source page, original file URL, author, license, license URL,
and `verification_status`.

- `pending`: not shown anywhere, including draft preview;
- `verified`: may be shown, with visible attribution;
- `rejected`: must not be downloaded or used.

A media record cannot become `verified` while author, exact license, license URL,
and source URL are missing. Published articles may reference only verified media
stored locally in this repository. Hotlinking is not allowed.

## Review and publication

1. Import source metadata and raw material into `ingestion/teapedia.org/`.
2. Write a Russian adaptation in `content/articles/` with status `draft`.
3. Check terminology against `TRANSLATION_GLOSSARY.yml` and verify factual
   claims with independent sources where practical.
4. Move to `review`; record reviewer notes.
5. Move to `published` only after editorial and license approval.

The public build contains only `published` articles. Draft and review content is
available only through the repository/admin manifest and is never promoted by
the importer.
