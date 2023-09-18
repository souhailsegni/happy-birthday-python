

from flask import Blueprint, request, jsonify, abort, render_template
from http import HTTPStatus
from datetime import datetime
from models import db, Birthday
from sqlalchemy import func, text

api = Blueprint('api', __name__)

def abort_if_username_is_not_valid(username):
    if not username.isalpha():
        abort(HTTPStatus.BAD_REQUEST, message="Invalid username '{}'. <username> must contain only letters".format(username))

def abort_if_date_of_birth_is_not_valid(date_of_birth_string):
    try:
        date_of_birth = datetime.strptime(date_of_birth_string, '%Y-%m-%d').date()
        current_date = datetime.now().date()
        if date_of_birth >= current_date:
            abort(HTTPStatus.BAD_REQUEST, message="'{}' date must be a date before today ('{}')".format(date_of_birth_string, current_date.strftime("%Y-%m-%d")))
        return date_of_birth
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, message="Incorrect date format for '{}' date, should be YYYY-MM-DD".format(date_of_birth_string))

@api.route('/')
def index():
    return render_template('index.html')

@api.route('/hello/<username>', methods=['POST', 'GET'])
def add_update_message(username):
    if request.method == 'POST':
        username = request.form['username']
        date_of_birth = request.form['date_of_birth']
        
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        today=datetime.now().date()
        
        if not username.isalpha():
          abort(HTTPStatus.BAD_REQUEST, "Invalid username '{}'. <username> must contain only letters".format(username))

        
        elif date_of_birth >= today:
              abort(HTTPStatus.BAD_REQUEST, "'{}' date must be a date before the today date ('{}')".format(date_of_birth, today.strftime("%Y-%m-%d")))
           
        existing_user = Birthday.query.filter_by(username=username).first()
        
        if existing_user:
            existing_user.date_of_birth = date_of_birth
            db.session.commit()
        else:
            new_user = Birthday(username=username, date_of_birth=date_of_birth)
            db.session.add(new_user)
            db.session.commit()
            
        return f'User {username} added successfully',201
        #return '', HTTPStatus.NO_CONTENT
    
    elif request.method == 'GET':
        
        username = request.args.get('username')  
        
        if not username:
            abort(HTTPStatus.BAD_REQUEST, message="Invalid username '{}'. <username> must contain only letters".format(username))
        
        user = Birthday.query.filter_by(username=username).first()

        user_dob = user.date_of_birth
        today = datetime.now().date()
        next_birthday = datetime(today.year, user_dob.month, user_dob.day).date()
        
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, user_dob.month, user_dob.day).date()
            days_until_birthday = (next_birthday - today).days
        else:
            days_until_birthday = (next_birthday - today).days

        if next_birthday == today:
            message1 = f'Hello, {username}! Happy birthday!'
            return render_template('message1.html',message=message1),200
            #return {'message': "Hello, {}! Happy birthday!".format(username)}, HTTPStatus.OK
        else:
            message2 = f'Hello, {username}! Your next birthday is in {days_until_birthday} day(s)'
            return render_template('message2.html', message=message2),200 
            #return {'message': "Hello, {}! Your birthday is in {} day(s)".format(username, days_until_birthday)}, HTTPStatus.OK
          
@api.route('/healthz')
def healthz():
    try:
        db.session.execute(text('SELECT 1'))
        return '', HTTPStatus.OK
    except Exception as e:
        error_message = str(e)
        response_data = {'error_message': error_message}
        return jsonify(response_data), HTTPStatus.INTERNAL_SERVER_ERROR

@api.route('/readiness')
def readiness():
    try:
        db.session.query(func.count(Birthday.id)).scalar()
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
    return '', HTTPStatus.OK

@api.route('/metrics')
def metrics():
    try:
        return jsonify({'users_count': db.session.query(func.count(Birthday.id)).scalar()}), HTTPStatus.OK
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))

def create_api_blueprint():
    return api
