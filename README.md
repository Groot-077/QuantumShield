# 🛡️ QuantumShield: Post-Quantum Secure Password Authentication Framework

> **B.Tech Cyber Security Project**  
> *Using Memory-Hard Hashing (Argon2id) and Lattice-Based Cryptography (CRYSTALS-Kyber-512)*

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791)](https://www.postgresql.org/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7)](https://render.com/)
[![Status](https://img.shields.io/badge/Status-Live-success)](https://quantumshield-vmut.onrender.com/)

🌐 **Live Application:** https://quantumshield-vmut.onrender.com

---

## 📌 Project Overview

**QuantumShield** is a modern web-based authentication framework engineered to defend user password credentials against classical GPU/ASIC brute-force cracking attacks while also preparing the authentication architecture for future quantum-computing threats.

The system utilizes **Argon2id** for memory-hard password hashing and integrates **CRYSTALS-Kyber-512** for post-quantum cryptographic protection.

QuantumShield generates a cryptographic **Quantum Commitment (`Cq`)** using BLAKE2b-512 to bind cryptographic parameters with the stored password-hashing information.

The application is built using **Python Flask**, **Flask-SQLAlchemy**, and a **PostgreSQL production database**, and is deployed as a cloud web service using **Render**.

---

## 🚀 Key Features

- 🔒 **Argon2id Memory-Hard Hashing:** Uses memory-hard password hashing to increase the cost of GPU/ASIC password-cracking attacks.
- ⚛️ **CRYSTALS-Kyber-512 Lattice Cryptography:** Uses a lattice-based post-quantum cryptographic approach based on Module Learning With Errors (M-LWE).
- 🔑 **Quantum Commitment Engine:** Generates a BLAKE2b-512 commitment such as `Cq = BLAKE2b(pk ∥ Argon2Hash ∥ Salt)`.
- 🔁 **Backward Key Combination Engine:** Combines cryptographic parameters to verify and validate candidate passwords against stored authentication information.
- 🔄 **Backward Secrecy / Key Ratcheting:** Supports periodic cryptographic key updates to reduce the impact of compromised key material.
- 🔄 **Backward Hash Compatibility:** Supports migration of legacy password hashes to the stronger Argon2id-based authentication mechanism where implemented.
- ⬅️ **Backward UI & Slide Controls:** Provides dedicated backward navigation controls and keyboard navigation across supported interfaces.
- 🚫 **Account Lockout Protection:** Protects accounts against repeated failed authentication attempts.
- 📊 **Security Operations Center:** Provides administrator-oriented analytics, audit history, and user management.
- 🛡️ **Defense-in-Depth:** Includes CSRF protection, input validation/sanitization, parameterized database operations, and secure session-cookie configuration.

---

## 🛠️ Technology Stack

### Backend

- **Python 3**
- **Flask 3.0**
- **Flask-SQLAlchemy**
- **Flask-WTF**
- **WTForms**
- **Gunicorn**

### Database

- **PostgreSQL** — Production database
- **SQLAlchemy** — Database ORM
- **PyMySQL** — MySQL connectivity support where applicable

### Cryptography & Security

- **Argon2id**
- **argon2-cffi**
- **CRYSTALS-Kyber-512**
- **BLAKE2b-512**
- **CSRF Protection**
- **Input Validation**
- **Secure Session Configuration**

### Frontend

- **HTML5**
- **CSS3**
- **Bootstrap 5**
- **FontAwesome 6**
- **JavaScript**
- **Chart.js**

### Deployment

- **GitHub**
- **Render**
- **Gunicorn**
- **PostgreSQL**

---

## ☁️ Live Deployment

QuantumShield is deployed as a **Python Web Service on Render**.

### Production Configuration

| Configuration | Value |
|---|---|
| Service | QuantumShield |
| Runtime | Python 3 |
| Branch | `main` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Database | PostgreSQL |
| Deployment Platform | Render |
| Deployment Status | 🟢 Live |

### 🌐 Live Application

👉 **https://quantumshield-vmut.onrender.com**

The GitHub `main` branch is connected to Render, so new commits can automatically trigger a new deployment.

> **Note:** The Render free instance may spin down after inactivity. The first request after inactivity can therefore take longer than normal.

---

## 📂 Project Directory Structure

```text
QuantumShield/
│
├── app.py                 # Application Entry Point & Flask Factory
├── config.py              # Configuration & Security Parameters
├── requirements.txt       # Python Package Dependencies
├── schema.sql             # Database Schema & Seed Data
│
├── crypto/                # Cryptographic Module Package
│   ├── __init__.py
│   ├── argon_hash.py      # Argon2id Memory-Hard Hasher
│   ├── kyber.py           # CRYSTALS-Kyber-512 PQC Engine
│   └── commitment.py      # Quantum Commitment Generator
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
│   ├── auth.py            # Registration, Login & Logout
│   ├── user.py            # User Dashboard & Profile
│   └── admin.py           # Admin Portal & User Management
│
├── utils/                 # Utilities & Security Helpers
│   ├── __init__.py
│   ├── security.py        # Password & Input Security
│   ├── validators.py      # WTForms Validation
│   └── decorators.py      # Login & Admin Guards
│
├── static/                # Static Web Assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── templates/             # Jinja2 HTML Templates
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── quantum_keys.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── user_management.html
│   ├── admin_user_form.html
│   ├── login_history.html
│   ├── pqc_overview.html
│   ├── architecture.html
│   ├── 404.html
│   └── 500.html
│
├── docs/                  # B.Tech Project Documentation
│   ├── project_documentation.md
│   ├── architecture_diagrams.md
│   ├── test_cases.md
│   ├── future_scope.md
│   └── conclusion.md
│
└── README.md              # Project Documentation
```

---

## ⚡ Quickstart Setup Instructions

### 1. Prerequisites

- Python 3.9 or higher
- Git
- PostgreSQL for database-backed development

The deployed production environment uses PostgreSQL.

---

### 2. Clone the Repository

```bash
git clone https://github.com/Groot-077/QuantumShield.git
cd QuantumShield
```

---

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

The project dependencies include Flask, Flask-SQLAlchemy, Flask-WTF, Argon2, PostgreSQL support, Gunicorn, and other required security libraries.

---

### 5. Configure Environment Variables

Create a local `.env` file:

```env
SECRET_KEY=your_secret_key
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_EMAIL=your_admin_email
DEFAULT_ADMIN_PASSWORD=your_admin_password
DATABASE_URL=your_database_url
```

### ⚠️ Security Warning

**Never commit your `.env` file to GitHub.**

Do not publish:

- `SECRET_KEY`
- Database passwords
- Administrator passwords
- API keys
- Private cryptographic keys
- Other sensitive credentials

For production, these values are configured through the deployment platform's secure environment-variable system.

---

### 6. Run the Application

```bash
python app.py
```

The application will start using the configured Flask application.

For local development, the application is typically available at:

```text
http://127.0.0.1:5000
```

---

## 🗄️ Database Configuration

### Production

The deployed QuantumShield application uses:

```text
PostgreSQL
```

The connection is provided through:

```text
DATABASE_URL
```

The database URL is configured through Render's environment variables rather than being hard-coded into the source code.

### Local Development

A PostgreSQL database can be configured through the local `.env` file.

Example format:

```env
DATABASE_URL=postgresql://username:password@host:port/database
```

> Never publish a real database connection string containing credentials.

---

## 🔑 Authentication & Security

### Argon2id Password Hashing

QuantumShield uses **Argon2id** to protect user passwords.

Instead of storing plaintext passwords, the application stores password hashes generated using a memory-hard password hashing algorithm.

Conceptually:

```text
Password
    │
    ▼
 Argon2id
    │
    ▼
Password Hash
    │
    ▼
Database
```

---

### ⚛️ Post-Quantum Cryptography

QuantumShield incorporates **CRYSTALS-Kyber-512** as part of its post-quantum cryptographic architecture.

The system is designed around lattice-based cryptography to address the potential threat posed by future cryptographically relevant quantum computers.

---

### 🔑 Quantum Commitment

The project uses a BLAKE2b-512-based commitment:

```text
Cq = BLAKE2b(pk ∥ Argon2Hash ∥ Salt)
```

where:

- `pk` = public cryptographic key
- `Argon2Hash` = password hash
- `Salt` = password salt
- `Cq` = Quantum Commitment

The commitment provides a cryptographic binding between the relevant authentication parameters.

---

## 🛡️ Security Controls

QuantumShield follows a defense-in-depth approach.

| Security Control | Purpose |
|---|---|
| Argon2id | Password protection |
| CRYSTALS-Kyber | Post-quantum cryptographic protection |
| BLAKE2b-512 | Cryptographic commitment |
| CSRF Protection | Prevent CSRF attacks |
| Input Validation | Reject invalid input |
| Input Sanitization | Reduce injection/XSS risks |
| Parameterized Queries | Reduce SQL injection risks |
| HTTPOnly Cookies | Reduce client-side cookie access |
| Account Lockout | Reduce repeated login attempts |
| Audit Logging | Track authentication events |
| Environment Variables | Protect secrets |

---

## 🚫 Account Lockout

QuantumShield includes account protection against repeated failed authentication attempts.

The system can lock an account after multiple consecutive failed login attempts for a defined period.

This helps reduce:

- Brute-force attacks
- Credential-guessing attempts
- Automated login attacks

---

## 📊 Security Operations Center

The administrator interface provides security-oriented functionality including:

- User management
- Authentication history
- Audit logs
- Security analytics
- User account controls
- Login activity monitoring
- Chart.js-based visualization

---

## 🔄 Deployment Workflow

```text
Developer
    │
    ▼
Modify QuantumShield
    │
    ▼
git add
    │
    ▼
git commit
    │
    ▼
git push origin main
    │
    ▼
GitHub Repository
    │
    ▼
Render Auto Deploy
    │
    ▼
Install requirements.txt
    │
    ▼
Gunicorn
    │
    ▼
PostgreSQL
    │
    ▼
🟢 QuantumShield Live
```

---

## 🔧 Render Deployment Configuration

The current production deployment uses:

```text
Name:
QuantumShield

Language:
Python 3

Branch:
main

Root Directory:
/

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app

Database:
PostgreSQL
```

Environment variables required by the deployed application include:

```text
SECRET_KEY
DEFAULT_ADMIN_USERNAME
DEFAULT_ADMIN_EMAIL
DEFAULT_ADMIN_PASSWORD
DATABASE_URL
```

> Actual environment-variable values are intentionally not included in this repository.

---

## 🧪 Testing

The application can be tested for:

### Authentication

- User registration
- User login
- User logout
- Invalid login attempts
- Password verification
- Administrator login

### Password Security

- Argon2id password hashing
- Password validation
- Password update
- Password migration where supported

### Database

- User creation
- User retrieval
- Authentication history
- Administrator operations
- PostgreSQL connectivity

### Security

- CSRF protection
- Input validation
- SQL injection resistance
- Session security
- Account lockout
- Audit logging

### Deployment

- Production startup
- Gunicorn execution
- PostgreSQL connection
- Environment-variable configuration
- Render deployment

---

## 📸 Project Screenshots

Recommended screenshots for the repository:

```text
static/images/screenshots/
│
├── home_landing.png
├── registration_flow.png
├── user_dashboard.png
├── quantum_keys.png
├── admin_dashboard.png
├── user_crud.png
└── audit_logs.png
```

### Suggested README sections

- 🏠 Home Landing Page
- 📝 User Registration
- 🔐 Login Interface
- 👤 User Dashboard
- ⚛️ Quantum Key Explorer
- 📊 Admin Dashboard
- 👥 User Management
- 📜 Security Audit Logs

---

## 📄 Deliverables Summary

1. Complete Flask source code
2. Cryptographic modules
3. Database models
4. Database schema
5. `requirements.txt`
6. Project documentation
7. Architecture diagrams
8. Security test cases
9. Future-scope documentation
10. Cloud deployment using Render
11. PostgreSQL production database
12. GitHub source repository

---

## 🌐 Project Links

### Live Application

👉 https://quantumshield-vmut.onrender.com

### GitHub Repository

👉 https://github.com/Groot-077/QuantumShield

---

## 👥 Team

| Name | Register Number |
|---|---|
| **Jaipal Prakash** | 23BCE0310 |
| **Nikhil Kumar** | 23BCE0404 |
| **Ujjawal Kumar** | 23BCE0354 |

---

## 🎓 Project Information

**Project:** QuantumShield  
**Category:** B.Tech Cyber Security Project  
**Domain:** Cybersecurity & Post-Quantum Cryptography  
**Backend:** Python Flask  
**Password Hashing:** Argon2id  
**Post-Quantum Cryptography:** CRYSTALS-Kyber-512  
**Cryptographic Hash:** BLAKE2b-512  
**Database:** PostgreSQL  
**Deployment:** Render  
**Source Control:** GitHub

---

## 🚀 Project Status

**🟢 LIVE — Successfully Deployed**

QuantumShield is currently deployed as a Render Web Service and connected to a PostgreSQL production database.

**Live URL:**  
https://quantumshield-vmut.onrender.com

---

## 📜 License

This project is developed for **academic and educational purposes** as part of a B.Tech Cyber Security project.

---

*Built with ❤️ for a B.Tech Cyber Security Project.*
