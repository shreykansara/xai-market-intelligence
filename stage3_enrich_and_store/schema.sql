-- 0. Raw GDELT Zip Exports Table (Level 1 Stage 1 Ingestion)
CREATE TABLE IF NOT EXISTS raw_gdelt_exports (
    id VARCHAR(255) PRIMARY KEY,
    export_date DATE NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_size_bytes BIGINT NOT NULL DEFAULT 0,
    raw_articles_count INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(50) DEFAULT 'INGESTED',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_gdelt_export_date ON raw_gdelt_exports (export_date DESC);


-- 0b. Raw GDELT News Events Table (Zero Local File Storage - Direct In-Memory Stream Ingestion)
CREATE TABLE IF NOT EXISTS raw_gdelt_news (
    id VARCHAR(255) PRIMARY KEY,
    global_event_id VARCHAR(100) NOT NULL,
    published_date DATE NOT NULL,
    actor1_name VARCHAR(255),
    actor2_name VARCHAR(255),
    event_code VARCHAR(50),
    action_geo_country VARCHAR(100),
    source_url TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'RAW',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_raw_news_date ON raw_gdelt_news (published_date DESC);
CREATE INDEX IF NOT EXISTS idx_raw_news_url ON raw_gdelt_news (source_url);


-- 0c. Stage 2 Filtered News Intermediate Table (Staging area before 11-D Projection)
CREATE TABLE IF NOT EXISTS stage2_filtered_news (
    id VARCHAR(255) PRIMARY KEY,
    published_date DATE NOT NULL,
    headline TEXT NOT NULL,
    source_link TEXT NOT NULL,
    location_affected VARCHAR(50) NOT NULL DEFAULT 'World',
    category VARCHAR(100) DEFAULT 'General Market',
    status VARCHAR(50) DEFAULT 'FILTERED',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_stage2_news_date ON stage2_filtered_news (published_date DESC);
CREATE INDEX IF NOT EXISTS idx_stage2_news_headline ON stage2_filtered_news (headline);
CREATE INDEX IF NOT EXISTS idx_stage2_news_link ON stage2_filtered_news (source_link);


-- 1. Benchmark Companies Table (CVP Matching & 11-D Market Positioning)
CREATE TABLE IF NOT EXISTS benchmark_companies (
    id VARCHAR(255) PRIMARY KEY,
    company VARCHAR(255) NOT NULL,
    sector VARCHAR(255) NOT NULL,
    target_customer TEXT,
    statement_of_need TEXT,
    product_name VARCHAR(255),
    product_category VARCHAR(255),
    statement_of_key_benefit TEXT,
    cvp TEXT NOT NULL,
    pestle_json JSONB,
    porters_json JSONB,
    strategic_embedding_11d vector(11) NOT NULL,
    cvp_embedding_384d vector(384) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- HNSW Vector Index for 11-D Strategic Positioning Search
CREATE INDEX IF NOT EXISTS idx_companies_11d_hnsw 
ON benchmark_companies USING hnsw (strategic_embedding_11d vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- HNSW Vector Index for 384-D CVP Semantic Vector Search
CREATE INDEX IF NOT EXISTS idx_companies_384d_hnsw 
ON benchmark_companies USING hnsw (cvp_embedding_384d vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS idx_companies_sector ON benchmark_companies (sector);


-- 2. News Articles Table (Strategic Market Events & PESTLE/Porter Analysis)
CREATE TABLE IF NOT EXISTS news_articles (
    id VARCHAR(255) PRIMARY KEY,
    published_date DATE NOT NULL,
    headline TEXT NOT NULL,
    strategic_embedding_11d vector(11) NOT NULL,
    source_link TEXT,
    location_affected VARCHAR(50) NOT NULL DEFAULT 'World',
    impact_score FLOAT NOT NULL DEFAULT 0.05,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- HNSW Vector Index for 11-D News Strategic Search (<5ms)
CREATE INDEX IF NOT EXISTS idx_news_11d_hnsw 
ON news_articles USING hnsw (strategic_embedding_11d vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS idx_news_date ON news_articles (published_date DESC);
CREATE INDEX IF NOT EXISTS idx_news_location ON news_articles (location_affected);
CREATE INDEX IF NOT EXISTS idx_news_impact ON news_articles (impact_score DESC);
