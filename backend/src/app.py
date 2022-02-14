# coding=utf-8
from flask_cors import CORS
from flask import Flask, jsonify, request,redirect,render_template, session, url_for

import entities.entity
import entities.exam
#from .entities.entity import Session, engine, Base
#from .entities.exam import Exam, ExamSchema
import auth
#from .auth import AuthError, requires_auth

#Imports for connecting backend to auth0
from six.moves.urllib.request import urlopen
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

# creating the Flask application
app = Flask(__name__)


CORS(app)


oauth = OAuth(app)
# if needed, generate database schema
entities.entity.Base.metadata.create_all(entities.entity.engine)

auth0 = oauth.register(
    'auth0',
    client_id='kYsfByzSV4rxmTJSX6jmaQumLeJZVjoM',
    client_secret='fDR6hxNSGJApKrxTdZyD2EC4ezV6oV4F5AlM_lm_Pvgb8UijifazIeJ8b3HzBEUL',
    api_base_url='https://dev-4-frsuj0.us.auth0.com',
    access_token_url='https://dev-4-frsuj0.us.auth0.com/oauth/token',
    authorize_url='https://dev-4-frsuj0.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'Manage exams',
    },
)

# Routes for login, callback 
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:5000')

@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')

@app.route('/exams')
def get_exams():
    # fetching from the database
    session = entities.entity.Session()
    exam_objects = session.query(entities.exam.Exam).all()

    # transforming into JSON-serializable objects
    schema = entities.exam.ExamSchema(many=True)
    exams = schema.dump(exam_objects)

    # serializing as JSON
    session.close()
    return jsonify(exams)


@app.route('/exams', methods=['POST'])
@auth.requires_auth
def add_exam():
    # mount exam object
    posted_exam = entities.exam.ExamSchema(only=('title', 'description'))\
        .load(request.get_json())

    exam = entities.exam.Exam(**posted_exam, created_by="HTTP post request")

    # persist exam
    session = entities.entity.Session()
    session.add(exam)
    session.commit()

    # return created exam
    new_exam = entities.exam.ExamSchema().dump(exam).data
    session.close()
    return jsonify(new_exam), 201

@app.errorhandler(auth.AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response