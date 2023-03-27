#!/usr/bin/env python3
"""
Main file
"""

from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, UserMixin, LoginManager, logout_user
from dotenv import load_dotenv
import os

import datetime

from forms import SignUpForm, LoginForm

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.environ.get("SECRETE_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")


db = SQLAlchemy(app=app)
bcrypt = Bcrypt(app=app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    user representation in the database
    """
    __tablename__ = "users"
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email_address = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    preferred_username = db.Column(db.String(), nullable=False)
    date_joined = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def __repr__(self):
        """
        Minimal representation for a User's object
        """
        return "u/{}.{}".format(self.preferred_username, self.email_address)


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
if __name__ == "__main__":
    app.run(debug=True)
