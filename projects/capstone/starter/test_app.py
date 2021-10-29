import os
import unittest
from unittest.mock import patch
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Ticker, Data
from auth import get_token_auth_header, verify_decode_jwt

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
        
        self.patch_ticker = {"symbol":"MMM"}
        self.patch_price  = {"price": "1"}        
        
        
        # RBAC user roles
        self.viewer_payload  = {'permissions': ['get:tickers-prices']}
        self.updater_payload = {'permissions': ['post:tickers-prices', 'patch:tickers-prices', 'delete:tickers-prices']}
        self.invalid_payload = {'permissions': ['get:invalid']}
         
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
# GET SUCCESS
    def test_get_public_endpoint(self):
        res = self.client().get("/headers")
        data = json.loads(res.data)
        
        print('------data: -------', data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)     
    
    
    def test_get_tickers(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.viewer_payload
    
            res = self.client().get("/tickers")
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)    
        

    def test_get_prices(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.viewer_payload        
    
            res = self.client().get("/prices")
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)


# GET FAILURE
    def test_error_get_public_endpoint(self):
        res = self.client().get("/headers/1")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)     
    
    
    def test_error_get_tickers(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.viewer_payload
    
            res = self.client().get("/tickers/1")
            data = json.loads(res.data)  
        
            self.assertEqual(res.status_code, 405)
            self.assertEqual(data["success"], False)    
        
    def test_error_get_prices(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.viewer_payload        
    
            res = self.client().get("/prices/1")
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 405)
            self.assertEqual(data["success"], False)



# POST SUCCESS
    def test_create_new_ticker(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.updater_payload
    
            res = self.client().post("/tickers", json=self.new_ticker)
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)


    def test_create_new_price(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.updater_payload
    
            res = self.client().post("/prices", json=self.new_data)
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)



# POST FAILURE
    def test_500_error_create_new_ticker(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.updater_payload
    
            res = self.client().post("/tickers", json='')
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 500)
            self.assertEqual(data["success"], False)


    def test_500_error_create_new_price(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.updater_payload
    
            res = self.client().post("/prices", json='')
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 500)
            self.assertEqual(data["success"], False)




#PATCH SUCCESS
    def test_patch_ticker(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.updater_payload
    
            res = self.client().patch("/tickers/1", json=self.patch_ticker)
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)


    def test_patch_price(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.updater_payload
    
            res = self.client().patch("/prices/1", json=self.patch_price)
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)


#PATCH FAILURE
    def test_error_patch_ticker(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.updater_payload
    
            res = self.client().patch("/tickers/10000", json=self.patch_ticker)
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data["success"], False)


    def test_error_patch_price(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.updater_payload
    
            res = self.client().patch("/prices/10000", json=self.patch_price)
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data["success"], False)





#DELETE SUCCESS
    def test_delete_ticker(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.updater_payload
    
            res = self.client().delete("/tickers/2")
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)


    def test_delete_price(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.updater_payload
    
            res = self.client().delete("/prices/2")
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)



#DELETE FAILURE
    def test_error_delete_ticker(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.updater_payload
    
            res = self.client().delete("/tickers/10000")
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data["success"], False)


    def test_error_delete_price(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.updater_payload
    
            res = self.client().delete("/prices/10000")
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data["success"], False)




# ------ invalid RBAC role calls ------
# GET
    def test_get_tickers_RBAC_error(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.invalid_payload
    
            res = self.client().get("/tickers")
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 500)
            self.assertEqual(data["success"], False) 

    def test_get_prices_RBAC_error(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.invalid_payload
    
            res = self.client().get("/prices")
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 500)
            self.assertEqual(data["success"], False) 

# POST
    def test_create_new_ticker_RBAC_error(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.invalid_payload
    
            res = self.client().post("/tickers", json=self.new_ticker)
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 500)
            self.assertEqual(data["success"], False)


    def test_create_new_price_RBAC_error(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.invalid_payload
    
            res = self.client().post("/prices", json=self.new_data)
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 500)
            self.assertEqual(data["success"], False)    
    
# PATCH
    def test_patch_ticker_RBAC_error(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.invalid_payload
    
            res = self.client().patch("/tickers/1", json=self.patch_ticker)
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 500)
            self.assertEqual(data["success"], False)


    def test_patch_price_RBAC_error(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.invalid_payload
    
            res = self.client().patch("/prices/1", json=self.patch_price)
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 500)
            self.assertEqual(data["success"], False)


# DELETE
    def test_delete_tickers_RBAC_error(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.invalid_payload
    
            res = self.client().delete("/tickers/1")
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 500)
            self.assertEqual(data["success"], False) 

    def test_delete_prices_RBAC_error(self):
        with patch('auth.get_token_auth_header') as mock_token:
          mock_token.return_value = 'some_token'
          with patch('auth.verify_decode_jwt') as mock_payload:
            mock_payload.return_value = self.invalid_payload
    
            res = self.client().delete("/prices/1")
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 500)
            self.assertEqual(data["success"], False)     





# execute unittests
if __name__ == "__main__":
    unittest.main()



