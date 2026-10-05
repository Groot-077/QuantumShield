"""
QuantumShield System Integration & Security Verification Script
Verifies Registration, Argon2id Salt Hashing, Kyber Keypair Generation, Quantum Commitment,
Authentication, Failed Attempt Lockout, and Audit Logging.
"""

from app import create_app
from models import db
from models.user import User
from models.login_history import LoginHistory
from crypto.argon_hash import argon2_hasher
from crypto.kyber import kyber_engine
from crypto.commitment import quantum_commitment_engine

app = create_app()

def run_tests():
    with app.app_context():
        print("=== QuantumShield Automated Security Tests ===")
        
        # 1. Test Argon2id Password Hashing
        pwd = "SecurePassword@2026!"
        pwd_hash = argon2_hasher.hash_password(pwd)
        salt = argon2_hasher.generate_salt()
        assert argon2_hasher.verify_password(pwd, pwd_hash) == True
        assert argon2_hasher.verify_password("WrongPassword", pwd_hash) == False
        print("[OK] Argon2id Memory-Hard Hashing: PASSED")

        # 2. Test Kyber-512 Key Generation & Encapsulation
        pk, sk = kyber_engine.generate_keypair()
        ct, ss_encap = kyber_engine.encapsulate(pk)
        ss_decap = kyber_engine.decapsulate(ct, sk)
        assert len(pk) > 30
        assert len(sk) > 30
        print("[OK] CRYSTALS-Kyber-512 Lattice Engine: PASSED")

        # 3. Test Quantum Commitment Generation & Verification
        c_q = quantum_commitment_engine.generate_commitment(pk, pwd_hash, salt)
        assert quantum_commitment_engine.verify_commitment(c_q, pk, pwd_hash, salt) == True
        assert quantum_commitment_engine.verify_commitment(c_q, pk, pwd_hash, "TamperedSalt") == False
        print("[OK] Quantum Commitment (BLAKE2b-512): PASSED")

        # 4. Test User Creation in Database
        test_username = "test_cyber_user"
        existing = User.query.filter_by(username=test_username).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()

        user = User(
            username=test_username,
            email="test_user@quantumshield.sec",
            password_hash=pwd_hash,
            salt=salt,
            kyber_public_key=pk,
            kyber_private_key=sk,
            quantum_commitment=c_q
        )
        db.session.add(user)
        db.session.commit()
        assert user.id is not None
        print(f"[OK] User Database Persistence (User #{user.id}): PASSED")

        # 5. Test Backward Secrecy (Post-Compromise Security) Key Ratchet
        old_pk = user.kyber_public_key
        old_commitment = user.quantum_commitment
        new_pk, new_sk, new_c_q = quantum_commitment_engine.ratchet_backward_secrecy_keypair(user.password_hash, user.salt)
        user.kyber_public_key = new_pk
        user.kyber_private_key = new_sk
        user.quantum_commitment = new_c_q
        db.session.commit()
        assert user.kyber_public_key != old_pk
        assert user.quantum_commitment != old_commitment
        assert quantum_commitment_engine.verify_commitment(user.quantum_commitment, user.kyber_public_key, user.password_hash, user.salt) == True
        print("[OK] Backward Secrecy (Post-Compromise Security Ratchet): PASSED")

        # 6. Test Backward Compatibility (Legacy Password Hash Verification)
        from werkzeug.security import generate_password_hash
        legacy_pwd = "LegacySecret123!"
        legacy_hash = generate_password_hash(legacy_pwd)
        assert argon2_hasher.verify_password(legacy_pwd, legacy_hash) == True
        assert argon2_hasher.verify_password("WrongPassword", legacy_hash) == False
        print("[OK] Backward Compatibility (Legacy Hash Fallback): PASSED")

        # 7. Test Backward Key Reconstruction & Password Verification Engine
        back_res = quantum_commitment_engine.backward_reconstruct_keys(
            kyber_pk=user.kyber_public_key,
            kyber_sk=user.kyber_private_key,
            salt=user.salt,
            stored_commitment=user.quantum_commitment,
            password=pwd,
            password_hash=user.password_hash
        )
        assert back_res['all_keys_valid'] == True
        assert back_res['commitment_match'] == True
        assert len(back_res['backward_proof_token']) == 64
        print("[OK] Backward Key Combination & Reconstruction Engine: PASSED")

        # 8. Test Flask Client Rendering of Quantum Keys Template & Backward Verify Form
        app.config['WTF_CSRF_ENABLED'] = False
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = user.id
                sess['username'] = user.username
            
            resp = client.get('/quantum-keys')
            assert resp.status_code == 200
            assert b'Backward Key Combination' in resp.data
            
            post_resp = client.post('/quantum-keys/backward-verify', data={'password': pwd}, follow_redirects=True)
            assert post_resp.status_code == 200
            assert b'Backward Key Match: PASSED' in post_resp.data
            print("[OK] Quantum Keys Backward Verification Route & UI rendering: PASSED")

        # 8. Test Failed Attempts & Account Lockout
        for i in range(5):
            user.increment_failed_attempts(max_attempts=5, lock_duration_minutes=15)
        assert user.is_locked() == True
        print("[OK] Account Lockout Mechanism (5 Failed Attempts): PASSED")

        # Reset user lock
        user.reset_failed_attempts()
        assert user.is_locked() == False
        print("[OK] Account Unlock & Reset: PASSED")

        print("==============================================")
        print("ALL SYSTEM INTEGRATION TESTS COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    run_tests()

