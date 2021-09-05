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
  # implemented below
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
      category_selection = Category.query.order_by(Category.id).all()

      # formatted version
      #categories = [category.format() for category in category_selection]

      # list version kinda works somewhere, but categories should be dictionary per GUI
      #categories = [category.id for category in category_selection]

      # dictionary version (should be correct formatting)
      categories = {category.id: category.type for category in category_selection}

      print('categories:', categories)

      if len(categories) == 0:
          abort(404)

      # testing categories with list of integers works,
      # but using dictionary in the end
      #categories=[1,2,3,4,5,10]
      # when we provide list, categories show as numbers
      # when we provide dictionary, GUI shows names of categories

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
  @app.route("/questions")
  def retrieve_questions():
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      category_selection = Category.query.order_by(Category.id).all()

      # categories - GUI expects not list, but dictionary
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

  ''' COMPLETE
  PATCH question, in rubric is mentioned that we need to test patch as well,
  so creating function for updating questions

  in this case we will be updating 'difficulty'
  '''
  @app.route("/questions/<int:question_id>", methods=["PATCH"])
  def update_question(question_id):
      body = request.get_json()

      try:
          question = Question.query.filter(Question.id == question_id).one_or_none()
          if question is None:
              abort(404)

          if "difficulty" in body:
              question.difficulty = int(body.get("difficulty"))
          #if "category" in body:
          #    question.difficulty = int(body.get("category"))

          question.update()

          return jsonify({
                          "success": True
                        })

      except:
          abort(400)

  '''
  @TODO: COMPLETE
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

          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request, selection)

          # after deletion we can maybe paginate all questions that are left
          # but in the GUI it seems to be working fine, so not sure if it is needed
          return jsonify({"success": True,
                          "deleted": question_id,
                          "questions": current_questions,
                          "total_questions": len(Question.query.all())
                          })

      except:
          abort(422)


  '''
  @TODO: COMPLETE
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

              # do we need current category in response?, will keep it there as None
              return jsonify(
                         {"success": True,
                          "questions": current_questions,
                          "total_questions": len(selection),
                          "current_category": None
                         }
              )

          else:
              question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
              question.insert()

              # include the newly added question in response
              selection = Question.query.order_by(Question.id).all()
              current_questions = paginate_questions(request, selection)

              # returns also paginated view eventually
              return jsonify({"success": True,
                              "created": question.id,
                              "questions": current_questions,
                              "total_questions": len(Question.query.all())
                            })

      except:
          abort(422)



  '''
  @TODO: IMPLEMENTED ABOVE
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
  # actually implemeted in the above function, since both are POST calls
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
  @TODO: COMPLETE
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
  @TODO:   NO IDEA HOW TO PROGRAM IT
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
  @app.route("/quizzes", methods=["POST"])
  def play_quiz():
  # expects POST method
  # incoming POST paiload is
  # 'previous_questions'   []   list of questions, maybe their IDs
  # 'quiz_category'  {"id": 1, "type": "Science"}
  # when all categories:
  # 'quiz_category'  {"id": 0, "type": "click"}

  # GUI has variable currentQuestion - it is dictionary, gets it as result.question
  # it gives us question.id from the database
  # so we need to check if our proposed question, has that id

      body = request.get_json()

      previous_questions   = body.get("previous_questions")
      quiz_category        = body.get("quiz_category")
      category_id          = quiz_category["id"]
      #new_category   = body.get("category", None)
      #new_difficulty = body.get("difficulty", None)
      #search         = body.get("searchTerm", None)

      print('previous_questions: ', previous_questions)
      print('quiz_category: ', quiz_category)
      print('category_id: ', category_id)


      selection = Question.query.filter(Question.category == category_id).all()
      questions = [question.format() for question in selection]
      #quiz_question = questions[1]

      import random
      num = random.randint(0, 10) # it is inclusive - generates integers 0 to 10
      # questions is a list, well, it has to be random,
      # so not from the start of the list

      #for q in questions:
      #    if q["id"] in previous_questions:
      #        print('question id already used')
      #    else:
      #        quiz_question = q
      #        break

      found = False

      while found==False:
          q = random.randint(0, len(questions))

          print('previous_questions: ', previous_questions)
          print('q: ', q)
          if q in previous_questions:
              print('question id already used')
          else:
              quiz_question = questions[q]
              print('quiz_question: ', quiz_question)
              found=True
              #break







      if len(quiz_question) == 0:
          abort(404)


      try:
          # we should return some random question in response payload
          # the question reply payload is a dictionary containing question, category ...

#          return jsonify({
#                          "success": True,
#                          "question": {"question": "ppppppp",
#                                       "answer": "ooooooo",
#                                       "id": 4,
#                                       "difficulty": 2,
#                                       "category": 3
#                          }
#                        })

          return jsonify({
                          "success": True,
                          "question": quiz_question
                        })






      except:
          #abort(422)
          abort(500)











#  @app.route("/questions", methods=["POST"])
#  def create_question():
#      body = request.get_json()
#
#      new_question   = body.get("question", None)
#      new_answer     = body.get("answer", None)
#      new_category   = body.get("category", None)
#      new_difficulty = body.get("difficulty", None)
#      search         = body.get("searchTerm", None)
#
#      try:
#          if search:
#              selection = Question.query.order_by(Question.id).filter(
#                          Question.question.ilike("%{}%".format(search))
#                          ).all()
#
#              current_questions = paginate_questions(request, selection)
#
#              # do we need current category in response?, will keep it there as None
#              return jsonify(
#                         {"success": True,
#                          "questions": current_questions,
#                          "total_questions": len(selection),
#                          "current_category": None
#                         }
#              )
#
#          else:
#              question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
#              question.insert()
#
#              # include the newly added question in response
#              selection = Question.query.order_by(Question.id).all()
#              current_questions = paginate_questions(request, selection)
#
#              # returns also paginated view eventually
#              return jsonify({"success": True,
#                              "created": question.id,
#                              "questions": current_questions,
#                              "total_questions": len(Question.query.all())
#                            })
#
#      except:
#          abort(422)

















  '''
  @TODO: COMPLETE
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
