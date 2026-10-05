# QuantumShield - System Architecture & Diagrams

This document presents the visual structural diagrams for the QuantumShield Post-Quantum Authentication Framework.

---

## 1. System Architecture Diagram

```mermaid
graph TD
    User([User Browser]) <-->|HTTPS / CSRF Token| FlaskApp[Flask Web Application]
    
    subgraph Controller & Security Middleware
        FlaskApp --> Router[Flask Blueprints: main, auth, user, admin]
        Router --> Security[SecurityUtils & WTForms Validators]
        Security --> Decorators[Auth Guards: login_required, admin_required]
    end
    
    subgraph Cryptographic Core Module
        Router --> Argon2[Argon2id Memory-Hard Engine]
        Router --> Kyber[CRYSTALS-Kyber-512 PQC Engine]
        Argon2 & Kyber --> Commitment[Quantum Commitment BLAKE2b Engine]
    end
    
    subgraph Database Layer
        Router --> ORM[SQLAlchemy ORM]
        ORM <--> DB[(MySQL / SQLite Database)]
        DB --> T1[Users Table]
        DB --> T2[Login History Table]
        DB --> T3[Admin Table]
    end
```

---

## 2. Database ER Diagram

```mermaid
erDiagram
    USERS {
        int id PK
        string username UK
        string email UK
        string password_hash
        string salt
        text kyber_public_key
        text kyber_private_key
        string quantum_commitment
        int failed_attempts
        datetime locked_until
        timestamp created_at
    }

    LOGIN_HISTORY {
        int id PK
        int user_id FK
        string attempted_username
        timestamp login_time
        datetime logout_time
        string ip_address
        string browser
        enum status
        string failure_reason
    }

    ADMIN {
        int id PK
        string username UK
        string email UK
        string password_hash
        timestamp created_at
    }

    USERS ||--o{ LOGIN_HISTORY : "tracks authentication attempts"
```

---

## 3. Registration Flowchart

```mermaid
flowchart TD
    A[Start Registration] --> B[User Fills Username, Email, Password]
    B --> C{Validate Form & Password Complexity}
    C -- Invalid --> D[Display Validation Error]
    D --> B
    C -- Valid --> E[Generate 16-Byte Random Salt S]
    E --> F[Compute Argon2id Memory-Hard Hash]
    F --> G[Generate Kyber-512 Lattice Keypair pk, sk]
    G --> H[Compute Quantum Commitment C_q]
    H --> I[Store User Record in MySQL Database]
    I --> J[Display Registration Success & Redirect to Login]
```

---

## 4. Authentication Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Browser
    participant FlaskApp as Flask Server
    participant DB as MySQL DB
    participant Crypto as Argon2id & Kyber Engine

    User->>Browser: Submit Login Form (Username, Password)
    Browser->>FlaskApp: POST /login (CSRF Token, Credentials)
    FlaskApp->>DB: Query User by Username/Email
    
    alt User Not Found
        DB-->>FlaskApp: Return Null
        FlaskApp->>DB: Log Failed Attempt (Invalid Username)
        FlaskApp-->>Browser: Flash Error: "Invalid Credentials"
    else User Exists
        DB-->>FlaskApp: Return User Record
        
        alt Account Locked
            FlaskApp-->>Browser: Flash Error: "Account Locked (15 mins)"
        else Account Active
            FlaskApp->>Crypto: Verify Argon2id Password Hash
            
            alt Password Incorrect
                Crypto-->>FlaskApp: Verification Failed
                FlaskApp->>DB: Increment failed_attempts, Apply Lock if >= 5
                FlaskApp->>DB: Log Failed Attempt
                FlaskApp-->>Browser: Flash Warning: "Invalid Password (Attempts left)"
            else Password Correct
                Crypto-->>FlaskApp: Verification Passed
                FlaskApp->>Crypto: Verify Quantum Commitment C_q
                Crypto-->>FlaskApp: Commitment Valid
                FlaskApp->>DB: Reset failed_attempts = 0
                FlaskApp->>DB: Log Successful Login
                FlaskApp->>Browser: Set HTTPOnly Session Cookie & Redirect to /dashboard
            end
        end
    end
```
