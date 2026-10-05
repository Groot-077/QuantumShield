# QuantumShield: A Post-Quantum Secure Password Authentication Framework Using Memory-Hard Hashing and Lattice Cryptography

## B.Tech Cyber Security Project Documentation

---

### Executive Summary
The rapid evolution of quantum computing poses an existential threat to classical cryptographic authentication systems. Quantum algorithms such as **Shor's Algorithm** reduce the time complexity of breaking RSA and Elliptic Curve Cryptography (ECC) from exponential to polynomial time, rendering existing public-key systems vulnerable. Simultaneously, advances in GPU and ASIC parallel hardware accelerate dictionary attacks against classical password hashes (MD5, SHA-256, bcrypt).

**QuantumShield** presents a hybrid post-quantum authentication framework combining **Argon2id memory-hard hashing** with **CRYSTALS-Kyber (FIPS 203)** lattice-based key encapsulation mechanisms. By generating a binding **Quantum Commitment ($C_q$)**, the framework guarantees zero-knowledge password verification resilient against both high-speed offline dictionary attacks and future quantum decryption.

---

## 1. Problem Statement & Motivation
Existing password authentication mechanisms suffer from two major vulnerabilities:
1. **GPU/ASIC Brute-Force Vulnerability:** Standard hash functions like SHA-256 and MD5 allow attackers to execute billions of hashes per second using parallel GPU clusters.
2. **Post-Quantum Cryptanalysis:** Future quantum computers running Shor's algorithm will compromise traditional asymmetric key exchange and public-key infrastructure.

---

## 2. Cryptographic Architecture

### 2.1 Argon2id Memory-Hard Hashing
Argon2id is configured according to OWASP cryptographic guidance:
- **Memory Cost ($m$):** $65,536\text{ KB}$ ($64\text{ MB}$)
- **Time Cost ($t$):** $3$ iterations
- **Parallelism ($p$):** $4$ threads
- **Salt Length:** $16$ bytes cryptographically secure random bytes

### 2.2 CRYSTALS-Kyber Lattice Key Encapsulation (Kyber-512)
CRYSTALS-Kyber relies on the Module Learning With Errors (M-LWE) problem over polynomial ring $\mathbb{R}_q = \mathbb{Z}_q[X]/(X^{256} + 1)$ with modulus $q = 3329$:
- **Public Key ($pk$):** $(A s + e, \text{seed}_A)$
- **Private Key ($sk$):** $s$
- **Security Level:** NIST Level 1 (Equivalent to AES-128 against quantum attack)

### 2.3 Quantum Commitment Derivation
The framework binds the user's password hash and Kyber public key into a single quantum commitment token $C_q$:
$$C_q = \text{BLAKE2b-512} \big( pk \parallel \text{Argon2idHash} \parallel \text{Salt} \big)$$

### 2.4 Backward Key Combination & Security Capabilities
- **Backward Key Combination Engine:** Combines all stored keys ($pk, sk, S, C_q$) backwards to verify candidate password inputs. It performs Kyber encapsulation/decapsulation lattice consistency checks and re-derives $C'_q$ to compute a 32-byte Backward Proof Token.
- **Backward Secrecy (Post-Compromise Security):** Implements periodic key ratcheting. When triggered, the system generates a new CRYSTALS-Kyber-512 keypair $(pk', sk')$ and re-computes $C'_q$. Any past key or commitment compromise provides zero predictive advantage against future authentication sessions.
- **Backward Compatibility & Automatic Migration:** Supports legacy password hash formats (Werkzeug, PBKDF2, SHA-256). Upon authenticating a legacy hash, the system transparently upgrades the record to memory-hard Argon2id, generates a Kyber-512 keypair, and computes a binding Quantum Commitment $C_q$.

---

## 3. System Workflow & Data Pipeline

### 3.1 Registration Workflow
1. User provides `username`, `email`, and `password`.
2. System validates strong password policy (Min 8 chars, uppercase, lowercase, digit, special character).
3. System generates random $16$-byte salt $S$.
4. System computes Argon2id hash $H_{\text{argon}}$.
5. System invokes Kyber Engine to generate lattice keypair $(pk, sk)$.
6. System computes Quantum Commitment $C_q = \text{BLAKE2b}(pk \parallel H_{\text{argon}} \parallel S)$.
7. Record saved to MySQL database with unique indexes on `username` and `email`.

### 3.2 Login Workflow & Account Lockout
1. User provides login credentials.
2. System checks `failed_attempts` counter and active lockout window (`locked_until`).
3. If attempts $\ge 5$, authentication is rejected immediately with remaining lock time.
4. Argon2id password hash verified in constant time.
5. If password invalid, `failed_attempts` incremented, lockout applied if threshold met, failure logged in `login_history`.
6. If password valid, Quantum Commitment re-computed and verified against stored $C_q$.
7. Upon successful verification, failed attempt counter reset, 15-minute HTTPOnly session created, and `login_history` logged.

---

## 4. Software Architecture & Technology Stack
- **Backend:** Python Flask 3.0, Flask-SQLAlchemy, Flask-WTF
- **Database:** MySQL / SQLite fallback
- **Hashing & PQC:** Argon2-cffi, CRYSTALS-Kyber (liboqs / native lattice simulation), BLAKE2b
- **Frontend:** Bootstrap 5, FontAwesome 6, Chart.js analytics, Vanilla JS password strength meter
