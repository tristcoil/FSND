import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS headers
  @app.after_request
  def after_request(response):
      response.headers.add(
          "Access-Control-Allow-Origin", "*"
      )
      response.headers.add(
          "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
      )
      response.headers.add(
          "Access-Control-Allow-Methods", "GET,POST,DELETE,PUT,PATCH,OPTIONS"
      )
      return response


  '''
  @TODO: prog
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route("/categories")
  def retrieve_categories():
      selection = Category.query.order_by(Category.id).all()

      categories = [category.format() for category in selection]
      # maybe better
      categories = [category.id for category in selection]
      print('categories:', categories)


      if len(categories) == 0:
          abort(404)

      # not sure what the frontend is expecting really
      # looks like it just wants list of integers, lol
      #categories=[1,2]

      return jsonify(
          {
              "success": True,
              "categories": categories
          }
      )



  '''
  @TODO: prog
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
# I wrote this part
  @app.route("/questions")
  def retrieve_questions():
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      category_selection = Category.query.order_by(Category.id).all()
      #categories = [category.id for category in category_selection]
      categories = {category.id: category.type for category in category_selection}

      if len(current_questions) == 0:
          abort(404)

      return jsonify(
          {
              "success": True,
              "questions": current_questions,
              "total_questions": len(Question.query.all()),
              "categories": categories,
              "current_category": None
          }
      )




  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
  @app.route("/questions/<int:question_id>", methods=["DELETE"])
  def delete_question(question_id):
      try:
          question = Question.query.filter(Question.id == question_id).one_or_none()

          if question is None:
              abort(404)

          question.delete()

          #after deletion we can maybe paginate all questions that are left
          return jsonify({"success": True,
                          "deleted": question_id})

      except:
          abort(422)





  '''
  @TODO: prog
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
  # there are 2 POST calls to /questions, so we need to decide based on payload contents

  @app.route("/questions", methods=["POST"])
  def create_question():
      body = request.get_json()

      new_question   = body.get("question", None)
      new_answer     = body.get("answer", None)
      new_category   = body.get("category", None)
      new_difficulty = body.get("difficulty", None)
      search         = body.get("searchTerm", None)

      try:
          if search:
              selection = Question.query.order_by(Question.id).filter(
                          Question.question.ilike("%{}%".format(search))
                          ).all()

              current_questions = paginate_questions(request, selection)
              return jsonify(
                         {"success": True,
                          "questions": current_questions,
                          "total_questions": len(selection),
                          "current_category": 1
                         }
              )

          else:
              question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
              question.insert()

              # !!!return also paginated view eventually
              return jsonify({"success": True,
                              "created": question.id})

      except:
          abort(422)



  '''
  @TODO: hmm also doable, add some aborts
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
  # implemeted in above function
  #NOTES: /questions     POST     payload comes with searchTerm
  #expects:
  #success
  #questions
  #total_questions
  #current_category
  #@app.route("/questions", methods=["POST"])
  #def search_questions():
  #    body = request.get_json()
  #
  #    search = body.get("searchTerm", None)
  #
  #    if search:
  #        selection = Question.query.order_by(Question.id).filter(
  #        Question.question.ilike("%{}%".format(search))
  #        ).all()
  #
  #        current_questions = paginate_questions(request, selection)
  #        return jsonify(
  #                       {"success": True,
  #                        "questions": current_questions,
  #                        "total_questions": len(selection),
  #                        "current_category": 1
  #                       }
  #        )




  '''
  @TODO:  hmm doable
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route("/categories/<int:category_id>/questions")
  def get_questions_by_category(category_id):

      try:
          selection = Question.query.filter(Question.category == category_id).all()
          current_questions = paginate_questions(request, selection)

          if len(current_questions) == 0:
              abort(404)

          return jsonify(
              {
                  "success": True,
                  "questions": current_questions,
                  "total_questions": len(selection),
                  "current_category": category_id
              }
          )


      except:
          abort(422)








  '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

  '''
  @TODO: x
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(404)
  def not_found(error):
      return (
          jsonify({"success": False, "error": 404, "message": "resource not found"}),
          404
      )

  @app.errorhandler(422)
  def unprocessable(error):
      return (
          jsonify({"success": False, "error": 422, "message": "unprocessable"}),
          422
      )

  @app.errorhandler(400)
  def bad_request(error):
      return (
          jsonify({"success": False, "error": 400, "message": "bad request"}),
          400
      )

  @app.errorhandler(405)
  def method_not_allowed(error):
      return (
          jsonify({"success": False, "error": 405, "message": "method not allowed"}),
          405
      )


  return app
