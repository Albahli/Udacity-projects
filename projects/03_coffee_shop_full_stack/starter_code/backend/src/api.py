import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import Menu, db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
@requires_auth('get:drinks-detail')
def get_drinks_with_short_info():
    
    drinks = list(map(Drink.short, Drink.query.all()))
    return jsonify({
        "success" : True,
        "drinks" : drinks
    }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_with_long_info(jwt):

    drinks = list(map(Drink.long, Drink.query.all()))
    return jsonify({
        "success" : True,
        "drinks" : drinks
    }), 200


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods =['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    body = dict(request.json)
    print("body: ", body)
    try:
            drink_data = json.loads(request.data.decode('utf-8'))
            drink = Drink(
                title=drink_data['title'],
                recipe=json.dumps(drink_data['recipe'])
                )
            drink.insert()
            drinks = Drink.query.all()
            formatted_drinks = [drink.long() for drink in drinks]
            return jsonify({
                "success" : True,
                "drinks": [formatted_drinks]
            }), 200
       
    except Exception as e:
        print(e)
        abort(422)



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
@app.route('/drinks/<id>', methods =['PATCH'])
@requires_auth('patch:drinks')
def modify_drink(jwt, id):
    body = dict(request.json)
    try:
        if body.get('title') or body.get('recipe'):
            drink_data = json.loads(request.data.decode('utf-8'))
            
            title = drink_data['title'],
            recipe = json.dumps(drink_data['recipe'])
                
            drink = Drink.query.get(id)
            if drink is None:
                abort(404)
            
            drink.title = title
            drink.recipe = recipe

            drink.update()
            drinks = Drink.query.all()
            formatted_drinks = [drink.long() for drink in drinks]
            return jsonify({
                "success" : True,
                "drinks": [formatted_drinks]
            }), 200
        else:
            abort(422)
    except Exception as e:
        print(e)
        abort(422)

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

@app.route('/drinks/<id>', methods =['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    try:
        drink = Drink.query.get(id)
        if drink is None:
            abort(404)
            
        drink.delete()
        return jsonify({
         'success': True,
         'delete': id,
        }), 200
    except Exception as e:
        print(e)
        abort(422)


@app.route('/menus', methods =['POST'])
@requires_auth('post:menu')
def create_menu(jwt):
    body = dict(request.json)
    print("body: ", body)
    try:
            menu_data = json.loads(request.data.decode('utf-8'))
            menu = Menu(title=menu_data['title'])
            menu.insert()
            menus = Menu.query.all()
            formatted_menus = [menu.get_menu_name() for menu in menus]
            return jsonify({
                "success" : True,
                "menus": [formatted_menus]
            }), 200
       
    except Exception as e:
        print(e)
        abort(422)



## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(404)
def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'resource not found',
          }), 404

@app.errorhandler(422)
def unprocessable(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'unprocessable',
          }), 422
          
@app.errorhandler(400)
def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'bad request',
          }), 400

@app.errorhandler(405)
def method_not_found(error):
      return jsonify({
          'success': False,
          'error': 405,
          'message': 'method not allowed',
          }), 405    


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def auth_error(AuthError):
    return jsonify({
          'success': False,
          'error': AuthError.status_code,
          'message': AuthError.error['code'],
          }),    

