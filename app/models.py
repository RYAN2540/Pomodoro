from app import db
from datetime import datetime
class Todos(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    category = db.Column(db.String(50), nullable = True)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean(), default=False)
    create_date = db.Column(db.DateTime(), default=datetime.now())

class Timer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    pomodoro_interval = db.Column(db.Integer())
    break_interval = db.Column(db.Integer())

class Feedbacks(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	username = db.Column(db.String(50))
	feedback = db.Column(db.String(100))
