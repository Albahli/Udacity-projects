import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flaskr import  __init__ , create_app
from models import setup_db, Question, DB_PATH


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:4279@localhost:5432/trivia"
        self.new_question = {
            'question':'question test ',
            'answer' : 'answer test',
            'category' : 1,
            'difficulty' : 2}
        setup_db(self.app)

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
# Getting paginated questions (SUCCESS)   
    def test_get_paginated_questions(self):
        """Test _____________ """
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

# Getting paginated questions (FAILED)      
    def test_404_sent_request_beyond_valid_page(self):
        """Test _____________ """
        res = self.client().get('/questions?page=1000') # Page number 1000 dose not exist
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
 # Delete Question (SUCCESS)         
    def test_delete_question(self):
        """Test _____________ """
        res = self.client().delete('/questions/18')
        data = json.loads(res.data)
        
        question = Question.query.filter(Question.id == 18).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_question_id'], 18)
        self.assertEqual(question, None)

# Delete Question (FAILED)
    def test_422_if_question_does_not_exist(self):
        # Question with id = 1000 does not exist
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Getting Categories (SUCEESS)
    def test_get_categories(self):
        """Test _____________ """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

# Getting Categories (FAILED)
    def test_405_get_categories(self):
        """Test _____________ """
        res = self.client().patch('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

# Create Question (SUCCESS)

    def test_create_question(self):
        """Test _____________ """
        res = self.client().post('/questions', json= self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_id'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

# Create Question (FAILED)

    def test_405_if_question_creation_not_allowed(self):
        """Test _____________ """
        res = self.client().post('/questions/45', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

# Search Question (SUCCESS)

    def test_search_question(self):
        """Test _____________ """
        res = self.client().post('/questions/search?term=tom')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

# Search Question (FALSE)

    def test_405_search_question(self):
        """Test _____________ """
        res = self.client().get('/questions/search?term=ThereIsNoQuestionWithThatTerm')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

# Get Questions By Category (SUCCESS)

    def test_get_questions_by_catgeory(self):
        """Test _____________ """
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

# Get Questions By Category (FAILED)

    def test_405_get_questions_by_catgeory(self):
        """Test _____________ """
        res = self.client().post('/categories/77/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')


# Play Quiz (SUCCESS)
    def test_play_quiz(self):
        """Test _____________ """
        res = self.client().post('/quizzes?category=1&prevQuestions=')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

# Play Quiz (FAILED)
    def test_405_play_quiz(self):
        """Test _____________ """
        res = self.client().patch('/quizzes')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
