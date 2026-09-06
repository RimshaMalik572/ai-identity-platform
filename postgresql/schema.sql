
-- ================================================================
-- AI IDENTITY PLATFORM — POSTGRESQL SCHEMA
-- ================================================================

CREATE TABLE IF NOT EXISTS identity_verifications (
    id SERIAL PRIMARY KEY,
    verification_id VARCHAR(64) UNIQUE NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    verification_score NUMERIC(5,2),
    decision VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fraud_signals (
    id SERIAL PRIMARY KEY,
    signal_id VARCHAR(64) UNIQUE NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    signal_type VARCHAR(128) NOT NULL,
    severity VARCHAR(32),
    score NUMERIC(5,2),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS trust_scores (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(128) NOT NULL,
    trust_score NUMERIC(5,2) NOT NULL,
    risk_level VARCHAR(32),
    signal_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    alert_id VARCHAR(64) UNIQUE NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    alert_type VARCHAR(128) NOT NULL,
    severity VARCHAR(32),
    status VARCHAR(32),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS platform_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(64) UNIQUE NOT NULL,
    event_type VARCHAR(128) NOT NULL,
    user_id VARCHAR(128),
    source VARCHAR(128),
    payload JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Useful indexes
CREATE INDEX IF NOT EXISTS idx_identity_user
    ON identity_verifications(user_id);

CREATE INDEX IF NOT EXISTS idx_fraud_user
    ON fraud_signals(user_id);

CREATE INDEX IF NOT EXISTS idx_trust_user
    ON trust_scores(user_id);

CREATE INDEX IF NOT EXISTS idx_alert_user
    ON alerts(user_id);

CREATE INDEX IF NOT EXISTS idx_event_user
    ON platform_events(user_id);
