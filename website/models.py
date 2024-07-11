from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(35))
    firstname = db.Column(db.String(35))
    email = db.Column(db.String(25), unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(25))
    cart = db.relationship('Cart')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(80), nullable=False)
