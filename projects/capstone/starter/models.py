import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

from dotenv import load_dotenv

# get vars from .env file
load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST_AND_PORT = os.getenv('HOST_AND_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_FILENAME = os.getenv('DATABASE_FILENAME')

project_dir = os.path.dirname(os.path.abspath(__file__))

#database_path = "postgres://{}:{}@{}/{}".format(USERNAME, PASSWORD, HOST_AND_PORT, DATABASE_NAME)
database_path = "sqlite:///{}".format(os.path.join(project_dir, DATABASE_FILENAME))


db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()



'''
Ticker
'''
class Ticker(db.Model):
    __tablename__ = 'ticker'
    
    id           = db.Column(db.Integer, primary_key=True)
    symbol       = db.Column(db.String)
    name         = db.Column(db.String)
    industry     = db.Column(db.String)
    description  = db.Column(db.String)

    # creates collection of Data objects on Ticker called Ticker.data
    data = db.relationship('Data', backref='ticker', lazy="joined")

    def __init__(self, symbol, name, industry, description):
        self.symbol      = symbol
        self.name        = name
        self.industry    = industry
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()        

    def format(self):
        return {
                 "id":          self.id,
                 "symbol":      self.symbol,
                 "name":        self.name,
                 "industry":    self.industry,
                 "description": self.description
               }

'''
Data
'''
class Data(db.Model):
    __tablename__ = 'data'
    
    id         = db.Column(db.Integer, primary_key=True)
    date       = db.Column(db.String)
    price      = db.Column(db.Integer)
    
    ticker_id  = db.Column(db.String, db.ForeignKey('ticker.id'))


    def __init__(self, date, price, ticker_id):
        self.date      = date
        self.price     = price
        self.ticker_id = ticker_id

    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()        

    def format(self):
        return {
                 "id":        self.id,
                 "date":      self.date,
                 "price":     self.price,
                 "ticker_id": self.ticker_id
               }












