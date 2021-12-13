from enum import unique
from datetime import date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from main import db, login_manager,app
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
    order = db.relationship('Orders',backref='user',lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
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
    price = db.Column(db.Integer, nullable= False)
    order = db.relationship('Orders',backref='books',lazy=True)

    def __repr__(self):
        return f"Book('{self.title}','{self.author}','{self.image_file}','{self.price}')"
    
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    razorpay_orderid = db.Column(db.Integer, primary_key = True)
    book_id = db.Column(db.Integer,db.ForeignKey('book.id'), nullable= False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable= False)
    book_price = db.Column(db.Integer, nullable= False)
    order_date = db.Column(db.DateTime,nullable=False, default=date.today)

    def __repr__(self):
        return f"Book('{self.razorpay_id}','{self.book_id}','{self.user_id}','{self.book_price}','{self.order_date}')"