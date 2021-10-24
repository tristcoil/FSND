# Backend - Full Stack Trivia API

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.


3. Create an endpoint to handle GET requests for all available categories.


4. Create an endpoint to DELETE question using a question ID.


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.


6. Create a POST endpoint to get questions based on category.


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.


9. Create error handlers for all expected errors including 400, 404, 422 and 500.



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## Backend API documentation and example API calls
```
Endpoints:
GET    '/categories'                                   
GET    '/questions'                                    
PATCH  '/questions/<int:question_id>'                  
DELETE '/questions/<int:question_id>'                  
POST   '/questions' # posts new question               
POST   '/questions' # searches questions               
GET    '/categories/<int:category_id>/questions'       
POST   '/quizzes'




GET '/categories'
- gets all categories
- request arguments: None
- returns: category object with category integer value and corresponding category as a string, success status as a boolean
coil@coil-VM:~/Desktop$ curl -X GET http://127.0.0.1:5000/categories
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}


GET '/questions'
- gets all questions
- request arguments: None
- returns: 
  category object with category integer value and corresponding category as a string,
  paginated question object with answer, category, difficulty, id and question as keys (plus corresponding values),
  current category as null,
  total amount of questions as integer, 
  success status as a boolean

coil@coil-VM:~/Desktop$ curl -X GET http://127.0.0.1:5000/questions
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 

    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "total_questions": 37
}
coil@coil-VM:~/Desktop$ 



PATCH  '/questions/<int:question_id>' 
- updates question (updates question difficulty)
- request arguments: <int:question_id>, key/value pair to update
- returns: 
  success status as a boolean

coil@coil-VM:~/Desktop$ curl -X PATCH -H "Content-Type: application/json" -d '{"difficulty": "1"}' http://127.0.0.1:5000/questions/12
{
  "success": true
}
coil@coil-VM:~/Desktop$ 





DELETE '/questions/<int:question_id>' 
- deletes specified question
- request arguments: <int:question_id
- returns: 
  primary database key of deleted question as integer
  questions that are remaining - paginated question object with answer, category, difficulty, id and question as keys (plus corresponding values),
  questions that are remaining - total amount of questions as integer, 
  success status as a boolean  

coil@coil-VM:~/Desktop$ curl -X DELETE http://127.0.0.1:5000/questions/11
{
  "deleted": 11, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 36
}
coil@coil-VM:~/Desktop$ 





POST   '/questions' # posts new question 
- creates new question
- request arguments: question, answer, category, difficulty as keys and their appropriate values
- returns: 
  primary database key of created question as integer
  all questions after addition - paginated question object with answer, category, difficulty, id and question as keys (plus corresponding values),
  all questions after addition - total amount of questions as integer, 
  success status as a boolean  


coil@coil-VM:~/Desktop$ curl -X POST -H "Content-Type: application/json" -d '{"question": "test question", "answer": "test answer", "category": "1", "difficulty": "1"}' http://127.0.0.1:5000/questions
{
  "created": 45, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 37
}
coil@coil-VM:~/Desktop$ 




POST   '/questions' # searches questions 
- searches questions based on provided keyword

- request arguments: searchTerm and its value
- returns: 
  current category as null
  found questions - paginated question object with answer, category, difficulty, id and question as keys (plus corresponding values),
  found questions - total amount of questions as integer, 
  success status as a boolean  

coil@coil-VM:~/Desktop$ curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "test"}' http://127.0.0.1:5000/questions
{
  "current_category": null, 
  "questions": [
    {
      "answer": "test answer", 
      "category": 1, 
      "difficulty": 1, 
      "id": 45, 
      "question": "test question"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
coil@coil-VM:~/Desktop$ 



GET    '/categories/<int:category_id>/questions'
- gets all questions for specified category
- request arguments: <int:category_id
- returns: 
  paginated question object with answer, category, difficulty, id and question as keys (plus corresponding values),
  current category as integer,
  total amount of questions in given category as integer, 
  success status as a boolean


coil@coil-VM:~/Desktop$ curl -X GET http://127.0.0.1:5000/categories/2/questions
{
  "current_category": 2, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "total_questions": 8
}
coil@coil-VM:~/Desktop$ 




POST   '/quizzes'
- provides quiz question based on requested category, excludes questions that have already been asked previously
- request arguments: list of integers - previously asked question ids, quiz category key, with type and id and their respective values
- returns: 
  question object with answer, category, difficulty, id and question as keys (plus corresponding values),
  success status as a boolean

request for questions from all categories:
coil@coil-VM:~/Desktop$ curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[13,14],"quiz_category":{"type":"click","id":0}}' http://127.0.0.1:5000/quizzes
{
  "question": {
    "answer": "Tom Cruise", 
    "category": 5, 
    "difficulty": 4, 
    "id": 4, 
    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  }, 
  "success": true
}
coil@coil-VM:~/Desktop$ 

request for questions from specific category:
coil@coil-VM:~/Desktop$ curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[13,14],"quiz_category":{"type":"Science","id":1}}' http://127.0.0.1:5000/quizzes
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}
coil@coil-VM:~/Desktop$ 

```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql , better to use modified version as psql trivia_test < trivia_coil.psql
python test_flaskr.py or python3 test_flaskr.py
```

## Sources

project based on these two related Udacity repos: 
- https://github.com/udacity/FSND
- https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises

fixing categories to dictionary
- https://knowledge.udacity.com/questions/664537

PUT vs POST
- https://stackoverflow.com/questions/630453/what-is-the-difference-between-post-and-put-in-http

get environment variables from env file
- https://www.activestate.com/blog/python-environment-variables-vs-secrets/
- https://stackoverflow.com/questions/40216311/reading-in-environment-variables-from-an-environment-file

