"""
Security Helper Module
Implements password complexity validators, HTML sanitization, client IP detection, and user-agent string formatting.
"""

import re
import html
from flask import request

class SecurityUtils:
    @staticmethod
    def validate_password_complexity(password: str) -> tuple[bool, str]:
        """
        Enforces Strong Password Policy:
        - Minimum 8 characters
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 digit
        - At least 1 special character (!@#$%^&*()_+-=[]{}|;:,.<>?)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter (A-Z)."
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter (a-z)."
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one numerical digit (0-9)."
        if not re.search(r'[\!\@\#\$\%\^\&\*\(\)\_\+\-\=\[\]\{\}\|;\:\,\.\<\>\?]', password):
            return False, "Password must contain at least one special character (e.g. !@#$%^&*)."
            
        return True, "Strong Password"

    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitizes raw string input against XSS vulnerabilities using HTML entity encoding."""
        if not text:
            return ""
        return html.escape(text.strip())

    @staticmethod
    def get_client_ip() -> str:
        """Retrieves real client IP address considering proxy headers like X-Forwarded-For."""
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        return request.remote_addr or '127.0.0.1'

    @staticmethod
    def get_user_agent() -> str:
        """Extracts and formats User-Agent browser / operating system description."""
        agent_str = request.headers.get('User-Agent', 'Unknown Client Browser')
        return agent_str[:250]  # Cap at 250 characters for DB safety
