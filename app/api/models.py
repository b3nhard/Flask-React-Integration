from app import db
from app.api.util import hash_pass,verify_pass
from flask import request
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    posts = db.relationship('Posts',backref='user')


    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "email":self.email,
            
        }
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self,name:None,email,password):
        self.name = name
        self.email=email
        self.password = hash_pass(password)
    def __repr__(self):
        return self.name


class Posts(db.Model):
    __tablename__="Posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    author_id = db.Column(db.ForeignKey("Users.id"))
    created_at = db.Column(db.DateTime)

    def __init__(self,title,content,author_id):
        self.title = title
        self.content=content
        self.author_id = author_id
        self.created_at = datetime.now()


    def serialize(self):
        return{
            "id":self.id,
            "title":self.title,
            "content":self.content,
            "author_id":self.author_id,
            "created_at":self.created_at
        }
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    
    def __repr__(self):
        return self.name
