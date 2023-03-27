#!/usr/bin/env python3
"""
Concerned with all the forms in the application
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo, Email

class SignUpForm(FlaskForm):
    """
    Form responsible for signing up a user
    """
    first_name = StringField("First Name", validators=[Length(min=3, max=20), DataRequired()])
    last_name = StringField("Last Name", validators=[Length(min=3, max=20), DataRequired()])
    email_address = StringField("Email Address", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo('password'), DataRequired()])
    preferred_username = StringField("Preferred Username", validators=[Length(min=2, max=20), DataRequired()])
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    """
    Form responsible for loggin in the user into the system
    """
    email_address = StringField("Email Address", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[Length(min=8), DataRequired()])
    submit = SubmitField("Log In")