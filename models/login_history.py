"""
Login History Model Definition
Audits user login activity, client IP addresses, browser specs, and login timestamps.
"""

from datetime import datetime
from models import db

class LoginHistory(db.Model):
    __tablename__ = 'login_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    attempted_username = db.Column(db.String(50), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime, nullable=True)
    ip_address = db.Column(db.String(45), nullable=False)
    browser = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # SUCCESS, FAILED, LOCKED
    failure_reason = db.Column(db.String(100), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'attempted_username': self.attempted_username,
            'login_time': self.login_time.strftime('%Y-%m-%d %H:%M:%S') if self.login_time else None,
            'logout_time': self.logout_time.strftime('%Y-%m-%d %H:%M:%S') if self.logout_time else 'Active Session',
            'ip_address': self.ip_address,
            'browser': self.browser,
            'status': self.status,
            'failure_reason': self.failure_reason or 'N/A'
        }
