# QuantumShield Test Cases & Security Verification Matrix

This document outlines the test cases, expected outcomes, and empirical verification results for QuantumShield.

---

## 1. Functional Test Cases

| Test Case ID | Feature | Test Input | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-FN-01** | User Registration | Valid details: `user1`, `user1@sec.com`, `Secret123!` | Account created, Argon2id salt/hash & Kyber keypair stored in DB. | **PASSED** |
| **TC-FN-02** | Duplicate Registration | Register with existing `user1` username | Validation error: "Username is already taken." | **PASSED** |
| **TC-FN-03** | Weak Password Check | Password: `short` | Validation error: "Password must be at least 8 characters long." | **PASSED** |
| **TC-FN-04** | Valid User Login | Correct username & password | Successfully authenticates, establishes 15-min session, redirects to dashboard. | **PASSED** |
| **TC-FN-05** | Invalid Password Login | Correct username, wrong password | Login rejected, failed attempts incremented, warning displayed. | **PASSED** |
| **TC-FN-06** | Profile Email Update | Update email to `newemail@sec.com` with valid password | Profile updated in DB, success message flashed. | **PASSED** |
| **TC-FN-07** | Admin Authentication | Username `admin` / `ankitarya5092002@gmail.com`, Password `Ankit@12345` | Admin session initialized, control panel loaded. | **PASSED** |

---

## 2. Cybersecurity & PQC Test Cases

| Test Case ID | Security Control | Attack / Test Scenario | Mitigating Control & Behavior | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-SEC-01** | Brute-Force Lockout | 5 consecutive failed login attempts | Account status changes to `LOCKED` for 15 minutes. Subsequent logins blocked. | **PASSED** |
| **TC-SEC-02** | Quantum Commitment Integrity | Mutate `quantum_commitment` string in DB | Login rejected with critical security alert: "Quantum Commitment verification failed!" | **PASSED** |
| **TC-SEC-03** | SQL Injection | Input: `' OR '1'='1` in username field | Input sanitized via SQLAlchemy parameterized ORM queries; treated as literal string. | **PASSED** |
| **TC-SEC-04** | Cross-Site Scripting (XSS) | Input: `<script>alert('XSS')</script>` in input field | Sanitized via `html.escape()`; rendered as plain harmless text. | **PASSED** |
| **TC-SEC-05** | CSRF Protection | Submit POST request without CSRF token | Request rejected with HTTP 400 Bad Request / Flask-WTF CSRF error. | **PASSED** |
| **TC-SEC-06** | Side-Channel Resistance | Constant-time string comparison test | `secrets.compare_digest()` prevents timing attacks on Quantum Commitment verification. | **PASSED** |
