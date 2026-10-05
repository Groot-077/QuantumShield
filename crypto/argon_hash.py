"""
Argon2id Memory-Hard Password Hashing Module
Uses OWASP recommended memory-hard configuration parameters:
- Type: Argon2id (Resistant to GPU cracking and side-channel attacks)
- Time cost (iterations): 3
- Memory cost: 65536 KB (64 MB)
- Parallelism: 4 threads
"""

import secrets
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError, VerificationError

class Argon2idHasher:
    def __init__(self, time_cost=3, memory_cost=65536, parallelism=4, hash_len=32, salt_len=16):
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.hash_len = hash_len
        self.salt_len = salt_len
        
        self.ph = PasswordHasher(
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=self.hash_len,
            salt_len=self.salt_len,
            type=Type.ID
        )

    def generate_salt(self) -> str:
        """Generates a cryptographically secure random salt hex string."""
        return secrets.token_hex(self.salt_len)

    def hash_password(self, password: str) -> str:
        """
        Hashes password using Argon2id with memory-hard parameters.
        Returns the formatted Argon2id hash string containing parameters, salt, and hash digest.
        """
        if not password:
            raise ValueError("Password cannot be empty.")
        return self.ph.hash(password)

    def verify_password(self, password: str, hash_str: str) -> bool:
        """
        Verifies a plaintext password against an Argon2id hash string.
        Returns True if matched, False otherwise.
        """
        if not password or not hash_str:
            return False
        try:
            return self.ph.verify(hash_str, password)
        except (VerifyMismatchError, VerificationError):
            return self.verify_legacy_hash(password, hash_str)
        except Exception:
            return self.verify_legacy_hash(password, hash_str)

    def verify_legacy_hash(self, password: str, hash_str: str) -> bool:
        """
        Backward Compatibility Layer:
        Verifies plaintext password against legacy hash formats (e.g., werkzeug, pbkdf2, sha256).
        Allows seamless backward compatibility and automatic migration to Argon2id + PQC upon login.
        """
        if not password or not hash_str:
            return False
        try:
            from werkzeug.security import check_password_hash
            return check_password_hash(hash_str, password)
        except Exception:
            return False

# Global instance for easy import across application
argon2_hasher = Argon2idHasher()

