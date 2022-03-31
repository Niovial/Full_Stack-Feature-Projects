import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import db_user, db_password


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(db_user, db_password,
                            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    def test_get_all_available_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])


    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_404_when_page_not_found(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)
        self.assertEqual(data["message"], "Resource cannot be found")


    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    def test_404_when_category_cannot_be_found(self):
        res = self.client().get('/categories/50/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Resource cannot be found")

    def test_get_searched_questions(self):
        res = self.client().post('/questions', json={'searchTerm' : "th"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_404_when_question_not_found(self):
        res = self.client().post('/questions', json={'searchTerm' : "jnfjnjen"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Resource cannot be found")


    def test_get_quiz_questions(self):
        res = self.client().post('/quizzes', json={
                "quiz_category":{"type": "History", "id": 4},
                "previous_questions":[2, 5]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        #self.assertTrue(data["question"])

    def test_when_no_more_questions(self):
        res = self.client().post('/quizzes', json={
                "quiz_category":{"type": "History", "id": 6},
                "previous_questions":[10, 11]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertFalse(data["question"])

    def test_422_when_no_questions_returned_on_query(self):
        res = self.client().post('/quizzes', json={"quiz_category":
                            {"type": "Unknown", "id": 600}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "Unprocessable")


    def test_create_new_question(self):
        res = self.client().post('/create_questions', json={
            "question":"What is the capital of Britain?",
            "answer":"London",
            "difficulty":1,
            "category":4
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created_question"])

    def test_400_if_wrong_request_body_keys(self):
        res = self.client().post('/create_questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 400)
        self.assertEqual(data["message"], "Bad request")


    def test_delete_a_question(self):
        res = self.client().delete('/questions/23')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])

    def test_404_when_question_unavailable(self):
        res = self.client().delete('/questions/2300')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Resource cannot found")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
