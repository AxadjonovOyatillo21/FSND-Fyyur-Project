from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

#----------------------------------------------------------------------------#
# We create db in here
#----------------------------------------------------------------------------#

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=True, cascade='all, delete-orphan')
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Show', backref='artist', lazy=True, cascade='all, delete-orphan')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
  venue_name = db.Column(db.String(120), nullable=False)
  venue_image_link = db.Column(db.String(500), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
  artist_name = db.Column(db.String(120), nullable=False)
  artist_image_link = db.Column(db.String(500), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False, default=datetime.today())
