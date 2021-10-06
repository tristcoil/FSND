import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth



# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------



app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
###db_drop_and_create_all()











# ROUTES




# delete this later, it has to be in different part of script
@app.route('/headers')
#@requires_auth('get:drinks-detail')  # should work for Barista, Manager
@requires_auth()  # should work for Barista, Manager
def headers(payload):
    print(payload)
    return 'Access Granted'





'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=["GET"])
@requires_auth()
def drinks():
    selection = Drink.query.order_by(Drink.id).all()
    
    if selection is None:
        abort(404)    
    
    drinks = [drink.short() for drink in selection]
    if len(drinks) == 0:
        abort(404)



    return jsonify({"success": True,
                    "drinks": drinks
                  })






'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=["GET"])
@requires_auth('get:drinks-detail')
def drinks_detail(payload):
    selection = Drink.query.order_by(Drink.id).all()
    
    if selection is None:
        abort(404)
        
    #drinks = [drink.long() for drink in selection]
    drinks = [drink for drink in selection]
    drinks = [drink.long() for drink in drinks]
    
    if len(drinks) == 0:
        abort(404)
        
    #print('---drinks[0].long()---', drinks[0].long())    
        
        
        
        
    return jsonify({"success": True,
                    "drinks": drinks
                    #"drinks": [drinks[0].long(),drinks[5].long(), drinks[6].long()]
                  })        






'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
# NOTE: payload info from frontend is in drink-form.component.ts file in frontend dir src/app/pages/drink-menu/drink-form
@app.route('/drinks', methods=["POST"])
###@requires_auth('post:drinks')
def post_drink():
    body = request.get_json()
    
    
    print('---body---: ', body)
    
    req_title  = body.get("title", None) 
    req_recipe = body.get("recipe", None)
    
    req_recipe = json.dumps(req_recipe)
    print('---req_recipe---: ', req_recipe)
    
    
    # req_recipe is list and has one dictionary in it
    #req_recipe = str(req_recipe)
    #print('---str req_recipe---: ', req_recipe)

    # has to look like
    # '[{"name": "vodka", "color": "blue", "parts": 1}]'
    # but looked like
    # '[{'name': 'vodka', 'color': 'blue', 'parts': 1}]'
    # json needs double quotes, so we used json dump string to fix it


    #try:    
    drink = Drink(title=req_title, recipe=req_recipe)
    drink.insert()

    # we have to return array with one dictionary
    return jsonify({"success": True,
                    "drinks": drink.long()
                  })     

    #except:





'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:drink_id>", methods=["PATCH"])
@requires_auth('patch:drinks')
#def patch_drink(drink_id):
def patch_drink(payload, drink_id):
    # we had to use 2 arguments above, otherwise it was mixing payload with drink_id together

    print('---drink_id---', drink_id)

    body = request.get_json()
    
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)
          
    #try:    
    if "title" in body:
        drink.title = body.get("title", None)
    if "recipe" in body:
        drink.recipe = json.dumps(body.get("recipe", None))            
    
    drink.update()
    
    # we have to return array with one dictionary
    return jsonify({"success": True,
                    "drinks": list(drink.long())
                  })     

    #except:





'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    body = request.get_json()
    
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)
        
    drink.delete()    
          
    #try:    
    
    # we have to return array with one dictionary
    return jsonify({"success": True,
                    "delete": drink_id
                  })     

    #except:





# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "resource not found"
    }), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "server error"
    }), 500






'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404









'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

# NOTE: AuthError defined in auth.py file




