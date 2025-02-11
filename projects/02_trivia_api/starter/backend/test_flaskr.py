import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from dotenv import load_dotenv


# get vars from .env file
load_dotenv()
USERNAME      = os.getenv('TEST_USERNAME')
PASSWORD      = os.getenv('TEST_PASSWORD')
HOST_AND_PORT = os.getenv('TEST_HOST_AND_PORT')
DATABASE_NAME = os.getenv('TEST_DATABASE_NAME')



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        #self.database_name = ""
        self.database_name = DATABASE_NAME

        #self.database_path = "postgres://{}:{}@{}/{}".format("", "", ':', self.database_name)
        self.database_path = "postgres://{}:{}@{}/{}".format(USERNAME, PASSWORD, HOST_AND_PORT, self.database_name)
        setup_db(self.app, self.database_path)

        # payload for new question creation and quiz request
        self.new_question = {"question": "What is your favourite actor.", "answer": "Tom Hanks", "difficulty": 1, "category": 1}
        self.quiz_request = {"previous_questions": [],
                             "quiz_category": {
                                               "id": 1,
                                               "type": "Science"
                                              }
                            }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("\questions?page=1000", json={"difficulty": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # the PATCH method not implemented yet in web page, but PATCH is required in rubric
    def test_update_question_difficulty(self):
        res = self.client().patch("/questions/5", json={"difficulty": 1})
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(question.format()["difficulty"], 1)

    def test_400_for_failed_update(self):
        # no payload, hence update fails
        res = self.client().patch("/questions/5")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))


    def test_put_create_new_question(self):
        res = self.client().put("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))







    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post("/questions/1000", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    # delete question 11 that is by default in trivia_test database
    def test_delete_question(self):
        # delete specific element from database
        res = self.client().delete("/questions/11")
        data = json.loads(res.data)

        # now we should get 'None' since that question is deleted
        question = Question.query.filter(Question.id == 11).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 11)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(question, None)


    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_quiz_response(self):
        res = self.client().post("/quizzes", json=self.quiz_request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])


    def test_500_quiz_server_fault(self):
        res = self.client().post("/quizzes")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "server error")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
