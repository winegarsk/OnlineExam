
from array import array
from ast import Str
from datetime import datetime
from unicodedata import category
from sqlalchemy import MetaData, create_engine, Column, String, Integer, DateTime, select
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

class Answer(Base):
    'Answer', MetaData, 
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement="auto")
    ExamID= Column(Integer)
    questionID = Column(Integer)
    correct= Column(String)
    answer=Column(String)

    def __init__(self,  ExamID, questionID, correct, answer):
        
        self.ExamID=ExamID
        self.questionID = questionID
        
        self.correct=correct
        self.answer=answer

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement="auto")
    ExamID= Column(Integer)
    questionID = Column(Integer)
    question = Column(String)
    description = Column(String)
    explanation=Column(String)
    category=Column(String)
    difficulty=Column(String)

    def __init__(self,  ExamID, question, questionID, description,explanation,category,difficulty):
        self.ExamID=ExamID
        self.question = question
        self.questionID=questionID
        self.description = description
        self.explanation=explanation
        self.category=category
        self.difficulty=difficulty

class Exam(Base):
    __tablename__ = 'exams'

    id = Column(Integer, primary_key=True, autoincrement="auto")
    title = Column(String)
    description = Column(String)
    category= Column(String)
    score= Column(Integer)

    def __init__(self, title, description,category,score):
    
        self.title = title
        self.description = description
        self.category=category
        self.score=score

class User(Base):
    """User account."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))

    def __init__(self,  username, password,email,first_name,last_name):
        
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