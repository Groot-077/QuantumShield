"""
WTForms Validators Module
Defines input forms for User Registration, User Login, Admin Login, and Profile Edits with built-in CSRF.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from utils.security import SecurityUtils

def password_policy_check(form, field):
    is_valid, msg = SecurityUtils.validate_password_complexity(field.data)
    if not is_valid:
        raise ValidationError(msg)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=4, max=30, message="Username must be between 4 and 30 characters.")
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email format.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        password_policy_check
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords do not match.")
    ])
    submit = SubmitField('Register Account')

class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[
        DataRequired(message="Please enter your username or email.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Please enter your password.")
    ])
    submit = SubmitField('Secure Login')

class AdminLoginForm(FlaskForm):
    username = StringField('Admin Username', validators=[
        DataRequired(message="Admin username required.")
    ])
    password = PasswordField('Master Password', validators=[
        DataRequired(message="Admin password required.")
    ])
    submit = SubmitField('Authenticate Admin')

class ProfileUpdateForm(FlaskForm):
    email = StringField('Email Address', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email format.")
    ])
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message="Current password required to verify identity.")
    ])
    new_password = PasswordField('New Password (Optional)', validators=[])
    submit = SubmitField('Update Profile')
