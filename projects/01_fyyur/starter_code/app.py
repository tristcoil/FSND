#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *               # this imports VenueForm classes reg WTF forms
from datetime import datetime





#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
# DONE, edited the config.py dependency

#------ DB Model imports (only after db is initialized) ---------------------#
from models import Venue, Artist, Show

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
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  print('/VENUES ENDPOINT')
  data = []
  venues = Venue.query.all()
  
  places = Venue.query.distinct(Venue.city, Venue.state).all()
  
  for place in places:
      tmp_venues = []
      
      for venue in venues:
      
          shows = db.session.query(Show).join(Venue.shows).filter(Venue.id == venue.id).all()
          upcoming_shows = []
      
          for show in shows:
              start_time = show.start_time
              start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
      
              if start_time > datetime.now():
                  upcoming_shows.append(show.id) 
      
          if venue.city == place.city and venue.state == place.state:
              tmp_venues.append({"id": venue.id,
                                 "name": venue.name,
                                 "num_upcoming_shows": len(upcoming_shows)
                                })
                                
      data.append({"city": place.city,
                   "state": place.state,
                   "venues": tmp_venues
                  })

  
  return render_template('pages/venues.html', areas=data);
  #return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term')
  
  venues = Venue.query.filter(Venue.name.ilike('%'+str(search_term)+'%'))
  count = venues.count()
  data = []
  
  # fix number of upcoming shows later, but frontend is not even reflecting that, so thats strange
  # maybe fix like this is enough
  
  for venue in venues:
      venue_id = venue.id
      
      shows = db.session.query(Show).join(Venue.shows).filter(Venue.id == venue_id).all()

      upcoming_shows = []
      my_dict = {}
 
      for show in shows:
          start_time = show.start_time
          start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
      
          tmp_show = {"artist_id": show.artist_id,
                          "artist_name": show.artist.name,
                          "artist_image_link": show.artist.image_link,
                          "start_time": show.start_time
                         }

          if start_time > datetime.now():
              upcoming_shows.append(tmp_show)   

      my_dict = {"id": venue.id,
                 "name": venue.name,
                 "num_upcoming_shows": len(upcoming_shows)
                }
  
      data.append(my_dict) 
  
  response = {"count": count,
              "data": data
             }  
  
  print('VENUE RESPONSE: ', response)
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  print ('call to VENUE ID PAGE')
  venue = Venue.query.filter_by(id=venue_id).first()
  print('venue_name ',venue.name)
  
  
  venue = Venue.query.filter_by(id=venue_id).first()
  data = []
  print('venue.id', venue.id)

   
  past_shows = []
  upcoming_shows = []
  data = []
  my_dict = {}

  my_dict = { 
              "id": venue.id,
              "name": venue.name,
              "genres": venue.genres,
              "address": venue.address,
              "city": venue.city,
              "state": venue.state,
              "phone": venue.phone,
              "website": venue.website_link,
              "facebook_link": venue.facebook_link,
              "seeking_talent": venue.seeking_talent,
              "seeking_description": venue.seeking_description,
              "image_link": venue.image_link,  
              "past_shows": past_shows,
              "upcoming_shows": upcoming_shows,
              "past_shows_count": len(past_shows),
              "upcoming_shows_count": len(upcoming_shows)
              }

  print('my_dict', my_dict)
  data.append(my_dict)
  print('data: ', data)
         
  
  
 

  #try:
  shows = db.session.query(Show).join(Venue.shows).filter(Venue.id == venue_id).all()
  venue = Venue.query.filter_by(id=venue_id).first()

  past_shows = []
  upcoming_shows = []
  data = []
  my_dict = {}
 
            
 
  for show in shows:
      print('I GOT HERE')
      start_time = show.start_time
      start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
      
      placeholder_show = {"artist_id": show.artist_id,
                          "artist_name": show.artist.name,
                          "artist_image_link": show.artist.image_link,
                          "start_time": show.start_time
                         }

      if start_time <= datetime.now():
          past_shows.append(placeholder_show)
      else:
          upcoming_shows.append(placeholder_show)    


      my_dict = { 
              "id": venue_id,
              "name": venue.name,
              "genres": venue.genres,
              "address": venue.address,
              "city": venue.city,
              "state": venue.state,
              "phone": venue.phone,
              "website": venue.website_link,
              "facebook_link": venue.facebook_link,
              "seeking_talent": venue.seeking_talent,
              "seeking_description": venue.seeking_description,
              "image_link": venue.image_link,  
              "past_shows": past_shows,
              "upcoming_shows": upcoming_shows,
              "past_shows_count": len(past_shows),
              "upcoming_shows_count": len(upcoming_shows)
              }

      print('my_dict', my_dict)
      data.append(my_dict)

  
  #except Exception as e:
  if len(shows) == 0:    
      venue = Venue.query.filter_by(id=venue_id).first()
      data = []
      print('venue.id', venue.id)

       
      past_shows = []
      upcoming_shows = []
      data = []
      my_dict = {}

      my_dict = { 
              "id": venue.id,
              "name": venue.name,
              "genres": venue.genres,
              "address": venue.address,
              "city": venue.city,
              "state": venue.state,
              "phone": venue.phone,
              "website": venue.website_link,
              "facebook_link": venue.facebook_link,
              "seeking_talent": venue.seeking_talent,
              "seeking_description": venue.seeking_description,
              "image_link": venue.image_link,  
              "past_shows": past_shows,
              "upcoming_shows": upcoming_shows,
              "past_shows_count": len(past_shows),
              "upcoming_shows_count": len(upcoming_shows)
              }

      print('my_dict', my_dict)
      data.append(my_dict)
  
  
  print('data: ', data)
  
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]    # for placeholder data
  data = list(filter(lambda d: d['id'] == venue_id, data ))[0]
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
  
    
  # using WTF forms  
  form = VenueForm(request.form)
  
  # perform WTF contents validation OK validation returns True, otherwise False
  if form.validate():
      pass
  else:
      print('Issue with WTF validation')    
      flash('WARNING: form field did not pass validation')
      # so stay on that submission form so user can fix contents
      return render_template('forms/new_venue.html', form=form)  
  
  
  try:
      venue = Venue(
          name                = form.name.data,
          city                = form.city.data,
          state               = form.state.data,
          address             = form.address.data,
          phone               = form.phone.data,
          genres              = form.genres.data,           
          facebook_link       = form.facebook_link.data,
          image_link          = form.image_link.data,
          website_link        = form.website_link.data,
          seeking_talent      = form.seeking_talent.data,
          seeking_description = form.seeking_description.data  
      )
      
      
      db.session.add(venue)
      db.session.commit()  
      
  
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.                           # i think we can use try except clause and it should work
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except Exception:
      flash('Venue ' + request.form['name'] + ' ERROR encountered while adding data to database')
  
  
  
  return render_template('pages/home.html')



@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  #this should work, not tested, best to create a delete button
  try:
    #Venue.query.filter.by(id=venue_id).delete()
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
        
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  
  print('/ARTISTS ENDPOINT')
  artists = Artist.query.all()
  data = []
  
  for artist in artists:
      my_dict = {"id": artist.id,
                 "name": artist.name
                }
      print(my_dict)           
      data.append(my_dict)
  
  #data is list of short dictionaries

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search_term = request.form.get('search_term')
  
  artists = Artist.query.filter(Artist.name.ilike('%'+str(search_term)+'%'))
  count = artists.count()
  data = []
  
  
  # fix number of upcoming shows later, but frontend is not even reflecting that, so thats strange, likely value not needed
  # likely fixed now
  
  for artist in artists:
      artist_id = artist.id
      
      shows = db.session.query(Show).join(Artist.shows).filter(Artist.id == artist_id).all()

      upcoming_shows = []
      my_dict = {}
 
      for show in shows:
          start_time = show.start_time
          start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
      
          tmp_show = {"artist_id": show.artist_id,
                      "artist_name": show.artist.name,
                      "artist_image_link": show.artist.image_link,
                      "start_time": show.start_time
                     }

          if start_time > datetime.now():
              upcoming_shows.append(tmp_show)   
  
  
      my_dict = {"id": artist.id,
                 "name": artist.name,
                 "num_upcoming_shows": len(upcoming_shows)
                }
  
      data.append(my_dict) 
  
  response = {"count": count,
              "data": data
             }
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  print ('call to ARTISTS ID PAGE')
  shows = db.session.query(Show).join(Artist.shows).filter(Artist.id == artist_id).all()
  artist = Artist.query.filter_by(id=artist_id).first()

  past_shows = []
  upcoming_shows = []
  data = []
  my_dict = {}
 
  for show in shows:
  
      start_time = show.start_time
      start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
      
      placeholder_show = {"venue_id": show.venue_id,
                   "venue_name": show.venue.name,
                   "venue_image_link": show.venue.image_link,
                   "start_time": show.start_time
                   }

      if start_time <= datetime.now():
          past_shows.append(placeholder_show)
      else:
          upcoming_shows.append(placeholder_show)    

      my_dict = { 
          "id": artist_id,
          "name": artist.name,
          "genres": artist.genres,
          "city": artist.city,
          "state": artist.state,
          "phone": artist.phone,
          "website": artist.website_link,
          "facebook_link": artist.facebook_link,
          "seeking_venue": artist.seeking_venue,
          "seeking_description": artist.seeking_description,
          "image_link": artist.image_link,  
          "past_shows": past_shows,
          "upcoming_shows": upcoming_shows,
          "past_shows_count": len(past_shows),
          "upcoming_shows_count": len(upcoming_shows)
          }

      print('my_dict', my_dict)
      data.append(my_dict)

  if len(shows) == 0:    
      artist = Artist.query.filter_by(id=artist_id).first()
      data = []
      print('artist.id', artist.id)

       
      past_shows = []
      upcoming_shows = []
      data = []
      my_dict = {}

      my_dict = { 
              "id": artist.id,
              "name": artist.name,
              "genres": artist.genres,
              "city": artist.city,
              "state": artist.state,
              "phone": artist.phone,
              "website": artist.website_link,
              "facebook_link": artist.facebook_link,
              "seeking_venue": artist.seeking_venue,
              "seeking_description": artist.seeking_description,
              "image_link": artist.image_link,  
              "past_shows": past_shows,
              "upcoming_shows": upcoming_shows,
              "past_shows_count": len(past_shows),
              "upcoming_shows_count": len(upcoming_shows)
              }

      print('my_dict', my_dict)
      data.append(my_dict)  
      
  
  #data = list(filter(lambda d: d['id'] == artist_id, [my_dict, data1, data2, data3] ))[0]     
  data = list(filter(lambda d: d['id'] == artist_id, data ))[0]   # with my payload
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist=Artist.query.get(artist_id)
  if artist:
      form.name.data = artist.name
      form.genres.data = artist.genres            
      form.city.data = artist.city
      form.state.data = artist.state
      form.phone.data = artist.phone
      form.website_link.data = artist.website_link
      form.facebook_link.data = artist.facebook_link
      form.seeking_venue.data = artist.seeking_venue
      form.seeking_description.data = artist.seeking_description
      form.image_link.data = artist.image_link  

  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  
  # using WTF forms  
  form = ArtistForm(request.form)
  
  artist = Artist.query.get(artist_id)

  # perform WTF contents validation OK validation returns True, otherwise False
  if form.validate():
      pass
  else:
      print('Issue with WTF validation')    
      flash('WARNING: form field did not pass validation')
      # so stay on that submission form so user can fix contents
      return render_template('forms/edit_artist.html', form=form, artist=artist)



    
  artist = Artist.query.get(artist_id)

  try:
      # using WTF forms
      artist.name                 = form.name.data
      artist.genres               = form.genres.data                        
      artist.city                 = form.city.data
      artist.state                = form.state.data
      artist.phone                = form.phone.data
      artist.website_link         = form.website_link.data
      artist.facebook_link        = form.facebook_link.data
      artist.seeking_venue        = form.seeking_venue.data
      artist.seeking_description  = form.seeking_description.data
      artist.image_link           = form.image_link.data 


      db.session.commit()
      flash('Records updated')
  except:
      db.session.rollback()
      flash('ERROR updating records')
  finally:
      db.session.close()    


  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  venue=Venue.query.get(venue_id)
  if venue:
      form.name.data = venue.name
      form.genres.data = venue.genres       
      form.address.data = venue.address
      form.city.data = venue.city
      form.state.data = venue.state
      form.phone.data = venue.phone
      form.website_link.data = venue.website_link
      form.facebook_link.data = venue.facebook_link
      form.seeking_talent.data = venue.seeking_talent
      form.seeking_description.data = venue.seeking_description
      form.image_link.data = venue.image_link    

  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  # using WTF forms  
  form = VenueForm(request.form)

  venue = Venue.query.get(venue_id)

  # perform WTF contents validation OK validation returns True, otherwise False
  if form.validate():
      pass
  else:
      print('Issue with WTF validation')    
      flash('WARNING: form field did not pass validation')
      # so stay on that submission form so user can fix contents
      return render_template('forms/edit_venue.html', form=form, venue=venue)

  
  

  try:
      # using WTF forms
      venue.name                 = form.name.data
      venue.genres               = form.genres.data                  
      venue.address              = form.address.data
      venue.city                 = form.city.data
      venue.state                = form.state.data
      venue.phone                = form.phone.data
      venue.website_link         = form.website_link.data
      venue.facebook_link        = form.facebook_link.data
      venue.seeking_talent       = form.seeking_talent.data
      venue.seeking_description  = form.seeking_description.data
      venue.image_link           = form.image_link.data   
    

      db.session.commit()
      flash('Records updated')
  except:
      db.session.rollback()
      flash('ERROR updating records')
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
    
  # using WTF forms  
  form = ArtistForm(request.form)
  
  # perform WTF contents validation OK validation returns True, otherwise False
  if form.validate():
      pass
  else:
      print('Issue with WTF validation')    
      flash('WARNING: form field did not pass validation')
      # so stay on that submission form so user can fix contents
      return render_template('forms/new_artist.html', form=form)
  
  try:
      artist = Artist(
          name                = form.name.data,
          city                = form.city.data,
          state               = form.state.data,
          phone               = form.phone.data,
          genres              = form.genres.data,           
          facebook_link       = form.facebook_link.data,
          image_link          = form.image_link.data,
          website_link        = form.website_link.data,
          seeking_venue       = form.seeking_venue.data,
          seeking_description = form.seeking_description.data  
      )
      
      
      db.session.add(artist)
      db.session.commit()    
               
                      
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  except Exception:
      flash('Artist ' + request.form['name'] + ' ERROR encountered while adding data to database') 

  return render_template('pages/home.html')

  

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  # order the query by venue id and then just add it to list, it will preserve order 
  #  fyuur=# select * from "Show";
  # id | artist_id | venue_id |     start_time      
  #----+-----------+----------+---------------------
  #  1 |         1 |        1 | 2021-08-15 22:44:37
  #  2 |         1 |        2 | 2021-08-15 23:45:04
  #  3 |         4 |        1 | 2021-08-16 23:39:30

  shows = db.session.query(Show).join(Venue.shows).order_by(db.desc(Show.venue_id)).all()
  
  data = []
  
  for show in shows:
      tmp_show = {'venue_id':show.venue_id,
                  'venue_name': show.venue.name,
                  'artist_id': show.artist_id,
                  'artist_name': show.artist.name,
                  'artist_image_link': show.artist.image_link,
                  'start_time': show.start_time
                 }
  
      print('tmp_show', tmp_show)  
      data.append(tmp_show)  
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # using WTF forms  
  form = ShowForm(request.form)
  
  # perform WTF contents validation OK validation returns True, otherwise False
  if form.validate():
      pass
  else:
      print('Issue with WTF validation')    
      flash('WARNING: form field did not pass validation')
      # so stay on that submission form so user can fix contents
      return render_template('forms/new_show.html', form=form)  
  
  
  try:
      show = Show(
          artist_id        = form.artist_id.data,
          venue_id         = form.venue_id.data,
          start_time       = form.start_time.data,
      )
            
      db.session.add(show)
      db.session.commit()    


      # on successful db insert, flash success
      flash('Show was successfully listed!')
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except Exception as e:
      print('ERROR: ', str(e))
      flash('ERROR adding a show to database')
  
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
