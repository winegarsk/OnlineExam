
import datetime
from flask_sqlalchemy import SQLAlchemy

#from .app import db

db = SQLAlchemy()


class User(db.Model):
    """User account."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    def __init__(self, id, username, password,email,first_name,last_name):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)