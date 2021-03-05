from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    '''
    db.Model helps connect our class to our database

    Args:
        gives tables in our database proper names
    ''' 
    
    __tablename__ = 'users' 
    
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        '''
        Raises an attribute error when we try to access the password
        '''
        raise AttributeError('You cannot read the password attribute') 

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        '''
        Defines how the user object will be constructed when the class is called
        '''
        return f'{self.username}'

class Todos(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(50))
    category = db.Column(db.String(50), nullable = True)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean(), default=False)
    create_date = db.Column(db.DateTime(), default=datetime.now())

class Timer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50))
    pomodoro_interval = db.Column(db.Integer())
    break_interval = db.Column(db.Integer())

class Feedbacks(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	username = db.Column(db.String(50))
	feedback = db.Column(db.String(100))