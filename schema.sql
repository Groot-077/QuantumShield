-- ============================================================================
-- QuantumShield Database Schema (MySQL Version)
-- Post-Quantum Secure Password Authentication Framework
-- ============================================================================

CREATE DATABASE IF NOT EXISTS quantumshield_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE quantumshield_db;

-- ----------------------------------------------------------------------------
-- Table: users
-- Stores user accounts, Argon2id salt/hash, Kyber PQC keys, and Quantum Commitment
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS login_history;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS admin;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(128) NOT NULL,
    kyber_public_key TEXT NOT NULL,
    kyber_private_key TEXT NOT NULL,
    quantum_commitment VARCHAR(128) NOT NULL,
    failed_attempts INT DEFAULT 0,
    locked_until DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- Table: login_history
-- Tracks all authentication attempts, IP addresses, browser agents, and status
-- ----------------------------------------------------------------------------
CREATE TABLE login_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    attempted_username VARCHAR(50) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_time DATETIME NULL,
    ip_address VARCHAR(45) NOT NULL,
    browser VARCHAR(255) NOT NULL,
    status ENUM('SUCCESS', 'FAILED', 'LOCKED') NOT NULL,
    failure_reason VARCHAR(100) NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- Table: admin
-- Stores administrator credentials with Argon2id protection
-- ----------------------------------------------------------------------------
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- Initial Sample Test Data
-- Default Admin Account: username='admin', email='ankitarya5092002@gmail.com'
-- Default Admin Password: 'Ankit@12345'
-- ----------------------------------------------------------------------------
INSERT INTO admin (username, email, password_hash) 
VALUES (
    'admin', 
    'ankitarya5092002@gmail.com', 
    '$argon2id$v=19$m=65536,t=3,p=4$UcQdVMxpRfO9tYgJgpr/HQ$jYDws6UAJxgsGjUKtKSZ7OYOVN18+RxpATN92/EXSfM'
);

-- Seed Sample User: username='alice', email='alice@quantumshield.sec'
INSERT INTO users (username, email, password_hash, salt, kyber_public_key, kyber_private_key, quantum_commitment)
VALUES (
    'alice_cyber',
    'alice@quantumshield.sec',
    '$argon2id$v=19$m=65536,t=3,p=4$0N8b2Wv5b0k4r7x1$JkL89mN0pQ1rS2tU3vW4xY5z6a7b8c9d',
    '0N8b2Wv5b0k4r7x1',
    'KYBER512_PUBKEY_SAMPLE_HEX_LATTICE_SEED_A8F9320B1C4D',
    'KYBER512_PRIVKEY_SAMPLE_HEX_LATTICE_SEED_E7B6C5D4E3F2',
    '6f8b1a3c9e2d4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a'
);

-- Seed Initial Audit Logs
INSERT INTO login_history (user_id, attempted_username, ip_address, browser, status, failure_reason)
VALUES 
(1, 'alice_cyber', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0', 'SUCCESS', NULL),
(1, 'alice_cyber', '192.168.1.105', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 'FAILED', 'Invalid Password Attempt'),
(NULL, 'hacker_john', '185.220.101.5', 'Python-urllib/3.10', 'FAILED', 'Non-existent Username');
