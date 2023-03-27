#!/usr/bin/env python3
"""
Concerned with all the models in the application
"""

from flask_login import UserMixin
from website import login_manager,db
import datetime

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