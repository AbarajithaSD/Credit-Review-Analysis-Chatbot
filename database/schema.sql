CREATE DATABASE IF NOT EXISTS credit_review_db;

USE credit_review_db;


-- =========================================================
-- CUSTOMERS TABLE
-- =========================================================

CREATE TABLE IF NOT EXISTS customers (

    id INT AUTO_INCREMENT PRIMARY KEY,

    customer_code VARCHAR(100),

    customer_name VARCHAR(255),

    business_currency VARCHAR(20),

    credit_limit DECIMAL(20,2),

    company_books_credit_limit DECIMAL(20,2),

    customer_credit_rating VARCHAR(50),

    invoice_balance DECIMAL(20,2),

    ncnr_percentage DECIMAL(10,2),

    payment_terms VARCHAR(100),

    total_efx_exposure DECIMAL(20,2),

    ar_balance DECIMAL(20,2),

    past_due_amount DECIMAL(20,2),

    customer_status VARCHAR(100),

    ap_balance DECIMAL(20,2),

    raw_material DECIMAL(20,2),

    raw_material_after_ncnr DECIMAL(20,2),

    wip DECIMAL(20,2),

    finished_goods DECIMAL(20,2),

    open_po_balance DECIMAL(20,2),

    open_po_balance_ncnr DECIMAL(20,2),

    cancellation_fees DECIMAL(20,2),

    invoice_raw_material DECIMAL(20,2),

    inv_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_customer_code (customer_code),

    INDEX idx_customer_name (customer_name),

    INDEX idx_customer_status (customer_status),

    INDEX idx_credit_rating (customer_credit_rating),

    INDEX idx_inv_date (inv_date)
);


-- =========================================================
-- CHAT SESSIONS TABLE
-- =========================================================

CREATE TABLE IF NOT EXISTS chat_sessions (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    session_uuid VARCHAR(100) NOT NULL UNIQUE,

    title VARCHAR(255),

    status ENUM(
        'active',
        'ended'
    ) DEFAULT 'active',

    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    ended_at TIMESTAMP NULL,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_session_uuid (session_uuid),

    INDEX idx_session_status (status)
);


-- =========================================================
-- CHAT MESSAGES TABLE
-- =========================================================

CREATE TABLE IF NOT EXISTS chat_messages (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    session_id BIGINT NOT NULL,

    role ENUM(
        'user',
        'assistant',
        'system'
    ) NOT NULL,

    message LONGTEXT NOT NULL,

    source_type ENUM(
        'database',
        'web',
        'database_web',
        'llm'
    ) DEFAULT 'llm',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id)
        REFERENCES chat_sessions(id)
        ON DELETE CASCADE,

    INDEX idx_session_messages (session_id),

    INDEX idx_created_at (created_at)
);


-- =========================================================
-- CHAT SUMMARIES TABLE
-- =========================================================

CREATE TABLE IF NOT EXISTS chat_summaries (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    session_id BIGINT NOT NULL,

    summary LONGTEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id)
        REFERENCES chat_sessions(id)
        ON DELETE CASCADE,

    INDEX idx_summary_session (session_id)
);


-- =========================================================
-- WEB RESEARCH TABLE
-- =========================================================

CREATE TABLE IF NOT EXISTS web_research (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    session_id BIGINT NOT NULL,

    question TEXT NOT NULL,

    source_title VARCHAR(500),

    source_url TEXT,

    source_content LONGTEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id)
        REFERENCES chat_sessions(id)
        ON DELETE CASCADE
);