# coding=utf-8
from flask_cors import CORS
from flask import Flask, jsonify, request,redirect,render_template, session, url_for
from .models import Session, engine, Base
from .models import User
from .auth import AuthError, requires_auth

#import entities.entity
#import entities.exam
#import 
#from .models import Exam


#Imports for connecting backend to auth0
from six.moves.urllib.request import urlopen
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from flask_sqlalchemy import SQLAlchemy

# creating the Flask application
app = Flask(__name__)
app.config.from_object("src.config.Config")

CORS(app)

oauth = OAuth(app)



session = Session()

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

@app.route('/register', methods=['POST'])
def register():
    json_data = request.json
      # mount User object
    user = User(
        id = json_data['id'],
        username=json_data['username'],
        password=json_data['password'],
        email=json_data['email'],
        first_name=json_data['first_name'],
        last_name=json_data['last_name']        
    )
    try:
        # persist user
        session.add(user)
        session.commit()
        status = 'success'
    except:
        status = 'this user is already registered'
     # return created user

    session.close()
    return jsonify({'result': status})

   

# Routes for login, callback 
@app.route('/login')
def login():
    json_data = request.json
    user = User.query.filter_by(email=json_data['email']).first()
    if user(
            user.password, json_data['password']):
        session['logged_in'] = True
        status = True
    else:
        status = False
    return auth0.authorize_redirect(redirect_uri='http://localhost:4200')

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    session.pop('logged_in', None)
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'kYsfByzSV4rxmTJSX6jmaQumLeJZVjoM'}
    return redirect('https://dev-4-frsuj0.us.auth0.com' + '/v2/logout?' + urlencode(params))

@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

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
    exam_objects = session.query(Exam).all()

    # transforming into JSON-serializable objects
    

    # serializing as JSON
    session.close()
    return jsonify(exam_objects)


@app.route('/exams', methods=['POST'])
@requires_auth
def add_exam():
    json_data = request.json
    # mount exam object
    posted_exam = ExamSchema(only=('title', 'description'))\
        .load(request.get_json())

    exam = Exam(
        title=json_data['title'],
        description=json_data['description']
    )
    try:
        # persist exam
        
        session.add(exam)
        session.commit()
        status = 'success'

    except:
        status = 'failed'
        session.close()
    return jsonify({'result': status})
    
   


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response