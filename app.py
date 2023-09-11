from flask import Flask, request, jsonify, render_template
from datetime import datetime
from database import Database  # Import your Database class

app = Flask(__name__)
db = Database()  # Initialize your Database instance

@app.route('/hello/<username>', methods=['PUT'])
def update_user_info(username):
    if not username.isalpha():
        return 'Username must contain only letters.'
    
    request_data = request.get_json()
    
    try:
        dob = datetime.strptime(request_data['dateOfBirth'], '%Y-%m-%d')
    except ValueError:
        return 'Invalid date format, Use YYYY-MM-DD format.'
    
    if dob >= datetime.now():
        return 'Date of birth must be before today.'
    
    db.update_user_info(username, dob)
    return " ", 204

@app.route('/hello/<username>', methods=['GET'])
def get_birthday_message(username):
    if not username.isalpha():
        return 'Username must contain only letters.'
    
    dob = db.get_user_info(username)
    
    if dob is None:
        return 'Date of birth not found.', 404
    
    days_until_birthday = (dob - datetime.now().date()).days
    
    if days_until_birthday == 0:
        message = f"Hello, {username}! Happy birthday!"
    else:
        message = f"Hello, {username}! Your birthday is in {days_until_birthday} day(s)."

    return jsonify({"message": message}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
