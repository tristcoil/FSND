from flask_sqlalchemy import SQLAlchemy
#from app import db


db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String))                  #list of stuff from database      like fetch all or something
    website_link = db.Column(db.String)
    seeking_talent = db.Column(db.String)
    seeking_description = db.Column(db.String)
    
    # this creates collection of Show objects on Venue called Venue.shows
    shows = db.relationship('Show', backref='venue', lazy="joined")
    


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))      # needs to be an array
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    image_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy="joined")

    

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# show is CHILD TABLE
class Show(db.Model):
    __tablename__ = 'Show'
    
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String)
    #shows are connected to artist and to venue as well
    # so there might be like parent / child relation
    artist_id  = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_id   = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    start_time = db.Column(db.String)


