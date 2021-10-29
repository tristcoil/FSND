

# Stock API backend
This is simplified version of an API backend for company stock price evaluation. The aim is to create prototypes of API endpoints whose data would be persisted in a database.
Currently the backend is capable of storing (and providing) very basic information about company that is in the stock market and its price at specific day.
These values need to be created manually via API call.

Application is running in Heroku:
https://test-app-udacity-coil.herokuapp.com/public 

Eventually the intend is to expand this application to have its frontend with graphing capabilities, should serve as stock research tool where we will have stock price and related stock technical indicators.

 

## How to run app locally:
project is written in python3, using postgresql and sqlite databases

```
export environmental variables:
~/Desktop/capstone$ export DATABASE_URL='postgresql://username:password@localhost:5432/capstone'

next run
cd to project directory
pip3 install -r requirements.txt 
createdb capstone
python3 manage.py db init
python3 manage.py db migrate 
python3 manage.py db upgrade

flask run --reload

when we are done, get rid of database:
dropdb capstone


for running tests - also export postgres DATABASE_URL to CLI
since tests are sourcing the main script and main script needs it as well
~/Desktop/capstone$ rm final_project_sqlite_test.db 
~/Desktop/capstone$ python3 test_app.py 
```


## Auth0 part:
Authorize link to get token:
for localhost
https://dev-mjhbba6a.us.auth0.com/authorize?audience=myapi&response_type=token&client_id=jJhcQu4ws1YXBACNxFPglBJ2KzISb12w&redirect_uri=http://localhost:5000/headers

for heroku
https://dev-mjhbba6a.us.auth0.com/authorize?audience=myapi&response_type=token&client_id=jJhcQu4ws1YXBACNxFPglBJ2KzISb12w&redirect_uri=https://test-app-udacity-coil.herokuapp.com/headers


RBAC roles:

Viewer - can get ticker and price data
get:tickers-prices

Updater - can POST, PATCH, DELETE ticker and price data, but not view them
post:tickers-prices
patch:tickers-prices
delete:tickers-prices


Viewer JWT token:

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFtVXQ3UG1wbFJ0NkZQQm1WN1Z0dSJ9.eyJpc3MiOiJodHRwczovL2Rldi1tamhiYmE2YS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI3MjI0NTI5NDM0ODgxNDE4NDYiLCJhdWQiOiJteWFwaSIsImlhdCI6MTYzNTU0OTYyNSwiZXhwIjoxNjM1NjM2MDI1LCJhenAiOiJqSmhjUXU0d3MxWVhCQUNOeEZQZ2xCSjJLeklTYjEydyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OnRpY2tlcnMtcHJpY2VzIl19.YBQATvruyjo7Hlr2NmjwLvOPsDirKtSlc8EWGEX1ZVKLjJvOOQ2mfynmc-2u13ypsN0gpqGp2_LNVyDYWSRhlzUBcIob3MmNgWRqqqen7rNnAA-CTzh1_YBKUtUpLvSZobZmNCrXWahZR5fJ5N7ddBVsFBAB84hr7AOMMu99sR0e47PapWzsY1aLoH4wuVzPNbteEso4xPRjoHc8XOVRdfk2apVtidAopZhTTH3bBpYPQqy4XfHVqj8w4yM9v-dztg0GWSagh17fnDB-cBq1G5v9DghKP3w1El0riJJUMPd9x0L6k-awl-d6O0w5txSMy3EJWupDMQ463brUymxE9g


Updater JWT token:

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFtVXQ3UG1wbFJ0NkZQQm1WN1Z0dSJ9.eyJpc3MiOiJodHRwczovL2Rldi1tamhiYmE2YS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI3MjI0NTI5NDM0ODgxNDE4NDYiLCJhdWQiOiJteWFwaSIsImlhdCI6MTYzNTU0OTM3MiwiZXhwIjoxNjM1NjM1NzcyLCJhenAiOiJqSmhjUXU0d3MxWVhCQUNOeEZQZ2xCSjJLeklTYjEydyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnRpY2tlcnMtcHJpY2VzIiwicGF0Y2g6dGlja2Vycy1wcmljZXMiLCJwb3N0OnRpY2tlcnMtcHJpY2VzIl19.myAr8lJP8SSrmghovnt0VGYhcw7pQseod3HgjFPQPIzE87rJXvnQOQ_l2xAUUlaBHQJsW-cRHvHyIUe_ltONP16ROuuxW5yyiakQTReJT6CcaAIkz8DejaSSEfQSM7pF7i38RjMsYp4GUbbQQ0v9eX7ohjbRy3sFA5vnt55ObzuowH3QaznMZYm807vn_-ZAxeSGNwDuzeHhtMoe7RF6Z6qF8QGJHtpdK3kUL_XWefi9XQZY5u1yC8q1sFCAPQlkphA9WuT3MQCSJocGzb8TkuRY1L526YD5rK0x5PPj0bWZtcTuD0l_MjbWt_Pi6Idm0c26p4C0ipYJQyaKZ_G8iA




## API documentation

```
Endpoints:
GET      '/tickers'
GET      '/prices'
POST     '/tickers'
POST     '/prices'
PATCH    '/tickers/<int:ticker_id>'
PATCH    '/prices/<int:price_id>'
DELETE   '/tickers/<int:ticker_id>'
DELETE   '/prices/<int:price_id>'


Note:
replace 'http://127.0.0.1:5000' with 'https://test-app-udacity-coil.herokuapp.com' when wanting to interact with heroku app
otherwise below commands are for testing locally

Additionally:
example calls to heroku are stored in two postman collections in 'postman_collections' directory


General notes about payload objects in the API:
tickers - list of ticker objects with id (primary db key), symbol, name, description, industry as keys (plus corresponding values)
data - list of data objects with id (primary db key), date, price, ticker_id (foreign key) as keys (plus corresponding values)
total elements - integer, 
success status - boolean



GET '/tickers'
- gets all tickers
- request arguments: None
coil@coil-VM:~/Desktop$ curl http://127.0.0.1:5000/tickers
{"success":true,"tickers":[{"description":"pretty cool company","id":1,"industry":"consumer electronics","name":"Apple","symbol":"AAPL"}],"total_elements":1}

GET '/prices'
- gets all price data
- request arguments: None
coil@coil-VM:~/Desktop$ curl http://127.0.0.1:5000/prices
{"data":[{"date":"2021-10-20","id":1,"price":1,"ticker_id":"1"}],"success":true,"total_elements":1}



POST '/tickers'
- creates new ticker object
- request arguments: dictionary with ticker data
coil@coil-VM:~/Desktop$ curl -X POST -H "Content-Type: application/json" -d '{"symbol":"AAPL", "name": "Apple", "industry": "consumer electronics", "description": "one of FAANG companies"}' http://127.0.0.1:5000/tickers
{"created":1,"success":true,"tickers":[{"description":"one of FAANG companies","id":1,"industry":"consumer electronics","name":"Apple","symbol":"AAPL"}],"total_tickers":1}

POST '/prices'
- creates new data object
- request arguments: dictionary with data
coil@coil-VM:~/Desktop$ curl -X POST -H "Content-Type: application/json" -d '{"date":"2021-10-20", "price": "150", "ticker_id": "1"}' http://127.0.0.1:5000/prices
{"created":1,"data":[{"date":"2021-10-20","id":1,"price":150,"ticker_id":"1"}],"success":true,"total_elements":1}



PATCH    '/tickers/<int:ticker_id>'
- updates given ticker object
- request arguments: dictionary with update data, primary database key of object we want to update
coil@coil-VM:~/Desktop$ curl -X PATCH -H "Content-Type: application/json" -d '{"description": "pretty cool company"}' http://127.0.0.1:5000/tickers/1
{"success":true}
 
PATCH    '/prices/<int:price_id>'
- updates given data object
- request arguments: dictionary update data, primary database key of object we want to update
coil@coil-VM:~/Desktop$ curl -X PATCH -H "Content-Type: application/json" -d '{"price": "1"}' http://127.0.0.1:5000/prices/1
{"success":true}



DELETE   '/tickers/<int:ticker_id>'
- deletes given ticker object
- request arguments: primary database key of object we want to update
coil@coil-VM:~/Desktop$ curl -X DELETE http://127.0.0.1:5000/tickers/1
{"deleted":1,"success":true,"tickers":[],"total_elements":0}

DELETE   '/prices/<int:price_id>'
- deletes given data object
- request arguments: primary database key of object we want to update
coil@coil-VM:~/Desktop$ curl -X DELETE http://127.0.0.1:5000/prices/1
{"data":[],"deleted":1,"success":true,"total_elements":0}

```









## Sources:

### Main sources:
all sources mentioned in below readme files
- https://github.com/tristcoil/FSND/blob/master/projects/01_fyyur/starter_code/README.md
- https://github.com/tristcoil/FSND/blob/master/projects/02_trivia_api/starter/backend/README.md
- https://github.com/tristcoil/FSND/blob/master/projects/03_coffee_shop_full_stack/starter_code/backend/README.md


### Additional sources:

install dotenv library
- https://pypi.org/project/python-dotenv/

bad json in tests
- https://stackoverflow.com/questions/16573332/jsondecodeerror-expecting-value-line-1-column-1-char-0

heroku install
- https://devcenter.heroku.com/articles/heroku-cli#download-and-install

manage.py issues looks like flask_script is not supported anymore - fixed by downgrading to version Flask-Migrate==2
- https://stackoverflow.com/questions/51925284/flask-migrate-modulenotfounderror
- https://github.com/miguelgrinberg/Flask-Migrate/issues/407
- https://issueexplorer.com/issue/miguelgrinberg/Flask-Migrate/407

heroku logs
- https://devcenter.heroku.com/articles/logging#view-logs

JWT token submission
- https://knowledge.udacity.com/questions/703470

cannot find postgresql dialect - need to have postgresql instead of postgres, hence we need to update heroku var to postgresql
- https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre

RBAC mocking with unittests - we need to put dotted path to functions from imported files - patch('auth.some_function')
- https://www.fugue.co/blog/2016-02-11-python-mocking-101
- https://realpython.com/python-mock-library/
- https://www.toptal.com/python/an-introduction-to-mocking-in-python
- https://stackoverflow.com/questions/16060724/patch-why-wont-the-relative-patch-target-name-work
- https://coderedirect.com/questions/507084/patch-why-wont-the-relative-patch-target-name-work

capstone database migrations
- https://classroom.udacity.com/nanodegrees/nd0044-ent/parts/3b182cb8-9978-415d-91af-b3ac260a73c8/modules/4d4996c2-d87b-46f8-8a34-2ca5866cc30b/lessons/cc54b3fe-fb99-477d-9472-60a6b0e727da/concepts/4cccdb28-f803-428e-9e50-416fdf628477








