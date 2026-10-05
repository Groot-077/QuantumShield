"""
QuantumShield Application Entry Point
Main Flask application factory, database initialization, blueprint registration, and CLI commands.
"""

import os
from flask import Flask, render_template
from config import Config
from models import db
from models.admin import Admin
from models.user import User
from crypto.argon_hash import argon2_hasher
from routes.main import main_bp
from routes.auth import auth_bp
from routes.user import user_bp
from routes.admin import admin_bp

from flask_wtf.csrf import CSRFProtect, generate_csrf

csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)
    app.jinja_env.globals['csrf_token'] = generate_csrf

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        init_default_admin()

    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    return app


def init_default_admin():
    """Create default admin only if no admin account exists."""

    try:
        admin_username = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')
        admin_email = os.environ.get('DEFAULT_ADMIN_EMAIL')
        admin_password = os.environ.get('DEFAULT_ADMIN_PASSWORD')

        if not admin_email or not admin_password:
            print("INFO: Default admin credentials are not configured.")
            return

        admin_user = Admin.query.filter(
            (Admin.username == admin_username) |
            (Admin.email == admin_email)
        ).first()

        if not admin_user:
            default_admin_hash = argon2_hasher.hash_password(admin_password)

            admin_user = Admin(
                username=admin_username,
                email=admin_email,
                password_hash=default_admin_hash
            )

            db.session.add(admin_user)
            db.session.commit()

            print("INFO: Default admin account created.")

        else:
            print("INFO: Existing admin account found. Password was not changed.")

    except Exception as e:
        db.session.rollback()
        print(f"DEBUG: Default admin check skipped: {e}")


app = create_app()


if __name__ == '__main__':
    print("=" * 70)
    print("  QUANTUMSHIELD: POST-QUANTUM SECURE AUTHENTICATION FRAMEWORK")
    print("  Server running on http://127.0.0.1:5000")
    print("=" * 70)

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )