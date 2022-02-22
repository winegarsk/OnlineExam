# coding=utf-8
from flask.cli import FlaskGroup
from flask_cors import CORS
from flask import Flask, jsonify, request,redirect,render_template, session, url_for
from sqlalchemy import null, select
from .models import Answer, Exam, Session, engine, Base
from .models import User,Question
from .auth import AuthError, requires_auth
from urllib.request import Request, urlopen
import json

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
server = Flask(__name__)
server.config.from_object("src.config.Config")

CORS(server)
cli = FlaskGroup(server)

oauth = OAuth(server)



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
@server.route("/questions")
def get_questions():
    req = Request('https://quizapi.io/api/v1/questions?apiKey=oBj6A4kItQwm8ncj0IXgiIRhxKNGOFNyvec0GZ3H&limit=10', headers={'User-Agent': 'Mozilla/5.0'})

    data = urlopen(req).read()
    dict = json.loads(data)

    correct_answers = []
    for i in dict:
        
        for key in i:
            # print(i.get(key))
            #print(key)
            #print(i[key])
            if key == "question":
                try:
                    session.add(Question( ExamID=None,questionID = i.get('id'), question = i.get('question'), description=i.get('description'),explanation=i.get('explanation'),category=i.get('category'),difficulty=i.get('difficulty')))
                    session.commit()
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()
            if key == "answers":
                for k in i.get(key):
                    choice = i.get(key)
                    try:
                        session.add(Answer( ExamID=None,questionID = i.get('id'), correct= None,answer= choice.get(k)))
                        session.commit()
                    except:
                        session.rollback()
                        raise
                    finally:
                        session.close()
            if key == "correct_answers":
                for j in i.get(key):
                    choice2 = i.get(key)
                    query =session.query(Answer).filter(Answer.questionID == i.get('id') and Answer.correct == None)

                    for user in query:
                        query.update({Answer.correct: choice2.get(j)})
                        break

                    

            
    return jsonify({'result': "success"})

@server.route('/register', methods=['POST'])
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
@server.route('/login')
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

@server.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    session.pop('logged_in', None)
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'kYsfByzSV4rxmTJSX6jmaQumLeJZVjoM'}
    return redirect('https://dev-4-frsuj0.us.auth0.com' + '/v2/logout?' + urlencode(params))

@server.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

@server.route('/callback')
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

@server.route('/exams')
def get_exams():
    # fetching from the database
    exam_objects = session.query(Exam).all()

    # transforming into JSON-serializable objects
    

    # serializing as JSON
    session.close()
    return jsonify(exam_objects)


@server.route('/exams', methods=['POST'])
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
    
   


@server.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response