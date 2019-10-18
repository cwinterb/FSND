#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from forms import *

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

db = SQLAlchemy()
default_venue_img = 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80'


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=True,
                           default=default_venue_img)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_talent_description = db.Column(db.String(500), nullable=True)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=True)
    shows = db.relationship("Show", backref='venue')


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    website_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(500), nullable=False)
    seeking_venues = db.Column(db.Boolean, nullable=True, default=False)
    seeking_venues_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship("Show", backref='artist')


class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
