"""
Authentication & Authorization Decorators
Restricts route access based on active user sessions and administrator privileges.
"""

from functools import wraps
from flask import session, flash, redirect, url_for, request

def login_required(f):
    """Ensures user is authenticated before allowing access to protected user routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash("Unauthorized access. Please log in to access your dashboard.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Ensures active session belongs to an authenticated administrator."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_id') or not session.get('is_admin'):
            flash("Access Restricted. Administrator credentials required.", "danger")
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function
