import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request):
    page = request.args.get("page", 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = Question.query.order_by(Question.id).all()
    formatted_questions = [question.format() for question in questions]
    question_list = formatted_questions[start:end]

    return question_list


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after
    completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS'
        )
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type'
        )

        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        category_dict = {}

        for category in categories:
            category_dict[category.id] = category.type

        return jsonify({
            "success": True,
            "categories": category_dict
        })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three
    pages. Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_paginated_questions():
        # Paginate questions
        question_list = paginate_questions(request)

        # Trigger an error when page argument is out of range
        if question_list == []:
            abort(404)

        current_category = []
        for question in question_list:
            category = Category.query.filter(
                        Category.id == question["category"]).one_or_none()
            current_category.append(category.type)

        # Get dictionary of categories
        categories = Category.query.order_by(Category.id).all()
        category_dict = {}

        for category in categories:
            category_dict[category.id] = category.type

        return jsonify({
            "success": True,
            "questions": question_list,
            "total_questions": len(question_list),
            "categories": category_dict,
            "current_category": current_category
        })

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will
    be removed. This removal will persist in the database and when you refresh
    the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_a_question(question_id):
        question = Question.query.get_or_404(question_id)

        question.delete()

        return jsonify({
            "success": True,
            "deleted": question.format()
        })

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last
    page of the questions list in the "List" tab.
    '''
    @app.route('/create_questions', methods=['POST'])
    def create_new_question():
        try:
            question = request.get_json().get("question", None)
            answer = request.get_json().get("answer", None)
            difficulty = request.get_json().get("difficulty", None)
            category = request.get_json().get("category", None)

            if question is None or answer is None:
                raise ValueError(
                        "question or answer not present in request body"
                      )
                abort(400)

            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
            new_question.insert()

            created_question = Question.query.filter(
                                  Question.question == question).one_or_none()
            created_question = created_question.format()

            return jsonify({
                "success": True,
                "created_question": created_question
            })
        except Exception as e:
            abort(400)

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions', methods=['POST'])
    def get_searched_questions():
        # There is a problem in this section of the code.
        # Try and see if you can solve it later on.
        search_term = request.get_json().get("searchTerm", None)
        questions = Question.query.filter(Question.question.ilike(
                        f"%{search_term}%")).all()
        formatted_questions = [question.format() for question in questions]

        if formatted_questions == []:
            abort(404)

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
            "current_category": None
        })

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_categorized_questions(category_id):
        category = Category.query.filter(Category.id == category_id).\
            one_or_none()

        if category is None:
            abort(404)

        questions = Question.query.filter(Question.category == category_id).\
            order_by(Question.id).all()

        formatted_questions = [question.format() for question in questions]

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
            "current_category": category.type
        })

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
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        # Expecting list containing question ids
        previous_questions = request.get_json().get("previous_questions")

        # Expecting dictionary with category type and id
        # e.g. {"type":"Science", "id":2}
        quiz_category = request.get_json().get("quiz_category")

        if quiz_category["id"] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(
                            Question.category == quiz_category["id"]).all()

        if not questions:
            abort(422)

        # Pick a random question for the user to answer
        import random
        random_question = random.choice(questions)
        game_question = {}
        if random_question.id not in previous_questions:
            game_question = random_question.format()

        # Continue game if there are questions to ask.
        if game_question != {}:
            return jsonify({
                "success": True,
                "question": game_question
            })
        else:
            # End game if there are no more questions to ask
            return jsonify({
                "success": True,
                "question": False
            })

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource cannot be found"
        }), 404

    @app.errorhandler(422)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        })

    return app
