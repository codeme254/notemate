#!/usr/bin/env python3
"""
Concerned with all the routes in the application
"""

from website import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user
from website.forms import LoginForm
from website.forms import SignUpForm
from website.models import User
from website import bcrypt
from website import db

@app.route("/", methods=["GET", "POST"])
def get_started():
    return render_template("get-started.html", title="Notemate - get started")

@app.route("/feed", methods=["GET", "POST"])
def feed():
    return render_template("feed.html", title="Feed | NoteMate")

@app.route("/create-account", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email_address.data
        
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email_address=form.email_address.data, password=password_hash, preferred_username=form.preferred_username.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account was succesfully created", "success")
        return redirect(url_for('login'))
    return render_template("sign-up.html", title="NoteMate - create your account", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Route responsible for loggin in the user
    """
    form = LoginForm()
    if form.validate_on_submit():
        email_passed = form.email_address.data
        password_passed = form.password.data
        user_loggin_in = User.query.filter_by(email_address=email_passed).first()
        if user_loggin_in and bcrypt.check_password_hash(user_loggin_in.password, password_passed):
            login_user(user_loggin_in)
            flash("You have successfully logged into your account", 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('feed'))
        else:
            flash("Login failed. Please check your email address or password", 'danger')
    return render_template('login.html', title="NoteMate - login to your account", form=form)

@app.route('/logout')
def logout():
    """
    Responsible for logging out a user
    """
    flash("You have been logged out of your account", 'flash_guidance')
    logout_user()
    return redirect(url_for('get_started'))