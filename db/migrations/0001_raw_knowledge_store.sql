BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TYPE processing_status AS ENUM ('queued', 'running', 'completed', 'failed', 'cancelled');
CREATE TYPE review_status AS ENUM ('candidate', 'review', 'accepted', 'rejected', 'conflicted');
CREATE TYPE evidence_stance AS ENUM ('supports', 'disputes', 'context');
CREATE TYPE rights_status AS ENUM ('unknown', 'restricted', 'permission_required', 'verified');
CREATE TYPE publication_status AS ENUM ('blocked', 'draft', 'review', 'published', 'withdrawn');

CREATE TABLE sources (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_key text NOT NULL UNIQUE,
    name text NOT NULL,
    base_url text,
    source_kind text NOT NULL,
    rights_notes text,
    collector_policy jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE source_documents (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id uuid NOT NULL REFERENCES sources(id),
    canonical_locator text NOT NULL,
    external_id text,
    first_seen_at timestamptz NOT NULL DEFAULT now(),
    last_seen_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_id, canonical_locator)
);

CREATE TABLE source_versions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_document_id uuid NOT NULL REFERENCES source_documents(id),
    captured_at timestamptz NOT NULL,
    sha256 char(64) NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
    object_key text NOT NULL,
    media_type text NOT NULL,
    byte_size bigint NOT NULL CHECK (byte_size >= 0),
    http_status integer,
    response_headers jsonb NOT NULL DEFAULT '{}'::jsonb,
    collector_version text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_document_id, captured_at),
    UNIQUE (source_document_id, sha256)
);

CREATE TABLE assets (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    sha256 char(64) NOT NULL UNIQUE CHECK (sha256 ~ '^[0-9a-f]{64}$'),
    object_key text NOT NULL UNIQUE,
    media_type text NOT NULL,
    byte_size bigint NOT NULL CHECK (byte_size >= 0),
    source_version_id uuid REFERENCES source_versions(id),
    rights_status rights_status NOT NULL DEFAULT 'unknown',
    rights_basis text,
    publication_status publication_status NOT NULL DEFAULT 'blocked',
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE processing_jobs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_version_id uuid NOT NULL REFERENCES source_versions(id),
    job_type text NOT NULL,
    processor_version text NOT NULL,
    parameters jsonb NOT NULL DEFAULT '{}'::jsonb,
    idempotency_key text NOT NULL UNIQUE,
    status processing_status NOT NULL DEFAULT 'queued',
    attempts integer NOT NULL DEFAULT 0 CHECK (attempts >= 0),
    error_detail text,
    created_at timestamptz NOT NULL DEFAULT now(),
    started_at timestamptz,
    finished_at timestamptz
);

CREATE TABLE document_versions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_version_id uuid NOT NULL REFERENCES source_versions(id),
    processing_job_id uuid REFERENCES processing_jobs(id),
    parent_document_version_id uuid REFERENCES document_versions(id),
    version_kind text NOT NULL,
    language_code text,
    content_sha256 char(64) NOT NULL CHECK (content_sha256 ~ '^[0-9a-f]{64}$'),
    content_text text NOT NULL,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_version_id, version_kind, content_sha256)
);

CREATE TABLE document_chunks (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    document_version_id uuid NOT NULL REFERENCES document_versions(id),
    ordinal integer NOT NULL CHECK (ordinal >= 0),
    section_path text[] NOT NULL DEFAULT ARRAY[]::text[],
    chunk_kind text NOT NULL,
    content_text text NOT NULL,
    start_offset integer CHECK (start_offset IS NULL OR start_offset >= 0),
    end_offset integer CHECK (end_offset IS NULL OR end_offset >= start_offset),
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (document_version_id, ordinal)
);

CREATE TABLE entities (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type text NOT NULL,
    canonical_key text NOT NULL CHECK (canonical_key ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$'),
    review_status review_status NOT NULL DEFAULT 'candidate',
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (entity_type, canonical_key)
);

CREATE TABLE entity_names (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id uuid NOT NULL REFERENCES entities(id),
    name text NOT NULL,
    language_code text,
    script_code text,
    transliteration_system text,
    name_role text NOT NULL DEFAULT 'alias',
    is_preferred boolean NOT NULL DEFAULT false,
    source_version_id uuid REFERENCES source_versions(id),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE NULLS NOT DISTINCT (entity_id, name, language_code, script_code, transliteration_system)
);

CREATE TABLE claims (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_entity_id uuid NOT NULL REFERENCES entities(id),
    predicate text NOT NULL,
    object_entity_id uuid REFERENCES entities(id),
    value_json jsonb,
    qualifiers jsonb NOT NULL DEFAULT '{}'::jsonb,
    confidence numeric(4,3) CHECK (confidence BETWEEN 0 AND 1),
    review_status review_status NOT NULL DEFAULT 'candidate',
    conflict_group_id uuid,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK ((object_entity_id IS NOT NULL) <> (value_json IS NOT NULL))
);

CREATE TABLE claim_evidence (
    claim_id uuid NOT NULL REFERENCES claims(id),
    source_version_id uuid NOT NULL REFERENCES source_versions(id),
    document_chunk_id uuid REFERENCES document_chunks(id),
    stance evidence_stance NOT NULL DEFAULT 'supports',
    locator jsonb NOT NULL DEFAULT '{}'::jsonb,
    note text,
    PRIMARY KEY (claim_id, source_version_id, stance)
);

CREATE TABLE relations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_entity_id uuid NOT NULL REFERENCES entities(id),
    relation_type text NOT NULL,
    object_entity_id uuid NOT NULL REFERENCES entities(id),
    claim_id uuid REFERENCES claims(id),
    review_status review_status NOT NULL DEFAULT 'candidate',
    qualifiers jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (subject_entity_id, relation_type, object_entity_id)
);

CREATE TABLE article_sources (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    article_key text NOT NULL,
    source_version_id uuid NOT NULL REFERENCES source_versions(id),
    claim_id uuid REFERENCES claims(id),
    citation_role text NOT NULL DEFAULT 'source',
    locator jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE NULLS NOT DISTINCT (article_key, source_version_id, claim_id, citation_role)
);

CREATE FUNCTION reject_immutable_change() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION '% is immutable; append a new version instead', TG_TABLE_NAME;
END;
$$;

CREATE TRIGGER source_versions_are_immutable
BEFORE UPDATE OR DELETE ON source_versions
FOR EACH ROW EXECUTE FUNCTION reject_immutable_change();

CREATE TRIGGER document_versions_are_immutable
BEFORE UPDATE OR DELETE ON document_versions
FOR EACH ROW EXECUTE FUNCTION reject_immutable_change();

CREATE INDEX source_versions_document_idx ON source_versions (source_document_id, captured_at DESC);
CREATE INDEX processing_jobs_queue_idx ON processing_jobs (status, created_at);
CREATE INDEX document_chunks_version_idx ON document_chunks (document_version_id, ordinal);
CREATE INDEX entity_names_lookup_idx ON entity_names (lower(name));
CREATE INDEX claims_subject_predicate_idx ON claims (subject_entity_id, predicate);
CREATE INDEX claims_conflict_idx ON claims (conflict_group_id) WHERE conflict_group_id IS NOT NULL;
CREATE INDEX claim_evidence_source_idx ON claim_evidence (source_version_id);
CREATE INDEX relations_subject_idx ON relations (subject_entity_id, relation_type);
CREATE INDEX relations_object_idx ON relations (object_entity_id, relation_type);
CREATE INDEX article_sources_article_idx ON article_sources (article_key);

COMMENT ON TABLE source_versions IS 'Immutable registrations of exact RAW captures; corrections append a new row.';
COMMENT ON TABLE document_versions IS 'Versioned derivatives. Never overwrite RAW content in source_versions/object storage.';
COMMENT ON COLUMN assets.rights_status IS 'Legal/permission assessment, independent from editorial publication_status.';
COMMENT ON COLUMN entities.canonical_key IS 'Stable language-independent key compatible with the curated YAML Knowledge Graph.';

COMMIT;
