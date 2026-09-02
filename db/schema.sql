-- Supabase (Postgres + pgvector) schema for everything in this system that
-- GROWS over time. Static training artifacts (subclusters.json, startups.json,
-- interaction_matrix.npy) stay as deployed files: they are regenerated wholesale
-- by offline scripts, never mutated at runtime, so a database buys nothing.
--
-- Apply with:  psql "$DATABASE_URL" -f db/schema.sql   (idempotent, safe to re-run)

CREATE EXTENSION IF NOT EXISTS vector;

-- ---------------------------------------------------------------------------
-- announcements / articles: provenance containers. Never scored, never
-- embedded - they exist so every fact can be traced back to its source.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS announcements (
    id              TEXT PRIMARY KEY,       -- e.g. lpu_ann_<content hash>
    source          TEXT NOT NULL,          -- 'lpu' | 'bbc_world' | 'aljazeera' | ...
    content_key     TEXT,                   -- dedup key; see lpu_ingestion._content_key
    source_file     TEXT,
    source_row_id   TEXT,
    title           TEXT NOT NULL DEFAULT '',
    body            TEXT NOT NULL DEFAULT '',
    uploaded_by     TEXT,
    link            TEXT,
    links           JSONB NOT NULL DEFAULT '[]'::jsonb,
    published       TIMESTAMPTZ,            -- NULL = date unparseable, row still kept
    raw_date        TEXT,
    ingested_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);
-- Content-hash uniqueness, NOT the source's own id: for the LPU scrape files
-- that id is per-file row numbering and collides across files while pointing at
-- completely different announcements (verified: all 16,218 shared ids differ).
CREATE UNIQUE INDEX IF NOT EXISTS announcements_content_key_uniq
    ON announcements (content_key) WHERE content_key IS NOT NULL;
CREATE INDEX IF NOT EXISTS announcements_published_idx ON announcements (published DESC);

-- ---------------------------------------------------------------------------
-- facts: the scored unit. One announcement decomposes into 1..N atomic facts.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS facts (
    id                  TEXT PRIMARY KEY,
    announcement_id     TEXT REFERENCES announcements (id) ON DELETE CASCADE,
    fact_text           TEXT NOT NULL,
    entities            JSONB NOT NULL DEFAULT '[]'::jsonb,
    published           TIMESTAMPTZ,
    scope               TEXT NOT NULL,      -- 'LPU' | 'World' | 'India' | ...
    source              TEXT NOT NULL,      -- 'lpu' | 'bbc_world' | ...
    pestle_scores       JSONB NOT NULL,     -- {political: 0.0, ...} 6 dims
    porters_scores      JSONB NOT NULL,     -- {supplier_power: 0.0, ...} 5 dims
    polarity            TEXT NOT NULL,
    mention_count       INTEGER NOT NULL DEFAULT 1,
    -- Ingestion honesty flags: false means "the model call failed", NOT
    -- "genuinely atomic" / "genuinely no market relevance". Kept in the DB for
    -- the same reason they're kept in the JSON - a silent failure must stay
    -- distinguishable from a real result.
    decomposition_ok    BOOLEAN NOT NULL DEFAULT TRUE,
    classification_ok   BOOLEAN NOT NULL DEFAULT TRUE,
    scope_source        TEXT,               -- 'source' | 'real' | 'fabricated'
    comparative         JSONB,
    first_seen          TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen           TIMESTAMPTZ NOT NULL DEFAULT now(),
    -- halfvec (fp16), NOT vector (fp32). This is a hard capacity constraint,
    -- measured not guessed: at the projected ~186.5k facts, fp32 vectors plus
    -- their HNSW index come to ~706 MB, which EXCEEDS Supabase's 500 MB free
    -- tier. halfvec halves both to ~419 MB total, which fits. MiniLM
    -- embeddings are L2-normalized with values well inside fp16 range, so the
    -- recall cost is negligible; running out of disk is not.
    embedding           halfvec(384)
);

CREATE INDEX IF NOT EXISTS facts_published_idx ON facts (published DESC);
CREATE INDEX IF NOT EXISTS facts_scope_idx     ON facts (scope);
CREATE INDEX IF NOT EXISTS facts_source_idx    ON facts (source);
-- Trigram-free simple text search for the browse page's substring filter.
CREATE INDEX IF NOT EXISTS facts_text_idx      ON facts USING gin (to_tsvector('english', fact_text));

-- Cosine-distance ANN index. Embeddings are L2-normalized, so cosine and inner
-- product rank identically; cosine is used to match the existing numpy code.
-- Build this AFTER bulk loading - creating it up front makes the initial import
-- dramatically slower.
CREATE INDEX IF NOT EXISTS facts_embedding_idx ON facts
    USING hnsw (embedding halfvec_cosine_ops);

-- ---------------------------------------------------------------------------
-- ingestion_runs: replaces ingestion_state.json. The scheduled GitHub Actions
-- job writes one row per run, and server.py reports ingestion health by reading
-- the newest row - so health comes from the DB rather than from a process that
-- no longer exists.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ingestion_runs (
    id              BIGSERIAL PRIMARY KEY,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at     TIMESTAMPTZ,
    ok              BOOLEAN,
    source          TEXT,
    error           TEXT,
    stats           JSONB NOT NULL DEFAULT '{}'::jsonb,
    -- Per-source watermark, replacing ingestion_state.json's last_published.
    last_published  TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS ingestion_runs_started_idx ON ingestion_runs (started_at DESC);

-- ---------------------------------------------------------------------------
-- ingestion_exclusions: replaces ingestion_excluded.jsonl. Rejected items are
-- recorded, never silently dropped.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ingestion_exclusions (
    id              BIGSERIAL PRIMARY KEY,
    reason          TEXT NOT NULL,          -- 'relevance_gate' | 'noncontent' | 'ungrounded' | 'unmatched_directional'
    fact_text       TEXT,
    source_title    TEXT,
    published       TIMESTAMPTZ,
    details         JSONB NOT NULL DEFAULT '{}'::jsonb,
    logged_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ingestion_exclusions_reason_idx ON ingestion_exclusions (reason, logged_at DESC);
