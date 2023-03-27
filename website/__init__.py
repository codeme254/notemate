#!/usr/bin/env python3
"""
Makes the current directory a package
"""

import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.environ.get("SECRETE_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")

bcrypt = Bcrypt(app=app)
db = SQLAlchemy(app=app)
login_manager = LoginManager(app=app)

from website import routes