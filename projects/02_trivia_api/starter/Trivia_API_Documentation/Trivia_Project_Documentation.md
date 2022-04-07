# The Trivia Game

This project is a game. Users of this application will be able to find a list of questions and their answers, search for questions based on their category (e.g. Science), add and delete questions. They will also be able to play a game where random questions are displayed depending on category and they have to answer them.

All backend code within this project follows PEP8 style guidelines.


## Getting Started

### Pre-requisites and Local Development
Developers should have python or python3, node and pip installed on their local machines.

### Backend

For the backend, navigate to the backend folder and run ```pip install -r requirements.txt```. All packages are included in the requirements file.

### Setting up the Database

With your Postgres server running, in your terminal, run the following commands:
```
createdb trivia
psql trivia < trivia.psql
```

To run the application, navigate to the project directory and enter the following commands in your terminal:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
python -m flask run --reload
```

These commands put the application into development and direct the application to the ```__init__.py``` file in the flaskr directory. They will also open a debugger in your terminal which will reload every time changes are made to the application. The application will be run on http://127.0.0.1:5000.

### Frontend

To begin the frontend server, navigate to the frontend folder. If you have not already done so, run ```npm install//```. After doing this, you can run ```npm start``` to start the frontend server.


### Tests

To run tests, navigate to the backend folder and run the following commands in your terminal:
```
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


## API Reference

### Getting Started

Base URL: Since this application is not hosted locally, there is no base URL. The backend is hosted on http://127.0.0.1:5000.

There is no authentication for this API.

### Error Handling

Errors are returned in the following JSON format:
```
{
  "success" : False,
  "error" : 500,
  "message" : "Internal server error"
   }
```

The API handles the following errors:
* 500: Internal server error
* 400: Bad request
* 404: Resource cannot be found
* 422: Unprocessable


### Endpoints

#### GET /categories
  * Fetches: a dictionary of the categories in which the keys are the ids and the values are the corresponding string of the category as well as a success value.
  * Request Arguments: None
Sample Request: ```curl http://127.0.0.1:5000/categories```.
The expected response should be:
```
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
```

#### GET /questions
  * Fetches: a list of question objects, success value, total number of questions, a dictionary of categories and the current category of questions. Results are paginated.
  * Request Arguments: The "page" request argument gets each page of results.
Sample Request: ```curl http://127.0.0.1:5000/questions?page=2```.
The expected response should be:
```
"categories": {
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
},
"current_category": [
        "Geography",
        "Art",
        "Art",
        "Art",
        "Art",
        "Science",
        "Science",
        "Science",
        "History"
    ],
"questions": [
  {
    "answer": "Agra",
    "category": 3,
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
  },
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
  },
  {
    "answer": "One",
    "category": 2,
    "difficulty": 4,
    "id": 18,
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  },
  {
    "answer": "Jackson Pollock",
    "category": 2,
    "difficulty": 2,
    "id": 19,
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  },
  {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  {
    "answer": "Scarab",
    "category": 4,
    "difficulty": 4,
    "id": 23,
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  }
],
"success": true,
"total_questions": 9
}
```

#### POST /create_questions
  * Creates and post a question object to the database.
  * Request Arguments: A JSON request body is needed with question, answer, difficulty and category keys with their values.
  * Returns a JSON formatted response containing a success value and the created question object if successful.
Sample Request: ```curl -X POST http://127.0.0.1:5000/create_questions -H 'Content-Type : application/json' -d '{"question":"What is the capital of Britain?", "answer":"London", "difficulty":1, "category":4}'```.
The expected response should be:
```
{
  "success": True,
  "created_question": {
    "answer": "London",
    "category": 4,
    "difficulty": 1,
    "id": 25,
    "question": "What is the capital of Britain?"
  }
}
```

#### POST /questions
  * Fetches a list question objects, a success value, total number of questions and the current category of questions based on the similarity of questions to the string value of the key "searchTerm" in the request body.
  * Request Arguments: A JSON request body is required with a searchTerm key and its corresponding string value.
Sample request:```curl -X POST http://127.0.0.1:5000/questions -H 'Content-Type : application/json' -d '{"searchTerm" : "th"}'```.
The expected response will be:
```
{
    "current_category": null,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
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
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        }
    ],
    "success": true,
    "total_questions": 12
}
```

#### GET /categories/id/questions
  * Fetches a list question objects, a success value, number of questions and the current category of questions based on the category of questions specified in the endpoint.
  * Request Arguments: None.
Sample request: ```curl -X GET http://127.0.0.1:5000/categories/2/questions```.
The expected response should be:
```
{
    "current_category": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true,
    "total_questions": 4
}
```

#### DELETE /questions/5
  * Deletes a question with the specified id if it exists.
  * Returns a JSON formatted containing a success value and the deleted question.
Sample request: ```curl -X DELETE http://127.0.0.1:5000/questions/5```.
The expected response should be:
```
{
    "deleted": {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    "success": true
}
```

#### POST /quizzes
  * Request Arguments: A JSON formatted list containing the ids of previous questions and JSON formatted dictionary containing the type and id of the category of questions being chosen from.
  * Fetches a random question based on category, and whether it is present in provided previous questions list or not.
Sample Request: ```curl -X POST http://127.0.0.1:5000/quizzes -H 'Content-Type : application/json' -d '{"quiz_category":{"type": "History", "id": 4}, "previous_questions":[2, 5]}'```.
The expected response should be:
```
{
    "question": {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
    },
    "success": true
}
```


## Deployment N/A

## Authors
Robert Kwami (Niovial)
