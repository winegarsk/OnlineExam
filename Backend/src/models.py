
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy



#Database variables
db_url = 'database:5432'
db_name = 'onlineexam-database-1'
db_user = 'postgres'
db_password = 'postgres'

#Connect to database through sqlalchemy
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    """User account."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))

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