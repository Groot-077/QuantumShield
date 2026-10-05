"""
User Blueprint - User Dashboard, Profile Management, and Quantum Key Explorer
Allows authenticated users to view post-quantum key material, security logs, and edit profile credentials.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models import db
from models.user import User
from models.login_history import LoginHistory
from crypto.argon_hash import argon2_hasher
from crypto.commitment import quantum_commitment_engine
from utils.decorators import login_required
from utils.validators import ProfileUpdateForm
from utils.security import SecurityUtils

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    """User Dashboard - Displays User PQC Credentials & Recent Audit Logs"""
    user = User.query.get_or_404(session['user_id'])
    
    # Fetch recent login attempts for this user
    recent_logs = LoginHistory.query.filter_by(user_id=user.id)\
        .order_by(LoginHistory.login_time.desc())\
        .limit(10).all()

    return render_template('dashboard.html', user=user, recent_logs=recent_logs)


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User Profile & Password Update Page"""
    user = User.query.get_or_404(session['user_id'])
    form = ProfileUpdateForm(email=user.email)

    if form.validate_on_submit():
        current_password = form.current_password.data
        new_email = SecurityUtils.sanitize_input(form.email.data).lower()
        new_password = form.new_password.data

        # Verify current password
        if not argon2_hasher.verify_password(current_password, user.password_hash):
            flash("Current password verification failed.", "danger")
            return render_template('profile.html', form=form, user=user)

        # Check email uniqueness if modified
        if new_email != user.email:
            existing = User.query.filter_by(email=new_email).first()
            if existing:
                flash("This email address is already in use.", "danger")
                return render_template('profile.html', form=form, user=user)
            user.email = new_email

        # Handle optional password update
        if new_password:
            is_valid, msg = SecurityUtils.validate_password_complexity(new_password)
            if not is_valid:
                flash(msg, "danger")
                return render_template('profile.html', form=form, user=user)

            # Re-hash password with Argon2id and re-compute Quantum Commitment
            new_salt = argon2_hasher.generate_salt()
            new_hash = argon2_hasher.hash_password(new_password)
            new_commitment = quantum_commitment_engine.generate_commitment(
                kyber_pk=user.kyber_public_key,
                argon2_hash=new_hash,
                salt=new_salt
            )
            
            user.salt = new_salt
            user.password_hash = new_hash
            user.quantum_commitment = new_commitment
            flash("Password updated successfully! Argon2id & Quantum Commitment refreshed.", "success")

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('user.profile'))

    return render_template('profile.html', form=form, user=user)


@user_bp.route('/quantum-keys')
@login_required
def quantum_keys():
    """Detailed view of Kyber-512 Public/Private keypair, Commitment Structure, and Backward Verification"""
    user = User.query.get_or_404(session['user_id'])
    backward_result = session.pop('backward_result', None)
    return render_template('quantum_keys.html', user=user, backward_result=backward_result)


@user_bp.route('/quantum-keys/ratchet', methods=['POST'])
@login_required
def ratchet_keys():
    """
    Triggers a Post-Quantum Key Ratchet to enforce Backward Secrecy (Post-Compromise Security).
    Rotates CRYSTALS-Kyber-512 keypair and updates Quantum Commitment C_q.
    """
    user = User.query.get_or_404(session['user_id'])
    new_pk, new_sk, new_commitment = quantum_commitment_engine.ratchet_backward_secrecy_keypair(
        argon2_hash=user.password_hash,
        salt=user.salt
    )
    user.kyber_public_key = new_pk
    user.kyber_private_key = new_sk
    user.quantum_commitment = new_commitment
    db.session.commit()

    flash("Backward Secrecy Ratchet Complete! Fresh CRYSTALS-Kyber-512 keypair and Quantum Commitment derived.", "success")
    return redirect(url_for('user.quantum_keys'))


@user_bp.route('/quantum-keys/backward-verify', methods=['POST'])
@login_required
def backward_verify():
    """
    Backward Key Combination & Password Verification Route:
    Combines Kyber Public Key, Kyber Private Key, Salt, and Quantum Commitment
    to verify password authenticity backwards through the PQC pipeline.
    """
    user = User.query.get_or_404(session['user_id'])
    candidate_password = request.form.get('password', '')

    if not candidate_password:
        flash("Please enter a candidate password to perform backward verification.", "warning")
        return redirect(url_for('user.quantum_keys'))

    # Execute Backward Reconstruction & Key Combination
    result = quantum_commitment_engine.backward_reconstruct_keys(
        kyber_pk=user.kyber_public_key,
        kyber_sk=user.kyber_private_key,
        salt=user.salt,
        stored_commitment=user.quantum_commitment,
        password=candidate_password,
        password_hash=user.password_hash
    )

    session['backward_result'] = result

    if result['all_keys_valid']:
        flash("BACKWARD VERIFICATION SUCCESSFUL: All keys (Kyber PK, SK, Salt, Quantum Commitment) combined & verified matching password!", "success")
    else:
        flash("BACKWARD VERIFICATION FAILED: Candidate password does not match combined cryptographic keys.", "danger")

    return redirect(url_for('user.quantum_keys'))


