"""
User Model Definition
Stores user credentials, Argon2id salt/hash, Kyber-512 PQC keys, and Quantum Commitment.
"""

from datetime import datetime, timedelta
from models import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    kyber_public_key = db.Column(db.Text, nullable=False)
    kyber_private_key = db.Column(db.Text, nullable=False)
    quantum_commitment = db.Column(db.String(128), nullable=False)
    failed_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to Login History
    login_histories = db.relationship('LoginHistory', backref='user', lazy=True, cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def is_locked(self) -> bool:
        """Checks if account is currently locked out."""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False

    def increment_failed_attempts(self, max_attempts=5, lock_duration_minutes=15):
        """Increments failed login counter and applies lockout if threshold exceeded."""
        self.failed_attempts += 1
        if self.failed_attempts >= max_attempts:
            self.locked_until = datetime.utcnow() + timedelta(minutes=lock_duration_minutes)
        db.session.commit()

    def reset_failed_attempts(self):
        """Resets failed login counter upon successful authentication."""
        self.failed_attempts = 0
        self.locked_until = None
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'kyber_public_key': self.kyber_public_key[:40] + '...',
            'quantum_commitment': self.quantum_commitment[:30] + '...',
            'failed_attempts': self.failed_attempts,
            'is_locked': self.is_locked(),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
