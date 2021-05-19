#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import json
import dateutil.parser
import babel
from datetime import datetime
from flask import (
  Flask, 
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_wtf.csrf import CSRFProtect
from forms import *
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
db.app = app
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# ****  You can see models in models.py file ****


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  data = []
  venues = Venue.query.all()
  places = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state)
  for place in places:
    data.append({
      "city": place.city,
      "state": place.state,
      "venues": [{
          'id': venue.id,
          'name': venue.name,
          'num_upcoming_shows': len([show for show in venue.shows if show.start_time > datetime.now()])
      } for venue in venues if venue.city == place.city and venue.state == place.state]
    })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():

  search_term = request.form['search_term']
  search_by = request.form['search_by'].lower()
  if search_by == 'name':
    filtered_venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  elif search_by == 'city':
    filtered_venues = Venue.query.filter(Venue.city.ilike(f'%{search_term}%')).all()
  elif search_by == 'state':
    filtered_venues = Venue.query.filter(Venue.state.ilike(f'%{search_term}%')).all()
  venues = []
  for item in filtered_venues:
    venue = {
      "id": item.id,
      "name": item.name,
      "num_upcoming_shows": len([show for show in item.shows if show.start_time > datetime.now()])
    }
    venues.append(venue)
  response={
    "count": len(filtered_venues),
    "data": venues
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  venue = Venue.query.get(venue_id)
  past_shows = [item for item in venue.shows if item.start_time < datetime.now()]
  upcoming_shows = [item for item in venue.shows if item.start_time > datetime.now()]
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": [genre.name for genre in venue.genres],
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

# @app.route('/venues/create', methods=['GET'])
# def create_venue_form():
#   form = VenueForm()
#   return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue_submission():
  form = VenueForm()
  if form.validate_on_submit():
    try:
      name = form.name.data
      city = form.city.data 
      state = form.state.data 
      address = form.address.data 
      phone = form.phone.data 
      facebook_link = form.facebook_link.data 
      image_link = form.image_link.data 
      website_link = form.website_link.data 
      seeking_talent = form.seeking_talent.data 
      seeking_description = form.seeking_description.data

      venue = Venue(name=name,
                    city=city,
                    state=state,
                    address=address,
                    phone=phone,
                    facebook_link=facebook_link,
                    image_link=image_link,
                    website=website_link,
                    seeking_talent=seeking_talent,
                    seeking_description=seeking_description
      )
      for item in form.genres.data:
        genre = VenueGenres(name=item)
        venue.genres.append(genre)
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!', category='success')
      return redirect(url_for('index'))
    except:
      db.session.rollback()
      flash('Inserting venue ' + request.form['name'] + ' was unsuccessful!', category='danger')
      print(sys.exc_info())

    finally:
      db.session.close()
  else:
    message = []
    for field, error in form.errors.items():
      message.append(field + ' ' + '|'.join(error))
    if message:
      flash('Errors ' + str(message))

  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<venue_id>/delete', methods=['GET', 'DELETE'])
def delete_venue(venue_id):

  try:
    venue = Venue.query.get(venue_id)
    if venue.genres:
      for genre in venue.genres:
        delete_genre = VenueGenres.query.get(genre.id)
        db.session.delete(delete_genre)

    db.session.delete(venue)
    db.session.commit()
    flash(f'Venue {venue.name} was successfully deleted!', category="success")

  except:
    db.session.rollback()
    flash(f'Deleting venue was unsuccessful!', category="danger")

  finally:
    db.session.commit()

  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  data = Artist.query.all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  search_term = request.form['search_term']
  search_by = request.form['search_by'].lower()
  if search_by == 'name':
    filtered_artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  elif search_by == 'city':
    filtered_artists = Artist.query.filter(Artist.city.ilike(f'%{search_term}%')).all()
  elif search_by == 'state':
    filtered_artists = Artist.query.filter(Artist.state.ilike(f'%{search_term}%')).all()
  artists = []
  for item in filtered_artists:
    artist = {
      "id": item.id,
      "name": item.name,
      "num_upcoming_shows": len(item.shows)
    }
    artists.append(artist)
  response={
    "count": len(filtered_artists),
    "data": artists
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  artist = Artist.query.get_or_404(artist_id)
  past_shows = [item for item in artist.shows if item.start_time <= datetime.now()]
  upcoming_shows = [item for item in artist.shows if item.start_time > datetime.now()]
  data = vars(artist)
  data['genres'] = [genre.name for genre in artist.genres]
  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
# @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
# def edit_artist(artist_id):

#   form = ArtistForm()
#   artist = Artist.query.get(artist_id)

#   return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  artist = Artist.query.get_or_404(artist_id)
  if form.validate_on_submit():
    try:
      if artist.shows:
        shows = artist.shows 
        for show in shows:
          show.artist_image_link = form.image_link.data
          show.artist_name = form.name.data 
      artist.name = form.name.data
      artist.city = form.city.data 
      artist.state = form.state.data 
      artist.phone = form.phone.data 
      for genre in artist.genres:
        if genre not in form.genres.data:
          del_genre = ArtistGenres.query.get(genre.id)
          db.session.delete(del_genre)
      for item in form.genres.data:
        if item not in artist.genres:
          genre = ArtistGenres(name=item)
          artist.genres.append(genre)
      artist.facebook_link = form.facebook_link.data 
      artist.image_link = form.image_link.data 
      artist.website = form.website_link.data 
      artist.seeking_venue = form.seeking_venue.data 
      artist.seeking_description = form.seeking_description.data
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully updated!', category='success')
      return redirect(url_for('show_artist', artist_id=artist_id))
    except:
      db.session.rollback()
      flash('Updating artist ' + request.form['name'] + ' was unsuccessful!', category='danger')
    finally:
      db.session.close()
  else:
    message = []
    for field, error in form.errors.items():
      message.append(field + ' ' + '|'.join(error))
    if message:
      flash('Errors ' + str(message))
  return render_template('forms/edit_artist.html', form=form, artist=artist)


# @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
# def edit_venue(venue_id):
#   form = VenueForm()
#   venue = Venue.query.get(venue_id)
#   

@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()
  venue = Venue.query.get_or_404(venue_id)
  if form.validate_on_submit():
    try:
      if venue.shows:
        shows = venue.shows 
        for show in shows:
          show.venue_image_link = form.image_link.data
          show.venue_name = form.name.data 
      venue.name = form.name.data
      venue.city = form.city.data 
      venue.state = form.state.data 
      venue.address = form.address.data 
      venue.phone = form.phone.data 
      for genre in venue.genres:
        if genre not in form.genres.data:
          del_genre = VenueGenres.query.get(genre.id)
          db.session.delete(del_genre)
      for item in form.genres.data:
        if item not in venue.genres:
          genre = VenueGenres(name=item)
          venue.genres.append(genre)
      venue.facebook_link = form.facebook_link.data 
      venue.image_link = form.image_link.data 
      venue.website = form.website_link.data 
      venue.seeking_talent = form.seeking_talent.data 
      venue.seeking_description = form.seeking_description.data
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully updated!', category='success')
      return redirect(url_for('show_venue', venue_id=venue_id))

    except:
      db.session.rollback()
      flash('Updating venue ' + request.form['name'] + ' was unsuccessful!', category='danger')

    finally:
      db.session.close()
  else:
    message = []
    for field, error in form.errors.items():
      message.append(field + ' ' + '|'.join(error))
    if message:
      flash('Errors ' + str(message))
  return render_template('forms/edit_venue.html', form=form, venue=venue)


  

#  Create Artist
#  ----------------------------------------------------------------

# @app.route('/artists/create', methods=['GET'])
# def create_artist_form():

#   form = ArtistForm()

#   return render_template('forms/new_artist.html', form=form)

# TODO: form validation !done
@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist_submission():
  form = ArtistForm()
  if form.validate_on_submit():
    try:
      name = form.name.data
      city = form.city.data 
      state = form.state.data 
      phone = form.phone.data 
      facebook_link = form.facebook_link.data 
      image_link = form.image_link.data 
      website_link = form.website_link.data 
      seeking_venue = form.seeking_venue.data 
      seeking_description = form.seeking_description.data

      artist = Artist(name=name,
                    city=city,
                    state=state,
                    phone=phone,
                    facebook_link=facebook_link,
                    image_link=image_link,
                    website=website_link,
                    seeking_venue=seeking_venue,
                    seeking_description=seeking_description
      )
      for item in form.genres.data:
        genre = ArtistGenres(name=item)
        artist.genres.append(genre)

      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!', category='success')
      return redirect(url_for('index'))
    except: 
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.', category='danger')
    finally:
      db.session.close()
  else:
    message = []
    for field, error in form.errors.items():
      message.append(field + ' ' + '|'.join(error))
    if message:
      flash('Errors ' + str(message))

  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/<artist_id>/delete', methods=['GET', 'DELETE'])
def delete_artist(artist_id):

  try:
    artist = Artist.query.get(artist_id)
    if artist.genres:
      for genre in artist.genres:
        delete_genre = ArtistGenres.query.get(genre.id)
        db.session.delete(delete_genre)
      db.session.delete(artist)
      db.session.commit()
    flash(f'Artist {artist.name} was successfully deleted!', category="success")
  except:
    db.session.rollback()
    flash(f'Deleting artist was unsuccessful!', category="danger")
  finally:
    db.session.commit()

  return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

  data = Show.query.all()

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/search', methods=['POST'])
def search_shows():
  search_term = request.form['search_term']
  search_by = request.form['search_by'].lower()
  if search_by == 'venue_name':
    filtered_shows = Show.query.filter(Show.venue_name.ilike(f'%{search_term}%')).all()
  elif search_by == 'artist_name':
    filtered_shows = Show.query.filter(Show.artist_name.ilike(f'%{search_term}%')).all()

  shows = filtered_shows
  response={
    "count": len(shows),
    "data": filtered_shows
  }

  return render_template('pages/search_shows.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  artists = Artist.query.all()
  venues = Venue.query.all()

  return render_template('forms/new_show.html', form=form, data=[artists, venues])

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  if form.validate_on_submit():
    try:
      form = ShowForm()
      venue = Venue.query.get(form.venue_id.data)
      artist = Artist.query.get(form.artist_id.data)
      artist_id = artist.id
      artist_name = artist.name 
      artist_image_link = artist.image_link
      venue_id = venue.id
      venue_name = venue.name
      print(venue.image_link)
      venue_image_link = venue.image_link
      start_time = form.start_time.data
      show = Show(artist_id=artist_id,
                  artist_name=artist_name,
                  artist_image_link=artist_image_link,
                  venue_id=venue_id,
                  venue_name=venue_name,
                  venue_image_link=venue_image_link,
                  start_time=start_time
      )
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!', category='success')
      return redirect(url_for('index'))
    except:
      db.session.rollback()
      flash('An error occurred. Show could not be listed.', category='danger')
    finally:
      db.session.close()
  else:
    message = []
    for field, error in form.errors.items():
      message.append(field + ' ' + '|'.join(error))
    if message:
      flash('Errors ' + str(message))
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
