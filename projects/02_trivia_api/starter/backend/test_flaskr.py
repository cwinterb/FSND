import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'carmellasouthward@localhost:5432', self.database_name)
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

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_sent_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        question_length = len(data['questions'])
        self.assertEqual(question_length, 0)

    def test_post_question(self):
        quest = 'Test Question'
        answer = 'Test Answer'
        difficulty = 5
        category = 3
        res = self.client().post(
            f'/questions?question={quest}&answer={answer}&difficulty={difficulty}&category={category}')
        question = Question.query.order_by(Question.id.desc()).first().__dict__
        self.assertEqual(question['difficulty'], 5)
        self.assertTrue(question)

    def test_question_search(self):
        search_term = 'country'
        res = self.client().post(f'/questions?search_term={search_term}')
        data = json.loads(res.data)
        self.assertEqual(data['questions'][0]['id'], 11)

    def test_question_search_404(self):
        search_term = 'XXXX'
        res = self.client().post(f'/questions?search_term={search_term}')
        data = json.loads(res.data)
        self.assertEqual((data['error']), 404)

    def test_delete_question(self):
        quest = 'Test Question'
        answer = 'Test Answer'
        difficulty = 5
        category = 3
        self.client().post(
            f'/questions?question={quest}&answer={answer}&difficulty={difficulty}&category={category}')
        question = Question.query.order_by(Question.id.desc()).first().__dict__
        id = question['id']
        self.client().delete(f'/questions/{id}')
        self.assertEqual(Question.query.filter(
            Question.id == id).first(), None)

    def test_delete_404(self):
        id = -1
        res = self.client().delete(f'/questions/{id}')
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertTrue(len(data['categories']) > 0)

    def test_get_categories_404(self):
        Category.query.delete()
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(data['questions'][0]['id'], 20)

    def test_get_questions_by_category_404(self):
        category_id = -1
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)

    def test_quiz(self):
        quiz_category = 1
        prev_questions = 0
        res = self.client().post(
            f'/quizzes?quiz_category={quiz_category}&prev_questions={prev_questions}')
        data = json.loads(res.data)
        self.assertTrue(data['question']['category'] == 1)

    def test_quiz_failure(self):
        prev_questions = None
        res = self.client().post(
            f'/quizzes?quiz_category=1&prev_questions={prev_questions}')
        data = json.loads(res.data)
        self.assertFalse(data['success'])

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
