#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from datetime import datetime
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from forms import *
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# Check models.py for database models
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


def prevent_duplicate_show(show):
    date_of_show = show.start_time
    results = Show.query.all()
    dates = []

    if results != []:
        for records in results:
            dates.append(records.start_time)

        for date in dates:
            if date_of_show not in dates:
                db.session.add(show)
                return False
            else:
                return True
    else:
        db.session.add(show)
        return False

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  city_state = Venue.query.with_entities(Venue.city, Venue.state).group_by(
                    Venue.city, Venue.state).all()

  venues_by_city = Venue.query.with_entities(Venue.id, Venue.name, Venue.city,
                    Venue.state).group_by(Venue.id, Venue.city, Venue.state).\
                    order_by(Venue.id).all()

  data = []
  for records in city_state:
      d = {}
      d["city"] = records[0]
      d["state"] = records[1]
      d["venues"] = []

      for venues in venues_by_city:
          if venues[2] == d["city"] and venues[3] == d["state"]:
              d2 = {}
              d2["id"] = venues[0]
              d2["name"] = venues[1]
              d["venues"].append(d2)
      data.append(d)

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  venues = Venue.query.with_entities(Venue.id, Venue.name).all()
  term = request.form.get('search_term')
  now = datetime.now()
  today = now.strftime("%Y-%m-%d")

  response = {
    "count" : 0,
    "data" : []
  }

  for venue in venues:
      if term.lower() in venue[1].lower():
          response["count"] += 1
          d = {
            "id" : venue[0],
            "name" : venue[1],
            "num_upcoming_shows" : Show.query.filter(Show.start_time > today,
                                    Show.venue_id == venue[0]).count()
          }
          response["data"].append(d)

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.filter(Venue.id == venue_id).first()

  name = venue.name
  genres = venue.genres
  address = venue.address
  city = venue.city
  state = venue.state
  phone = venue.phone
  website = venue.website
  facebook_link = venue.facebook_link
  image_link = venue.image_link
  seeking_talent = venue.seeking_talent
  seeking_description = venue.seeking_description

  now = datetime.now()
  today = now.strftime("%Y-%m-%d")
  past_shows_count = Show.query.filter(Show.start_time < today,
                        Show.venue_id == venue_id).count()

  upcoming_shows_count = Show.query.filter(Show.start_time > today,
                          Show.venue_id == venue_id).count()

  query_past_shows = Show.query.join(Artist).with_entities(Show.artist_id, Artist.name,
                        Artist.image_link, Show.start_time).filter(Show.start_time < today,
                        Show.venue_id == venue_id).all()

  query_upcoming_shows = Show.query.join(Artist).with_entities(Show.artist_id, Artist.name,
                        Artist.image_link, Show.start_time).filter(Show.start_time > today,
                        Show.venue_id == venue_id).all()

  past_shows = []
  for show in query_past_shows:
      d = {}
      d["artist_id"] = show[0]
      d["artist_name"] = show[1]
      d["artist_image_link"] = show[2]
      d["start_time"] = show[3].strftime("%Y-%m-%d %H:%M:%S")
      past_shows.append(d)

  upcoming_shows = []
  for show in query_upcoming_shows:
      d = {}
      d["artist_id"] = show[0]
      d["artist_name"] = show[1]
      d["artist_image_link"] = show[2]
      d["start_time"] = show[3].strftime("%Y-%m-%d %H:%M:%S")
      upcoming_shows.append(d)

  venue_data = {
    "id" : venue_id,
    "name" : name,
    "genres" : genres,
    "address" : address,
    "city" : city,
    "state" : state,
    "phone" : phone,
    "website" : website,
    "facebook_link" : facebook_link,
    "seeking_talent" : seeking_talent,
    "seeking_description" : seeking_description,
    "image_link" : image_link,
    "past_shows" : past_shows,
    "upcoming_shows" : upcoming_shows,
    "past_shows_count" : past_shows_count,
    "upcoming_shows_count" : upcoming_shows_count
  }

  data = venue_data
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form  = VenueForm(request.form)
  error = False
  try:
      new_venue = Venue(
          name = form.name.data,
          city = form.city.data,
          state = form.state.data,
          address = form.address.data,
          phone = form.phone.data,
          genres = request.form.getlist('genres'),
          image_link = form.image_link.data,
          facebook_link = form.facebook_link.data,
          website = form.website_link.data,
          seeking_talent = form.seeking_talent.data,
          seeking_description = form.seeking_description.data
      )
      db.session.add(new_venue)
      db.session.commit()
  except ValueError as e:
      error = True
      print(e)
      db.session.rollback()
  finally:
      db.session.close()

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  if error:
      flash('An error occurred. Venue: ' + form.name.data + ' could not be listed.')
  else:
      flash('Venue ' + form.name.data + ' was successfully listed!')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  error = False
  try:
      venue = Venue.query.get_or_404(venue_id)

      db.session.delete(venue)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
  finally:
      db.session.close()

  return redirect(url_for("index"))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  artist_name = Artist.query.with_entities(Artist.id, Artist.name).order_by(
                Artist.id).all()

  data = []
  for artist in artist_name:
      d = {}
      d["id"] = artist[0]
      d["name"] = artist[1]
      data.append(d)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  artists = Artist.query.with_entities(Artist.id, Artist.name).all()
  term = request.form.get('search_term')
  now = datetime.now()
  today = now.strftime("%Y-%m-%d")

  response = {
    "count" : 0,
    "data" : []
  }

  for artist in artists:
      if term.lower() in artist[1].lower():
          response["count"] += 1
          d = {
            "id" : artist[0],
            "name" : artist[1],
            "num_upcoming_shows" : Show.query.filter(Show.start_time > today,
                                    Show.artist_id == artist[0]).count()
          }
          response["data"].append(d)

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  artist = Artist.query.filter(Artist.id == artist_id).first()

  name = artist.name
  genres = artist.genres
  city = artist.city
  state = artist.state
  phone = artist.phone
  website = artist.website
  facebook_link = artist.facebook_link
  image_link = artist.image_link
  seeking_venue = artist.seeking_venue
  seeking_description = artist.seeking_description

  now = datetime.now()
  today = now.strftime("%Y-%m-%d")
  past_shows_count = Show.query.filter(Show.start_time < today,
                        Show.artist_id == artist_id).count()

  upcoming_shows_count = Show.query.filter(Show.start_time > today,
                          Show.artist_id == artist_id).count()

  query_past_shows = Show.query.join(Venue).with_entities(Show.venue_id, Venue.name,
                        Venue.image_link, Show.start_time).filter(Show.start_time < today,
                        Show.artist_id == artist_id).all()

  query_upcoming_shows = Show.query.join(Venue).with_entities(Show.venue_id, Venue.name,
                        Venue.image_link, Show.start_time).filter(Show.start_time > today,
                        Show.artist_id == artist_id).all()

  past_shows = []
  for show in query_past_shows:
      d = {}
      d["venue_id"] = show[0]
      d["venue_name"] = show[1]
      d["venue_image_link"] = show[2]
      d["start_time"] = show[3].strftime("%Y-%m-%d %H:%M:%S")
      past_shows.append(d)

  upcoming_shows = []
  for show in query_upcoming_shows:
      d = {}
      d["venue_id"] = show[0]
      d["venue_name"] = show[1]
      d["venue_image_link"] = show[2]
      d["start_time"] = show[3].strftime("%Y-%m-%d %H:%M:%S")
      upcoming_shows.append(d)

  artist_data = {
    "id" : artist_id,
    "name" : name,
    "genres" : genres,
    "city" : city,
    "state" : state,
    "phone" : phone,
    "website" : website,
    "facebook_link" : facebook_link,
    "seeking_venue" : seeking_venue,
    "seeking_description" : seeking_description,
    "image_link" : image_link,
    "past_shows" : past_shows,
    "upcoming_shows" : upcoming_shows,
    "past_shows_count" : past_shows_count,
    "upcoming_shows_count" : upcoming_shows_count
  }

  data = artist_data
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  artist = Artist.query.get(artist_id)
  form = ArtistForm(request.form)

  form.name.process_data(artist.name)
  form.city.process_data(artist.city)
  form.state.process_data(artist.state)
  form.phone.process_data(artist.phone)
  form.genres.process_data(artist.genres)
  form.facebook_link.process_data(artist.facebook_link)
  form.image_link.process_data(artist.image_link)
  form.website_link.process_data(artist.website)
  form.seeking_venue.process_data(artist.seeking_venue)
  form.seeking_description.process_data(artist.seeking_description)

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  form = ArtistForm(request.form)

  try:
      artist = Artist.query.get(artist_id)

      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.genres = request.form.getlist('genres')
      artist.facebook_link = form.facebook_link.data
      artist.image_link = form.image_link.data
      artist.website = form.website_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data

      db.session.add(artist)
      db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)

  form = VenueForm(request.form)

  form.name.process_data(venue.name)
  form.city.process_data(venue.city)
  form.state.process_data(venue.state)
  form.phone.process_data(venue.phone)
  form.address.process_data(venue.address)
  form.genres.process_data(venue.genres)
  form.facebook_link.process_data(venue.facebook_link)
  form.image_link.process_data(venue.image_link)
  form.website_link.process_data(venue.website)
  form.seeking_talent.process_data(venue.seeking_talent)
  form.seeking_description.process_data(venue.seeking_description)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  form = VenueForm(request.form)

  try:
      venue = Venue.query.get(venue_id)

      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.genres = request.form.getlist('genres')
      venue.image_link = form.image_link.data
      venue.facebook_link = form.facebook_link.data
      venue.website = form.website_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data

      db.session.add(venue)
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
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  error = False
  try:
      new_artist = Artist(
          name = form.name.data,
          city = form.city.data,
          state = form.state.data,
          phone = form.phone.data,
          genres = request.form.getlist('genres'),
          image_link = form.image_link.data,
          facebook_link = form.facebook_link.data,
          website = form.website_link.data,
          seeking_venue = form.seeking_venue.data,
          seeking_description = form.seeking_description.data
      )
      db.session.add(new_artist)
      db.session.commit()
  except ValueError as e:
      error = True
      print(e)
      db.session.rollback()
  finally:
      db.session.close()

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  if error:
      flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
  else:
      flash('Artist ' + form.name.data + ' was successfully listed!')

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  shows = Show.query.join(Venue).join(Artist, Artist.id == Show.artist_id).with_entities(
            Show.venue_id, Venue.name, Show.artist_id, Artist.name,
            Artist.image_link, Show.start_time).all()

  show_data = []
  for show in shows:
      d = {}
      d["venue_id"] = show[0]
      d["venue_name"] = show[1]
      d["artist_id"] = show[2]
      d["artist_name"] = show[3]
      d["artist_image_link"] = show[4]
      d["start_time"] = show[5].strftime("%Y-%m-%d %H:%M:%S")
      show_data.append(d)

  return render_template('pages/shows.html', shows=show_data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  error = False
  try:
      new_show = Show(
          start_time = form.start_time.data,
          artist_id = form.artist_id.data,
          venue_id = form.venue_id.data
      )
      duplicates = prevent_duplicate_show(new_show)
      db.session.commit()
  except ValueError as e:
      error = True
      print(e)
      db.session.rollback()
  finally:
      db.session.close()

  # on successful db insert, flash success
  if duplicates:
      flash('Show already exists!')
  else:
      flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  if error:
      flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
