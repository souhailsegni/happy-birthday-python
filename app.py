
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import psycopg2
from datetime import datetime,date,timedelta

CREATE_USER_DATA="CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, date_of_birth text);"
INSERT_DATA="INSERT INTO users (username, date_of_birth) VALUES (%s, %s);"
SELECT_DATA="SELECT date_of_birth FROM users WHERE username = %s;"
load_dotenv()
app = Flask(__name__)

url=os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

cursor = connection.cursor()
cursor.execute(CREATE_USER_DATA)
connection.commit()
cursor.close()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/hello/<username>', methods=['POST'])
def save_update_data(username):
    try:
        
        data = request.json()
        
        date_of_birth = datetime.strptime(data['dateOfBirth'], '%Y-%m-%d').date()
        
        if date_of_birth >= datetime.now().date():
               return "Date of birth must be before today's date.", 400
        
        elif True:
            cursor = connection.cursor()
            cursor.execute(INSERT_DATA, (username, date_of_birth))
            connection.commit()
            cursor.close()
            
        message= f"user {username} added successfully"
        return {"message": message}, 201
    except ValueError:
        return 'Invalid date format. Use YYYY-MM-DD.', 400
@app.route('/hello/message', methods=['GET'])
def get_message(username):
        data = request.get_json()
        username=data(['username'])
        cursor = connection.cursor()
        cursor.execute(SELECT_DATA, (username,))
        result = cursor.fetchone()
        cursor.close()
        if not result:
          return 'User not found', 404
        
        user_dob = result[0]
        today = datetime.now().date()

        if (today.month == user_dob.month ) and (today.day == user_dob.day):
           message = f'Hello, {username}! Happy birthday!'
        else:
           days_until_birthday = (datetime(today.year, user_dob.month, user_dob.day).date()  - today).days
           message = f'Hello, {username}! Your birthday is in {days_until_birthday} day(s)'

        return jsonify({'message': message}), 200

if __name__ == '__main__':
    app.run(debug=True)

  