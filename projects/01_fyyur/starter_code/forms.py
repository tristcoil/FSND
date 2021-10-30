from datetime import datetime
#from flask_wtf import Form
from flask_wtf import FlaskForm
import flask_wtf
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, Optional, InputRequired, ValidationError

import re


# this file is being updated based on reviever feedback
# https://review.udacity.com/#!/reviews/3249321


#var definitions
genres_lst = [   
                ('Alternative', 'Alternative'),
                ('Blues', 'Blues'),
                ('Classical', 'Classical'),
                ('Country', 'Country'),
                ('Electronic', 'Electronic'),
                ('Folk', 'Folk'),
                ('Funk', 'Funk'),
                ('Hip-Hop', 'Hip-Hop'),
                ('Heavy Metal', 'Heavy Metal'),
                ('Instrumental', 'Instrumental'),
                ('Jazz', 'Jazz'),
                ('Musical Theatre', 'Musical Theatre'),
                ('Pop', 'Pop'),
                ('Punk', 'Punk'),
                ('R&B', 'R&B'),
                ('Reggae', 'Reggae'),
                ('Rock n Roll', 'Rock n Roll'),
                ('Soul', 'Soul'),
                ('Other', 'Other'),
             ]   



state_lst =  [
                ('AL', 'AL'),
                ('AK', 'AK'),
                ('AZ', 'AZ'),
                ('AR', 'AR'),
                ('CA', 'CA'),
                ('CO', 'CO'),
                ('CT', 'CT'),
                ('DE', 'DE'),
                ('DC', 'DC'),
                ('FL', 'FL'),
                ('GA', 'GA'),
                ('HI', 'HI'),
                ('ID', 'ID'),
                ('IL', 'IL'),
                ('IN', 'IN'),
                ('IA', 'IA'),
                ('KS', 'KS'),
                ('KY', 'KY'),
                ('LA', 'LA'),
                ('ME', 'ME'),
                ('MT', 'MT'),
                ('NE', 'NE'),
                ('NV', 'NV'),
                ('NH', 'NH'),
                ('NJ', 'NJ'),
                ('NM', 'NM'),
                ('NY', 'NY'),
                ('NC', 'NC'),
                ('ND', 'ND'),
                ('OH', 'OH'),
                ('OK', 'OK'),
                ('OR', 'OR'),
                ('MD', 'MD'),
                ('MA', 'MA'),
                ('MI', 'MI'),
                ('MN', 'MN'),
                ('MS', 'MS'),
                ('MO', 'MO'),
                ('PA', 'PA'),
                ('RI', 'RI'),
                ('SC', 'SC'),
                ('SD', 'SD'),
                ('TN', 'TN'),
                ('TX', 'TX'),
                ('UT', 'UT'),
                ('VT', 'VT'),
                ('VA', 'VA'),
                ('WA', 'WA'),
                ('WV', 'WV'),
                ('WI', 'WI'),
                ('WY', 'WY'),
             ]




def validate_phone(form, field):
    # checks if phone number is in valid format
    phone_number = field.data
    #print('--- phone number ---', phone_number)
    match = bool( re.match( r"^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$", phone_number))
    if not match:
        raise ValidationError('phone has to be in format xxx-xxx-xxxx')        

def validate_facebook(form, field):
    #just very simple check that string contains facebook
    # we use also URL() method for this field, should be sufficient
    form_string = field.data
    if not re.search('facebook.com', form_string):
        raise ValidationError('link needs to contain facebook.com substring')

def validate_genres(form, field):
    my_genres=field.data
    if not set(my_genres).issubset(dict(genres_lst).keys()):
        raise ValidationError('Wrong genres specified')

def validate_state(form, field):
    my_state=field.data
    if my_state not in dict(state_lst).keys():
        raise ValidationError('Wrong state specified')





class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id', validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id', validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )



class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(), validate_state],
        choices=state_lst
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[validate_phone]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired(), validate_genres],
        choices=genres_lst
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL(), validate_facebook]
    )
    website_link = StringField(
        'website_link', validators=[Optional(), URL()]
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )





class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(), validate_state],
        choices=state_lst
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[validate_phone]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired(), validate_genres],
        choices=genres_lst 
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[Optional(), URL(), validate_facebook]
    )
    website_link = StringField(
        'website_link', validators=[Optional(), URL()]
    )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
    )



        
        

        
