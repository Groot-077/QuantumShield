"""
Admin Blueprint - Control Panel, User CRUD Management, and Audit History Logs
Provides administrator views for security analytics, lock/unlock operations, user CRUD, and system logs.
"""

from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, jsonify
from models import db
from models.user import User
from models.admin import Admin
from models.login_history import LoginHistory
from crypto.argon_hash import argon2_hasher
from crypto.kyber import kyber_engine
from crypto.commitment import quantum_commitment_engine
from utils.decorators import admin_required
from utils.validators import AdminLoginForm, RegistrationForm
from utils.security import SecurityUtils

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin Portal Login Route"""
    if session.get('is_admin'):
        return redirect(url_for('admin.dashboard'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        username = SecurityUtils.sanitize_input(form.username.data)
        password = form.password.data

        admin_acc = Admin.query.filter((Admin.username == username) | (Admin.email == username)).first()

        if admin_acc and argon2_hasher.verify_password(password, admin_acc.password_hash):
            session.clear()
            session['admin_id'] = admin_acc.id
            session['admin_username'] = admin_acc.username
            session['is_admin'] = True
            session.permanent = True
            
            flash("Admin authentication successful! Security Control Center loaded.", "success")
            return redirect(url_for('admin.dashboard'))
        else:
            flash("Invalid admin credentials.", "danger")

    return render_template('admin_login.html', form=form)


@admin_bp.route('/admin/dashboard')
@admin_required
def dashboard():
    """Admin Dashboard with Real-Time Cyber Metrics and Login Analytics"""
    total_users = User.query.count()
    total_logins = LoginHistory.query.count()
    failed_logins = LoginHistory.query.filter_by(status='FAILED').count()
    locked_accounts = User.query.filter(User.locked_until > datetime.utcnow()).count()
    
    recent_logs = LoginHistory.query.order_by(LoginHistory.login_time.desc()).limit(8).all()

    # Chart Data Preparation (Last 7 days attempt distribution)
    days_labels = []
    success_counts = []
    failed_counts = []
    
    for i in range(6, -1, -1):
        target_date = datetime.utcnow().date() - timedelta(days=i)
        days_labels.append(target_date.strftime('%b %d'))
        
        s_cnt = LoginHistory.query.filter(
            db.func.date(LoginHistory.login_time) == target_date,
            LoginHistory.status == 'SUCCESS'
        ).count()
        
        f_cnt = LoginHistory.query.filter(
            db.func.date(LoginHistory.login_time) == target_date,
            LoginHistory.status == 'FAILED'
        ).count()
        
        success_counts.append(s_cnt)
        failed_counts.append(f_cnt)

    return render_template(
        'admin_dashboard.html',
        total_users=total_users,
        total_logins=total_logins,
        failed_logins=failed_logins,
        locked_accounts=locked_accounts,
        recent_logs=recent_logs,
        days_labels=days_labels,
        success_counts=success_counts,
        failed_counts=failed_counts
    )


@admin_bp.route('/admin/users')
@admin_required
def user_management():
    """User Management Page - Lists all registered users with administrative action controls"""
    search_query = request.args.get('search', '').strip()
    if search_query:
        users = User.query.filter(
            (User.username.like(f"%{search_query}%")) | (User.email.like(f"%{search_query}%"))
        ).order_by(User.created_at.desc()).all()
    else:
        users = User.query.order_by(User.created_at.desc()).all()

    return render_template('user_management.html', users=users, search_query=search_query)


@admin_bp.route('/admin/users/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    """Admin CRUD: Create New User with full Kyber & Argon2id protection"""
    form = RegistrationForm()
    if form.validate_on_submit():
        username = SecurityUtils.sanitize_input(form.username.data)
        email = SecurityUtils.sanitize_input(form.email.data).lower()
        password = form.password.data

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return render_template('admin_user_form.html', form=form, title="Add New User")

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return render_template('admin_user_form.html', form=form, title="Add New User")

        salt = argon2_hasher.generate_salt()
        pwd_hash = argon2_hasher.hash_password(password)
        kyber_pk, kyber_sk = kyber_engine.generate_keypair()
        q_commitment = quantum_commitment_engine.generate_commitment(kyber_pk, pwd_hash, salt)

        new_user = User(
            username=username,
            email=email,
            password_hash=pwd_hash,
            salt=salt,
            kyber_public_key=kyber_pk,
            kyber_private_key=kyber_sk,
            quantum_commitment=q_commitment
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash(f"User '{username}' created successfully.", "success")
        return redirect(url_for('admin.user_management'))

    return render_template('admin_user_form.html', form=form, title="Add New User")


@admin_bp.route('/admin/users/<int:user_id>/toggle-lock', methods=['POST'])
@admin_required
def toggle_lock(user_id):
    """Admin Control: Lock or Unlock user account manually"""
    user = User.query.get_or_404(user_id)
    if user.is_locked():
        user.reset_failed_attempts()
        flash(f"Account '{user.username}' unlocked successfully.", "success")
    else:
        user.failed_attempts = 5
        user.locked_until = datetime.utcnow() + timedelta(hours=24)
        db.session.commit()
        flash(f"Account '{user.username}' locked manually.", "warning")

    return redirect(url_for('admin.user_management'))


@admin_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Admin CRUD: Delete User Account and associated audit logs"""
    user = User.query.get_or_404(user_id)
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f"User account '{username}' deleted permanently.", "success")
    return redirect(url_for('admin.user_management'))


@admin_bp.route('/admin/login-history')
@admin_required
def login_history():
    """Audit Trail Page - Views complete system-wide login attempts"""
    status_filter = request.args.get('status', '').upper()
    
    query = LoginHistory.query.order_by(LoginHistory.login_time.desc())
    if status_filter in ['SUCCESS', 'FAILED', 'LOCKED']:
        query = query.filter_by(status=status_filter)
        
    logs = query.limit(200).all()
    return render_template('login_history.html', logs=logs, current_filter=status_filter)


@admin_bp.route('/admin/logout')
def admin_logout():
    """Admin Logout Route"""
    session.clear()
    flash("Admin session terminated.", "info")
    return redirect(url_for('admin.admin_login'))
