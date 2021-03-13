#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
import sys
import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from sqlalchemy import func
import logging
from flask_migrate import Migrate
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db, Venue, Artist, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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
  data=[]
  venue_data = {}
  venues = Venue.query.all()
  venues_areas = Venue.query.distinct(Venue.city).all()

  for venue_area in venues_areas:
    venue_data = {
      "city": venue_area.city,
      "state": venue_area.state,
      "venues": []
    }
    for venue in venues:
      if venue.city == venue_area.city:
        venue_data['venues'].append({
        "id": venue.id,
        "name": venue.name,
      })
    data.append(venue_data)
    data.sort(key=lambda s: s['state'])
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term')
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%'))
  response = {
    "count": venues.count(),
    "data": []
  }
  veneu_data = {}
  for venue in venues:
    veneu_data = {
      "id": venue.id,
      "name": venue.name,
    }
    response['data'].append(veneu_data)


  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  
  venue = Venue.query.get(venue_id)
  
  past_shows = []
  upcoming_shows = []

  past_shows = db.session.query(Show).join(Venue).filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all()
  upcoming_shows = db.session.query(Show).join(Venue).filter(Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).all()


  # The solution without JOINs
  # show_data = {}
  # for show in venue.shows:
  #   show_data = {
  #     "artist_id": show.artist.id,
  #     "artist_name": show.artist.name,
  #     "artist_image_link": show.artist.image_link,
  #     "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
  #   }
  #   if show.start_time < datetime.now():
  #     past_shows.append(show_data)
  #   else:
  #     upcoming_shows.append(show_data)

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": ''.join(list(filter(lambda x : x!= '{' and x!='}', venue.genres ))).split(','),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": [{
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
      }for show in past_shows],
    "upcoming_shows": [{
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
      }for show in upcoming_shows],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
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
  error = False
  form = VenueForm(request.form, meta={'csrf': False})
  if form.validate():
   try:
     venue_seeking_talent = False
     if (form.seeking_talent.data == 'true'):
       venue_seeking_talent = True
     else:
       pass
     tmp_genres = form.genres.data
     list_of_geners = ','.join(tmp_genres)
     newVenue = Venue(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        address = form.address.data,
        phone = form.phone.data,
        genres = list_of_geners,
        seeking_talent = venue_seeking_talent,
        seeking_description = form.seeking_description.data if venue_seeking_talent else '',
        facebook_link = form.facebook_link.data,
        image_link = form.image_link.data,
        website = form.website.data,
       )
     print(newVenue)
     db.session.add(newVenue)
     db.session.commit()
   except Exception as e:
     print(e)
     error = True
     db.session.rollback()
     print(sys.exc_info())
   finally:
     db.session.close()
   if error:
     flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
   else:
     flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artist_list = Artist.query.all()
  artist_data = {}
  data=[]

  for artist in artist_list:
    artist_data = {
      "id": artist.id,
      "name": artist.name,
    }
    data.append(artist_data)
  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  search_term = request.form.get('search_term')
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%'))
  response = {
    "count": artists.count(),
    "data": []
  }
  artist_data = {}
  for artist in artists:
    artist_data = {
      "id": artist.id,
      "name": artist.name,
    }
    response['data'].append(artist_data)

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.filter_by(id=artist_id).first()
  
  past_shows = []
  upcoming_shows = []

  past_shows = db.session.query(Show).join(Artist).filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()
  upcoming_shows = db.session.query(Show).join(Artist).filter(Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()

  # The solution without JOINs
  # show_data = {}
  # for show in artist.shows:
  #   show_data = {
  #     "venue_id": show.venue.id,
  #     "venue_name": show.venue.name,
  #     "venue_image_link": show.venue.image_link,
  #     "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
  #   }
  #   if show.start_time < datetime.now():
  #     past_shows.append(show_data)
  #   else:
  #     upcoming_shows.append(show_data)

  artist_data={
    "id": artist.id,
    "name": artist.name,
    "genres": ''.join(list(filter(lambda x : x!= '{' and x!='}', artist.genres ))).split(','),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [{
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
      }for show in past_shows],
    "upcoming_shows": [{
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
      }for show in upcoming_shows],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_artist.html', artist=artist_data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  form = ArtistForm(request.form, meta={'csrf': False})
  if form.validate():
   try:
     artist_seeking_venue = False
     if (form.seeking_venue.data == 'true'):
       artist_seeking_venue = True
     else:
       pass
    
     tmp_genres = form.genres.data
     list_of_geners = ','.join(tmp_genres)

     newArtist = Artist(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        phone = form.phone.data,
        genres = list_of_geners,
        seeking_venue = artist_seeking_venue,
        seeking_description = form.seeking_description.data if artist_seeking_venue else '',
        facebook_link = form.facebook_link.data,
        image_link = form.image_link.data,
        website = form.website.data,
       )
     print(newArtist)
     db.session.add(newArtist)
     db.session.commit()
   except Exception as e:
     print(e)
     error = True
     db.session.rollback()
     print(sys.exc_info())
   finally:
     db.session.close()
   if error:
     flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
     return render_template('pages/home.html')
   else:
     flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.all()
  show_data = {}
  data=[]
  
  for show in shows:
    venues_for_this_show = show.venue
    artist_for_this_show = show.artist
    show_data = {
      "venue_id": show.venue_id,
      "venue_name": venues_for_this_show.name,
      "artist_id": artist_for_this_show.id,
      "artist_name": artist_for_this_show.name,
      "artist_image_link": artist_for_this_show.image_link,
      "start_time": format_datetime(show.start_time.strftime("%d/%m/%Y, %H:%M"))
      }
    data.append(show_data)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  form = ShowForm(request.form, meta={'csrf': False})
  if form.validate():
   try:
     newShow = Show(
        start_time = form.start_time.data,
        artist_id = form.artist_id.data,
        venue_id = form.venue_id.data
      )
     print(newShow)
     db.session.add(newShow)
     db.session.commit()
   except Exception as e:
     print(e)
     error = True
     db.session.rollback()
     print(sys.exc_info())
   finally:
    db.session.close()
   if error:
     flash('An error occurred. Show could not be listed.')
     return render_template('pages/home.html')
   else:
     flash('Show was successfully listed!')
   return render_template('pages/home.html')
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
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
