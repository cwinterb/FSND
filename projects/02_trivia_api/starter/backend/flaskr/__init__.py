import os
from flask import Flask, request, abort, jsonify, redirect, url_for, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/questions', methods=['GET', 'POST'])
    def get_questions():
        if request.method == 'GET':
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            questions = Question.query.all()
            categories = Category.query.all()
            formatted_questions = [question.format() for question in questions]
            formatted_categories = {}
            for category in categories:
                formatted_categories[category.__dict__[
                    'id']] = category.__dict__['type']
            return jsonify({
                'success': True,
                'questions': formatted_questions[start: end],
                'total_questions': len(formatted_questions),
                'categories': formatted_categories
            })
        if (request.method == 'POST' and request.args.get('search_term') is not None):
            search_term = request.args.get('search_term')
            response = Question.query.filter(
                Question.question.contains(search_term)).all()
            response_formatted = [question.format() for question in response]
            total_questions = len(response)
            current_category = []
            for question in response_formatted:
                current_category.append(question['category'])
            return jsonify({
                'success': True,
                'questions': response_formatted,
                'total_questions': total_questions,
                'current_cateogry': current_category
            })

        if request.method == 'POST':
            try:
                question = request.args.get('question')
                answer = request.args.get('answer')
                difficulty = request.args.get('difficulty')
                category = request.args.get('category')
                new_question = Question(
                    question=question, answer=answer, difficulty=difficulty, category=category)
                db.session.add(new_question)
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close()
                return jsonify({
                    'success': True
                })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get_or_404(question_id)
            db.session.delete(question)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
            return jsonify({
                'success': True
            })

    @app.route('/categories', methods=['GET'])
    def get_categories():
        if request.method == 'GET':
            categories = Category.query.all()
            formatted_categories = {}
            for category in categories:
                formatted_categories[category.__dict__[
                    'id']] = category.__dict__['type']
            return jsonify({
                'success': True,
                'categories': formatted_categories
            })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        query = Question.query.filter_by(category=category_id).all()
        response = [question.format() for question in query]
        total_questions = len(response)
        return jsonify({
            'success': True,
            'questions': response,
            'total_questions': total_questions,
            'current_category': category_id})

    @app.route('/quizzes', methods=["POST"])
    def quiz():
        quiz_category = request.args.get('quiz_category')
        previous_questions = request.args.get('prev_questions')
        print(previous_questions)
        category_length = len(Question.query.filter_by(
            category=quiz_category).all())
        rand = random.randint(1, category_length)
        # rand_question = Question.query.filter(
        #     Question.category == quiz_category).all()[rand - 1].format()
        cat_questions = Question.query.filter(
            Question.category == quiz_category)
        rand_question = cat_questions.filter(
            Question.id not in previous_questions).all().random().format()
        print(rand_question)
        previous_questions.join(rand_question)
        print(previous_questions)
        return jsonify({
            'question': rand_question,
            'previous_questions': previous_questions
        })
    return app


'''
    # @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''

'''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''

'''
      @DONE:
      Create an endpoint to handle GET requests
      for all available categories.
      '''

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

'''
  @DONE:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

'''
  @DONE:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

'''
  @DONE:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

'''
  @DONE:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

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

'''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
