import os
from models import setup_db
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)

  return app

APP = create_app()

@APP.route('/')
def index():
  return 'Hello'

@APP.route('/hi')
def index():
  return 'hi'

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)