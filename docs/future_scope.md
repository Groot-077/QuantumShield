# Future Scope & Industry Roadmap - QuantumShield

## 1. Hybrid Post-Quantum Signature Integration
While CRYSTALS-Kyber handles Key Encapsulation (KEM), future versions of QuantumShield will integrate **CRYSTALS-Dilithium** (FIPS 204) or **Falcon** post-quantum digital signature algorithms to sign user session JWTs and API payloads.

## 2. Hardware Security Module (HSM) & TPM Integration
Private Kyber keys ($sk$) are currently stored encrypted within the persistent database layer. Future enterprise deployments will isolate master lattice keys inside **PKCS#11 compliant Hardware Security Modules (HSMs)** or **Trusted Platform Modules (TPMs)**.

## 3. WebAuthn & FIDO2 Post-Quantum Extension
Integrating WebAuthn biometric passkeys with a post-quantum extension will allow hardware tokens (e.g. YubiKeys) to execute lattice-based key agreement directly on chip.

## 4. Zero-Knowledge Proofs (ZKP) for Anonymity
Implementing Bulletproofs or zk-SNARKs on top of the Quantum Commitment $C_q$ will allow users to prove ownership of valid Argon2id credentials without transmitting public key material.
