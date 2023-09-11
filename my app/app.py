from flask import request, render_template
from models import db, Birthday
from datetime import datetime
from __init__ import create_app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello/user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        date_of_birth = request.form['date_of_birth']
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        if not username.isalpha():
            return 'Username must contain only letters.', 400
        
        elif date_of_birth >= datetime.now().date():
            return "Date of birth must be before today's date.", 400
           
        existing_user = Birthday.query.filter_by(username=username).first()
        
        if existing_user:
            existing_user.date_of_birth = date_of_birth
            db.session.commit()
        else:
            new_user = Birthday(username=username, date_of_birth=date_of_birth)
            db.session.add(new_user)
            db.session.commit()
        
        return f'User {username} added successfully', 201

@app.route('/hello/user', methods=['GET'])
def get_message():
    if request.method == 'GET':
        username = request.args.get('user') 
        if not username:
            return 'User not found', 404
        
       
        user = Birthday.query.filter_by(username=username).first()
        user_dob = user.date_of_birth
        today = datetime.now().date()
        next_birthday = datetime(today.year, user_dob.month, user_dob.day).date()
        
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, user_dob.month, user_dob.day).date()

        days_until_birthday = (next_birthday - today).days

        if next_birthday == today:
            message1 = f'Hello, {username}! Happy birthday!'
            return render_template('message1.html', message=message1), 200
        else:
            message2 = f'Hello, {username}! Your next birthday is in {days_until_birthday} day(s)'
            return render_template('message2.html', message=message2), 200 

if __name__ == '__main__':
    app.run(debug=True)
