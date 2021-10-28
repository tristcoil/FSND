import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Ticker, Data

from dotenv import load_dotenv

# get vars from .env file
load_dotenv()
DATABASE_FILENAME = os.getenv('TEST_DATABASE_NAME')
DATABASE_NAME = os.getenv('TEST_DATABASE_NAME')

project_dir = os.path.dirname(os.path.abspath(__file__))











class TestCase(unittest.TestCase):
   
    
    def setUp(self):    
    
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DATABASE_NAME
        
        self.database_path = "sqlite:///{}".format(os.path.join(project_dir, self.database_name))
        
        setup_db(self.app, self.database_path)
        

        
        # mock data
        self.new_ticker = {"symbol":"AAPL", "name": "Apple", "industry": "consumer electronics", "description": "one of FAANG companies"}
        self.new_data   = {"date":"2021-10-20", "price": "150", "ticker_id": "1"}
        
         
        # binds app to our context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()            
            

        ticker = Ticker(symbol="IBM", name="IBM", industry="IT", description="IBM is IT company")
        ticker.insert() 
         
        data = Data(date="2021-10-20", price="150", ticker_id="1")
        data.insert() 







    def tearDown(self):
        pass
        
        
        
    # -------------- TESTS ----------------
    
    def test_get_public_endpoint(self):
        res = self.client().get("/public")
        data = json.loads(res.data)
        
        print('------data: -------', data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)     
    
    
    def test_get_tickers(self):
        res = self.client().get("/tickers")
        data = json.loads(res.data)
        
        print('------data: -------', data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)    
        

    def test_get_prices(self):
        res = self.client().get("/prices")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


















# execute unittests
if __name__ == "__main__":
    unittest.main()



