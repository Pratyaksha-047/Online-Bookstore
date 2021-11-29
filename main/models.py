from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from main import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean , default= False)
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"
    

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='/img/book3.jpeg')
    publishing_year = db.Column(db.Integer)
    author = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(10))
    nocopies= db.Column(db.Integer)
    description = db.Column(db.String(5000))

    def __repr__(self):
        return f"Book('{self.title}','{self.author}','{self.image_file}')"
    
