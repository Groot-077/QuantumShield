# 🛡️ QuantumShield: Post-Quantum Secure Password Authentication Framework

> **B.Tech Cyber Security Project**  
> *Using Memory-Hard Hashing (Argon2id) and Lattice-Based Cryptography (CRYSTALS-Kyber-512)*

---

## 📌 Project Overview
**QuantumShield** is a modern web-based authentication framework engineered to defend user password credentials against both classical GPU/ASIC brute-force cracking attacks and future quantum computer threats running Shor's algorithm.

The system utilizes **Argon2id** for memory-hard password hashing and integrates **CRYSTALS-Kyber-512** (NIST FIPS 203 standardized lattice cryptography) to generate a binding **Quantum Commitment ($C_q$)** for every user.

---

## 🚀 Key Features
- 🔒 **Argon2id Memory-Hard Hashing:** OWASP recommended parameters ($m=64\text{MB}, t=3, p=4$) to defeat GPU cracking.
- ⚛️ **CRYSTALS-Kyber-512 Lattice Cryptography:** Post-quantum public/private key generation based on Module Learning With Errors (M-LWE).
- 🔑 **Quantum Commitment Engine:** BLAKE2b-512 digest $C_q = \text{BLAKE2b}(pk \parallel Argon2Hash \parallel Salt)$.
- 🔁 **Backward Key Combination Engine:** Combines all keys ($pk, sk, S, C_q$) backwards to verify & validate candidate passwords against stored PQC parameters.
- 🔄 **Backward Secrecy (Post-Compromise Security):** Periodic Kyber-512 lattice key ratcheting revokes past compromised material for future sessions.
- 🔄 **Backward Hash Compatibility:** Seamless fallback and automatic migration for legacy password hashes (Werkzeug, PBKDF2, SHA-256) to Argon2id + PQC upon login.
- ⬅️ **Backward UI & Slide Controls:** Dedicated backward navigation buttons and keyboard shortcuts across user dashboards, forms, and presentation deck.
- 🚫 **Account Lockout Protection:** 5 consecutive failed login attempts locks account for 15 minutes.
- 📊 **Security Operations Center (Admin):** Live analytics dashboard with Chart.js, complete audit history, and user CRUD management.
- 🛡️ **Defense-in-Depth:** CSRF protection, XSS input sanitization, parameterized SQL queries, HTTPOnly cookies.

---

## 🛠️ Technology Stack
- **Backend Framework:** Python Flask 3.0
- **Database Layer:** MySQL (with automatic SQLite fallback for dev)
- **ORM:** Flask-SQLAlchemy
- **Forms & Security:** Flask-WTF, WTForms, CSRFProtect
- **Cryptography Engine:** `argon2-cffi`, CRYSTALS-Kyber Engine, BLAKE2b-512
- **Frontend Stack:** HTML5, CSS3, Bootstrap 5, FontAwesome 6, Chart.js

---

## 📂 Project Directory Structure

```
QuantumShield/
│
├── app.py                 # Application Entry Point & Flask Factory
├── config.py              # Configuration & Security Parameters
├── requirements.txt       # Python Package Dependencies
├── schema.sql             # Full MySQL Database Schema & Seed Data
│
├── crypto/                # Cryptographic Module Package
│   ├── __init__.py
│   ├── argon_hash.py      # Argon2id Memory-Hard Hasher
│   ├── kyber.py           # CRYSTALS-Kyber-512 PQC KEM Engine
│   └── commitment.py     # Quantum Commitment Generator (BLAKE2b)
│
├── models/                # SQLAlchemy Database Models
│   ├── __init__.py
│   ├── user.py            # User Model & Lockout Logic
│   ├── login_history.py   # Audit History Model
│   └── admin.py           # Admin Account Model
│
├── routes/                # Modular Flask Blueprints
│   ├── __init__.py
│   ├── main.py            # Public Overview & Technical Routes
│   ├── auth.py            # Registration, Login, Logout Flows
│   ├── user.py            # User Dashboard & Profile Controls
│   └── admin.py           # Admin Portal & CRUD User Management
│
├── utils/                 # Utilities & Security Helpers
│   ├── __init__.py
│   ├── security.py        # Password Policy & Input Sanitization
│   ├── validators.py      # WTForms Validation Classes
│   └── decorators.py      # Login & Admin Route Guards
│
├── static/                # Static Web Assets
│   ├── css/style.css      # Dark Cyber Glassmorphic Theme
│   └── js/main.js         # Live Password Strength Meter & Clipboard JS
│
├── templates/             # Jinja2 HTML5 Templates
│   ├── base.html          # Master Shell & Navbar
│   ├── index.html         # Landing Hero Page
│   ├── register.html      # Registration Form & Strength Meter
│   ├── login.html         # User Authentication Form
│   ├── dashboard.html     # User Dashboard & Audit Table
│   ├── profile.html       # Profile & Password Update
│   ├── quantum_keys.html  # PQC Key Explorer
│   ├── admin_login.html   # Admin Portal Login
│   ├── admin_dashboard.html # Control Center & Chart.js Graph
│   ├── user_management.html # Admin CRUD User Table
│   ├── admin_user_form.html # Admin Add User Form
│   ├── login_history.html # System Audit Log Stream
│   ├── pqc_overview.html  # In-depth PQC Educational Guide
│   ├── architecture.html  # System Design & Flowchart Guide
│   ├── 404.html           # 404 Error Handler
│   └── 500.html           # 500 Error Handler
│
├── docs/                  # B.Tech Project Documentation
│   ├── project_documentation.md # B.Tech Thesis Report
│   ├── architecture_diagrams.md # Mermaid Architecture & Sequence Diagrams
│   ├── test_cases.md      # Security & Functional Test Cases Matrix
│   ├── future_scope.md    # Industry Roadmap
│   └── conclusion.md      # Summary Conclusion
│
└── README.md              # Project Setup & Execution Guide
```

---

## ⚡ Quickstart Setup Instructions

### 1. Prerequisites
- Python 3.9 or higher
- MySQL Server (Optional, SQLite is used automatically out-of-the-box for portable dev)

### 2. Environment Setup & Dependency Installation
Open terminal or command prompt in the `QuantumShield` directory:

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install required dependencies
pip install -r requirements.txt
```

### 3. Database Setup (MySQL Optional)
If you wish to use a local MySQL server:
1. Open MySQL workbench or shell and execute `schema.sql`:
   ```bash
   mysql -u root -p < schema.sql
   ```
2. Update your database URI in `config.py` or set environment variable:
   ```bash
   set DATABASE_URL=mysql+pymysql://root:password@localhost/quantumshield_db
   ```

*Note: If no MySQL server is specified, QuantumShield automatically creates and seeds a local SQLite database (`quantumshield.db`) on first run.*

### 4. Running the Application
Start the Flask development web server:

```bash
python app.py
```

The application will initialize database tables, seed the default administrator account, and run on:  
👉 **`http://127.0.0.1:5000`**

---

## 🔑 Sample Test Credentials

| Account Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` / `ankitarya5092002@gmail.com` | `Ankit@12345` | Admin Control Panel (`/admin/login`) |
| **Sample User** | `alice_cyber` | *Registered via form* | User Dashboard (`/login`) |

---

## 📸 Project Screenshots Placeholders

- **Home Landing Page:** `static/images/screenshots/home_landing.png`
- **User Registration with Live Password Meter:** `static/images/screenshots/registration_flow.png`
- **User Dashboard & PQC Keys:** `static/images/screenshots/user_dashboard.png`
- **Admin Control Panel & Chart.js Analytics:** `static/images/screenshots/admin_dashboard.png`
- **User Management CRUD & Lock Controls:** `static/images/screenshots/user_crud.png`
- **Security Audit Log Stream:** `static/images/screenshots/audit_logs.png`

---

## 📄 Deliverables Summary
1. Complete Source Code (Flask Blueprint Architecture)
2. Database SQL File (`schema.sql`)
3. Project Requirements (`requirements.txt`)
4. Documentation Files (`docs/project_documentation.md`, `docs/architecture_diagrams.md`, `docs/test_cases.md`, `docs/future_scope.md`, `docs/conclusion.md`)

---
*Built with ❤️ for B.Tech Cyber Security Project.*
