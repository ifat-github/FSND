#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime
from models import db, Venue, Artist, Show	

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
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
  list_of_cities = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all() 
  shows = db.session.query(Show).all()

  for city in list_of_cities:
    venues = db.session.query(Venue).filter_by(city=city.city, state=city.state).all() 
    entry = {
          'city': city.city,
          'state': city.state,
          'venues': venues
    }
    data.append(entry)

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  query = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
  response = {
    'count': len(query),
    'data': query
  }

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  past_shows=[]
  upcoming_shows=[]

  venue = Venue.query.get(venue_id)
  past = db.session.query(Show).join(Artist).join(Venue).filter(Show.venue_id==venue_id,Show.artist_id == Artist.id,Show.start_time < datetime.now()).all()
  upcoming = db.session.query(Show).join(Artist).join(Venue).filter(Show.venue_id==venue_id,Show.artist_id == Artist.id,Show.start_time > datetime.now()).all()
  
  for show in past:
    past_shows.append({
      'artist_id': show.artists.id,
      'artist_name': show.artists.name,
      'artist_image_link':show.artists.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    })
  for show in upcoming:
    upcoming_shows.append({
      'artist_id': show.artists.id,
      'artist_name': show.artists.name,
      'artist_image_link': show.artists.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    })

  data = {
    'id': venue_id,
    'name': venue.name,
    'city': venue.city,
    'state': venue.state,
    'address': venue.address,
    'phone': venue.phone,
    'image_link': venue.image_link,
    'facebook_link': venue.facebook_link,
    'website_link': venue.website_link,
    'genres': venue.genres,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description,
    'upcoming_shows': upcoming_shows,  
    'past_shows': past_shows,   
    'upcoming_shows_count': len(upcoming_shows),
    'past_shows_count': len(past_shows)
  }
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    form = VenueForm(request.form)
    venue = Venue()
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({ 'success': True })

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  query = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
  response = {
    'count': len(query),
    'data': query
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  past_shows=[]
  upcoming_shows=[]

  artist = Artist.query.get(artist_id)
  past = db.session.query(Show).join(Artist).join(Venue).filter(Show.artist_id == artist_id,Show.venue_id==Venue.id,Show.start_time < datetime.now()).all()
  upcoming = db.session.query(Show).join(Artist).join(Venue).filter(Show.artist_id == artist_id,Show.venue_id==Venue.id,Show.start_time > datetime.now()).all()
  
  for show in past:
    past_shows.append({
      'venue_id': show.venues.id,
      'venue_name': show.venues.name,
      'venue_image_link':show.venues.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    })
  for show in upcoming:
    upcoming_shows.append({
      'venue_id': show.venues.id,
      'venue_name': show.venues.name,
      'venue_image_link': show.venues.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    })
  data = {
    'id': artist_id,
    'name': artist.name,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'image_link': artist.image_link,
    'facebook_link': artist.facebook_link,
    'website_link': artist.website_link,
    'genres': artist.genres,
    'seeking_venue': artist.seeking_venue,
    'seeking_description': artist.seeking_description,
    'upcoming_shows': upcoming_shows,  
    'past_shows': past_shows,   
    'upcoming_shows_count': len(upcoming_shows),
    'past_shows_count': len(past_shows)
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = db.session.query(Artist).filter_by(id=artist_id).first()
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    form = ArtistForm(request.form)
    artist = Artist.query.filter_by(id=artist_id).first()
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = db.session.query(Venue).filter_by(id=venue_id).first()
  form = VenueForm(obj=venue)
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    form = VenueForm(request.form)
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    form = ArtistForm(request.form)
    artist = Artist()
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  result = []
  shows = Show.query.join(Venue, Show.venue_id == Venue.id).join(
      Artist, Artist.id == Show.artist_id).all()

  for show in shows:

    showObj = {
      "venue_id": show.venue_id,
      "venue_name": show.venues.name,
      "artist_id": show.artist_id,
      "artist_name": show.artists.name,
      "artist_image_link": show.artists.image_link,
      "start_time": str(show.start_time)
    }
    result.append(showObj)
    
  return render_template('pages/shows.html', shows=result)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    form = ShowForm(request.form)
    show = Show()
    form.populate_obj(show)
    start_time = request.form.get('start_time', '')
    show.start_time=start_time

    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

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
