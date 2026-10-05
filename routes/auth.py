"""
Authentication Blueprint - User Registration, Login, and Logout Logic
Executes Argon2id password hashing, Kyber-512 PQC key generation, Quantum Commitment computation,
and Session/Audit logging.
"""

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models import db
from models.user import User
from models.login_history import LoginHistory
from crypto.argon_hash import argon2_hasher
from crypto.kyber import kyber_engine
from crypto.commitment import quantum_commitment_engine
from utils.validators import RegistrationForm, LoginForm
from utils.security import SecurityUtils

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User Registration Route with PQC KeyGen & Argon2id Hashing"""
    if session.get('user_id'):
        return redirect(url_for('user.dashboard'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        username = SecurityUtils.sanitize_input(form.username.data)
        email = SecurityUtils.sanitize_input(form.email.data).lower()
        password = form.password.data

        # Check existing user
        if User.query.filter_by(username=username).first():
            flash("Username is already taken. Please choose another.", "danger")
            return render_template('register.html', form=form)

        if User.query.filter_by(email=email).first():
            flash("Email address is already registered.", "danger")
            return render_template('register.html', form=form)

        try:
            # 1. Generate Salt
            salt = argon2_hasher.generate_salt()

            # 2. Generate Argon2id Memory-Hard Hash
            password_hash = argon2_hasher.hash_password(password)

            # 3. Generate Kyber-512 Lattice Keypair
            kyber_pk, kyber_sk = kyber_engine.generate_keypair()

            # 4. Generate Quantum Commitment
            quantum_commitment = quantum_commitment_engine.generate_commitment(
                kyber_pk=kyber_pk,
                argon2_hash=password_hash,
                salt=salt
            )

            # 5. Persist User Entity to DB
            new_user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                salt=salt,
                kyber_public_key=kyber_pk,
                kyber_private_key=kyber_sk,
                quantum_commitment=quantum_commitment
            )
            db.session.add(new_user)
            db.session.commit()

            flash("Registration Successful! Your account is protected with Argon2id & Kyber-512 PQC.", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error creating account: {str(e)}", "danger")

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User Authentication Route with Account Lockout & Quantum Commitment Verification"""
    if session.get('user_id'):
        return redirect(url_for('user.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        identifier = SecurityUtils.sanitize_input(form.username.data)
        password = form.password.data
        ip_addr = SecurityUtils.get_client_ip()
        browser_info = SecurityUtils.get_user_agent()

        # Find user by username OR email
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower())
        ).first()

        # 1. Handle Non-existent User
        if not user:
            log_attempt(None, identifier, ip_addr, browser_info, 'FAILED', 'Invalid Username or Email')
            flash("Invalid username or password.", "danger")
            return render_template('login.html', form=form)

        # 2. Check Account Lockout Status
        if user.is_locked():
            log_attempt(user.id, user.username, ip_addr, browser_info, 'LOCKED', 'Account Locked due to max failed attempts')
            remaining_mins = int((user.locked_until - datetime.utcnow()).total_seconds() / 60) + 1
            flash(f"Account locked due to multiple failed login attempts. Try again in {remaining_mins} minute(s).", "danger")
            return render_template('login.html', form=form)

        # 3. Verify Password Hash (Argon2id or Legacy Fallback)
        is_password_correct = argon2_hasher.verify_password(password, user.password_hash)

        if not is_password_correct:
            user.increment_failed_attempts(max_attempts=5, lock_duration_minutes=15)
            log_attempt(user.id, user.username, ip_addr, browser_info, 'FAILED', 'Incorrect Password')
            
            if user.is_locked():
                flash("Account has been LOCKED due to 5 consecutive failed login attempts.", "danger")
            else:
                attempts_left = 5 - user.failed_attempts
                flash(f"Invalid password. {attempts_left} attempt(s) remaining before lockout.", "warning")
            return render_template('login.html', form=form)

        # Handle Automatic Backward Compatibility Hash Migration if legacy hash was used
        if not user.password_hash.startswith('$argon2id$'):
            # Legacy hash verified: Automatically upgrade user to Argon2id & Kyber PQC
            new_salt = argon2_hasher.generate_salt()
            new_hash = argon2_hasher.hash_password(password)
            kyber_pk, kyber_sk = kyber_engine.generate_keypair()
            new_commitment = quantum_commitment_engine.generate_commitment(kyber_pk, new_hash, new_salt)
            
            user.salt = new_salt
            user.password_hash = new_hash
            user.kyber_public_key = kyber_pk
            user.kyber_private_key = kyber_sk
            user.quantum_commitment = new_commitment
            db.session.commit()
            flash("Backward Compatibility Active: Account automatically upgraded to Argon2id & CRYSTALS-Kyber-512 PQC!", "info")
        else:
            # 4. Verify Quantum Commitment Hash Integrity for Argon2id users
            is_quantum_valid = quantum_commitment_engine.verify_commitment(
                stored_commitment=user.quantum_commitment,
                kyber_pk=user.kyber_public_key,
                argon2_hash=user.password_hash,
                salt=user.salt
            )

            if not is_quantum_valid:
                log_attempt(user.id, user.username, ip_addr, browser_info, 'FAILED', 'Quantum Commitment Verification Failure')
                flash("SECURITY ALERT: Quantum Commitment verification failed! Contact Administrator.", "danger")
                return render_template('login.html', form=form)

        # 5. Successful Authentication -> Create Session
        user.reset_failed_attempts()
        session.clear()
        session['user_id'] = user.id
        session['username'] = user.username
        session['email'] = user.email
        session.permanent = True  # Enforces 15-min session lifetime

        # Record Login Audit Log
        login_log = log_attempt(user.id, user.username, ip_addr, browser_info, 'SUCCESS', None)
        session['active_login_log_id'] = login_log.id

        flash(f"Welcome back, {user.username}! PQC Session established successfully.", "success")
        return redirect(url_for('user.dashboard'))

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    """Logs out active user session and updates login audit history."""
    log_id = session.get('active_login_log_id')
    if log_id:
        log_entry = LoginHistory.query.get(log_id)
        if log_entry:
            log_entry.logout_time = datetime.utcnow()
            db.session.commit()

    session.clear()
    flash("You have been logged out safely.", "info")
    return redirect(url_for('auth.login'))


def log_attempt(user_id, username, ip_addr, browser, status, failure_reason):
    """Helper to record audit trail in login_history table."""
    try:
        log_entry = LoginHistory(
            user_id=user_id,
            attempted_username=username,
            ip_address=ip_addr,
            browser=browser,
            status=status,
            failure_reason=failure_reason
        )
        db.session.add(log_entry)
        db.session.commit()
        return log_entry
    except Exception as e:
        db.session.rollback()
        return None
