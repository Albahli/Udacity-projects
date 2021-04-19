# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

# API Documentation

The end point `/categories` will return a list of categories, the total number of categories and a success message.
``` http://127.0.0.1:5000/categories
```

The end point `/questions` will return a list of type Question, list of categories, the total number of questions and a success message.
```
http://127.0.0.1:5000/questions
```
-  

## Endpoints
One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

# API Documentation
## Models
### Category
- The Category model represents:
  - id
  - type

 Each `id` is fixed to a specific `type`, so for example:
```
{
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports",
}, 
```
### Question

- The question model represents:
  - id
  - question
  - answer
  - category
  - difficulty
- The question belongs to specific category and the difficulty is an integer from 1 to 5 (The lower the easier)

```
{
      'id': 1, // random generated
      'question': 'Which country won the first ever soccer World Cup in 1930?',
      'answer': 'Uruguay',
      'category': 6, // belong to Sports category
      'difficulty': 4
}
```


## `/categories`

### Methods:
- GET

#### GET
This end point return:
- List of categories.
- Total number of categories.
- A message whether if the operation is successful or not. 

Example calling the endpoint:
``` 
http://127.0.0.1:5000/categories
```
will return:
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}
```

## `/questions`

### Methods:
- GET
- POST
- DELETE

#### GET
This end point will return:
- List of categories.
- List consisting of 10 elements of type Question.
- Total number of questions.
- A message whether if the operation is successful or not.

Example calling the endpoint:
```
http://127.0.0.1:5000/questions
```
will return:
```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
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

    },
   // .
   // .
   // .
   // .
   //.
   // .
   // .
   // 10th Question
   ],
  "success": true, 
  "total_questions": 3
}
```

You can also get the second 10 questions by doing the following:

```
http://127.0.0.1:5000/questions?page=2
```

#### POST

Calling this endpoint with POST method will create a new question.

For example, passing new question data in the body:
```
{
    question: 'When the first world war happened?',
    answer: 'July 28, 1914',
    difficulty: 2,
    category: 4
}
```
After that, calling this endpoint:
```
http://127.0.0.1:5000/questions
```


This will return:
- List consisting of 10 elements of type Question.
- The new created question ID.
- Total number of questions.
- A message whether if it is success or not.

Example calling the endpoint:

```
{
  "success": true
  "created_id": 4
  "questions": [
    {
      "answer": "July 28, 1914",
      "category": 4
      "difficulty": 2,
      "question": "When the first world war happened?",
    }, 
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

    },
   // .
   // .
   // .
   // .
   //.
   // .
   // .
   // 10th Question
  "total_questions": 26
}
```
## `/questions/<int:question_id>`

### Methods:
- DELETE

#### DELETE

Calling this endpoint with DELETE method will basically delete a question.

In order to delete a questions, the question ID must be known.

This how the endpoint should be like:
```
http://127.0.0.1:5000/questions/<int:question_id>
```
Example:
```
http://127.0.0.1:5000/questions/4
```
This will return:
- The deleted question ID.
- A message whether if it is success or not.

Example calling the endpoint
```
{
   'success': True,
   'deleted_question_id': 4,
}
```

## `/questions/search`

### Methods:
- POST

#### POST
This end point takes query parameter named `term` and returns:
- Returns a list of questions for whom the search term is a substring of the question.
- A message whether if the operation is successful or not. 

Example calling the endpoint :
``` 
http://127.0.0.1:5000/questions/search?term=tom
```
This will return:
```
{
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "success": true
}
```

## `/categories/<int:category>/questions`

### Methods:
- GET

#### GET
This end point takes an integer which represents the category number and returns:
- A list of questions within that category.
- A message whether if the operation is successful or not. 

Example calling the endpoint :
``` 
http://127.0.0.1:5000/categories/2/questions
```
this will return:
```
{
    "questions": [
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true
}
```


## `/quizzes`

### Methods:
- POST

#### POST
This endpoint takes two query parameters `category` as integer and `prevQuestions` as list of question IDs.
Based on those two parameters, the end point will return one random question based on `category` and will exclude any questions in the `prevQuestions` list.

For example, calling this endpoint:
```
http://127.0.0.1:5000/quizzes?category=1&prevQuestions=
```
this will return:
```
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
```

Example, calling this endpoint:
```
http://127.0.0.1:5000/quizzes?category=1&prevQuestions=20,33
```
this will return a question not in the `prevQuestions=20,33`:
```
{
    "question": {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
}
```

Example, calling this endpoint with `category=0` will be based on all categories:
```
http://127.0.0.1:5000/quizzes?category=0&prevQuestions=20,33
```
this will return a question not in the `prevQuestions=20,33` and from another category:
```
{
    "question": {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```