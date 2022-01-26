# coding=utf-8
from flask_cors import CORS
from flask import Flask, jsonify, request

from .entities.entity import Session, engine, Base
from .entities.exam import Exam, ExamSchema
from .auth import AuthError, requires_auth
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

# creating the Flask application
app = Flask(__name__)
CORS(app)

oauth = OAuth(app)

# if needed, generate database schema
Base.metadata.create_all(engine)

auth0 = oauth.register(
    'auth0',
    client_id='OznIr8gSuGNtPCfvFUsqgOXU4gd4PKaD',
    client_secret='o6lZloIf6wzu65SMuw-c6wFrDec2vUKNM-Jr-wf8SqPPgzpHYatFr2440jh6kk2Z',
    api_base_url='https://dev-dm6nugc4.us.auth0.com',
    access_token_url='https://dev-dm6nugc4.us.auth0.com/oauth/token',
    authorize_url='https://dev-dm6nugc4.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

@app.route('/exams')
def get_exams():
    # fetching from the database
    session = Session()
    exam_objects = session.query(Exam).all()

    # transforming into JSON-serializable objects
    schema = ExamSchema(many=True)
    exams = schema.dump(exam_objects)

    # serializing as JSON
    session.close()
    return jsonify(exams)

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:4200')

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

@app.route('/exams', methods=['POST'])
@requires_auth
def add_exam():
    # mount exam object
    posted_exam = ExamSchema(only=('title', 'description'))\
        .load(request.get_json())

    exam = Exam(**posted_exam, created_by="HTTP post request")

    # persist exam
    session = Session()
    session.add(exam)
    session.commit()

    # return created exam
    new_exam = ExamSchema().dump(exam).data
    session.close()
    return jsonify(new_exam), 201

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response