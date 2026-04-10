from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(20))  # admin / student


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    student = db.Column(db.String(80))