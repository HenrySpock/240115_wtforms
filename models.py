"""Models for Blogly."""
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, URL

from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, URL

db = SQLAlchemy() 

class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    species = db.Column(db.String(80), nullable=False)
    photo_url = db.Column(db.String(200))
    age = db.Column(db.Integer)
    notes = db.Column(db.String(200))
    available = db.Column(db.Boolean, nullable=False, default=True) 