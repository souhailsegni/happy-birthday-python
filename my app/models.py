from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Birthday(db.Model):
    __tablename__ = 'birthday'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
