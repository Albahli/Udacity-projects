import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy.sql.sqltypes import String
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions
  

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={"r*/api/*": {"origins": "*"}},send_wildcard=True )

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
      response.headers.add('Access-Control-Allow-Origin', '*')
      return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    
    selection = Category.query.all()
    categories = {category.id : category.type for category in selection}   
    
    if len(selection) == 0:
            abort(404)
    else:
        return jsonify({
        'success': True,
        'categories': categories,
        'total_categories': len(Category.query.all())
        }) 

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    selection = Question.query.all()
    categories_selection = Category.query.all()

    current_questions = paginate_questions(request, selection)

    current_categories = [category.type for category in categories_selection]
    if len(current_questions) == 0:
        abort(404)
        
    else:
        return jsonify({
        'success': True,
        'questions': current_questions,
        'categories': current_categories,
        'total_questions': len(Question.query.all()),
        'current_category': None
        })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
            
        question.delete()
        return jsonify({
         'success': True,
         'deleted_question_id': question.id,
        })
    except:
        abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    try:

        if body.get('question') and body.get('answer'):
            
            question = Question(
            question = body.get('question', None),
            answer = body.get('answer', None),
            category = body.get('category', None),
            difficulty = body.get('difficulty', 1),
            )
            question.insert()
            
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            
            return jsonify({
            'success': True,
            'created_id': question.id,
            'questions': current_questions,
            'total_questions': len(Question.query.all())
            })
        else:
           abort(422)
    except:
        abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    term = request.args.get('term', '')
    try:
        selection = Question.query.filter(Question.question.ilike("%" + term + "%")).order_by(Question.id).all()
        #current_questions = paginate_questions(request, selection)
        questions = [question.format() for question in selection]
        return jsonify({
            'success': True,
            'questions': questions,
            })
    except:
        print(sys.exc_info())
        abort(422)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category>/questions')
  def get_question_by_category(category):
    try:
        selection = Question.query.filter(Question.category == category+1)
        questions = [question.format() for question in selection]
        return jsonify({
            'success': True,
            'questions': questions,
            })
    except:
        abort(404)

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
  @app.route('/quizzes', methods=['POST', 'GET'])
  def play_quiz():
      
    try:
        body = request.get_json()

        category = request.args.get('category')
        previous_questions_args = request.args.get('prevQuestions', [])
        
        formatted_previous_questions = previous_questions_args.split(",")        
        quiz_question = None

        if previous_questions_args:
            
            if category == '0':
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category.in_(category)).all() #if previous_questions is None else Question.query.filter(~Question.id.in_(previous_questions), Question.category.in_(category)).all()
            
            
            quiz_questions = []
            
            for question in questions:
                quiz_questions.append(str(question.id))

            for previous_question in formatted_previous_questions:
                if previous_question in quiz_questions:
                    print('removing question')
                    quiz_questions.remove(previous_question)
                   
            print(list(dict.fromkeys(quiz_questions)))
            if quiz_questions:
                quiz_question_id = random.choice(list(dict.fromkeys(quiz_questions)))
                quiz_question = Question.query.get(quiz_question_id)
        
        else:
            print('First question case')
            if category == '0':
                quiz_question = Question.query.first()
            else:
                quiz_question = Question.query.filter(Question.category.in_(category)).first()
       
        return jsonify({
            'success': True,
            'question': quiz_question.format() if quiz_question else None,
            })
    except:
        print(sys.exc_info())
        abort(404) 
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
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

  return app

    