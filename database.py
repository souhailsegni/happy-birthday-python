
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)#the user must be unique and not empty
    date_of_birth = db.Column(db.Date, nullable=False) #dob must be not empty 

    def __init__(self, username, date_of_birth):
        self.username = username
        self.date_of_birth = date_of_birth