CREATE TABLE IF NOT EXISTS audit.logs (
    id BIGSERIAL PRIMARY KEY,

    layer TEXT NOT NULL,
    process_name TEXT NOT NULL,

    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,

    rows_processed BIGINT DEFAULT 0,

    status TEXT NOT NULL,
    message TEXT NOT NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);