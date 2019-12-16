#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from datetime import datetime, time as time_
# from forms import *
from constants import default_project_img

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

database_name = "capstone"
database_path = "postgres://{}/{}".format(
    'carmellasouthward@localhost:5432', database_name)
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()
