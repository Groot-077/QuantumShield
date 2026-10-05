"""
QuantumShield - Configuration Module
Defines configuration settings for Flask, SQLAlchemy Database, Security, and Argon2id Hashing.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base Configuration Class"""
    
    # Secret Key for Session Signing & CSRF Protection
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Database Configuration (MySQL by default, fallback to local SQLite for portable dev)
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'quantumshield_db')
    
    # Default URI (Checks environment variable, otherwise MySQL, fallback to SQLite if needed)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(BASE_DIR, "quantumshield.db")}'
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security Settings
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)  # Session timeout 15 minutes
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    
    # Account Lockout Settings
    MAX_FAILED_LOGIN_ATTEMPTS = 5
    ACCOUNT_LOCKOUT_DURATION_MINUTES = 15
    
    # Argon2id Hashing Parameters (NIST & OWASP Recommended)
    ARGON2_TIME_COST = 3       # Number of iterations
    ARGON2_MEMORY_COST = 65536 # 64 MB memory
    ARGON2_PARALLELISM = 4     # 4 parallel threads
    ARGON2_SALT_LEN = 16       # 16 bytes salt
    ARGON2_HASH_LEN = 32       # 32 bytes hash output
    
    # Post-Quantum Cryptography Parameters (Kyber-512)
    KYBER_VARIANT = "Kyber512" # NIST Security Level 1 (AES-128 equivalent)

class ProductionConfig(Config):
    """Production Environment Configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    """Development Environment Configuration"""
    DEBUG = True

class TestingConfig(Config):
    """Testing Environment Configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
