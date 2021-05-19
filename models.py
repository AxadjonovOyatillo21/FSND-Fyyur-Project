from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

#----------------------------------------------------------------------------#
# We create db in here
#----------------------------------------------------------------------------#

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

venue_genres = db.Table('venue_genres',
    db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('venue_genre.id'), primary_key=True)
)

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.relationship('VenueGenres', secondary=venue_genres, backref=db.backref('venue', lazy="joined"))
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Show', backref='venue', lazy="joined", cascade='all, delete-orphan')
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class VenueGenres(db.Model):
    __tablename__ = 'venue_genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


artist_genres = db.Table('artist_genres',
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('artist_genre.id'), primary_key=True)
)

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.relationship('ArtistGenres', secondary=artist_genres, backref=db.backref('artist', lazy="joined"))
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=False)
    shows = db.relationship('Show', backref='artist', lazy="joined", cascade='all, delete-orphan')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class ArtistGenres(db.Model):
    __tablename__ = 'artist_genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


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
