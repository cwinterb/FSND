from models import setup_db, Question, Category, db
import random
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import *
import os
from flask import (Flask, request,
                   abort, jsonify, redirect,
                   url_for, json)


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
            if len(questions) == 0:
                abort(404)
            categories = Category.query.all()
            if len(categories) == 0:
                abort(404)
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
        if (request.method == 'POST'
                and request.args.get('search_term') is not None):
            search_term = request.args.get('search_term')
            response = Question.query.filter(
                Question.question.contains(search_term)).all()
            if len(response) == 0:
                abort(404)
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
                    question=question,
                    answer=answer,
                    difficulty=difficulty,
                    category=category)
                Question.insert(new_question)
            except DatabaseError:
                db.session.rollback()
                abort(422)
            finally:
                db.session.close()
                return jsonify({
                    'question': question,
                    'answer': answer,
                    'difficulty': difficulty,
                    'category': category})

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get_or_404(question_id)
            Question.delete(question)
        except DatabaseError:
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
            if len(categories) == 0:
                abort(404)
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
        query = Question.query.filter_by(category=str(category_id)).all()
        if len(query) == 0:
            abort(404)
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
        previous_questions = request.args.get('prev_questions').split(',')
        try:
            prev_questions = [int(q) for q in previous_questions]
        except typeError:
            abort(500)
            return jsonify({'success': False})
        if int(quiz_category) > 0:
            cat_questions = Question.query.filter(
                Question.category == quiz_category)
        else:
            cat_questions = Question.query
        next_question = (cat_questions.filter(
            ~ Question.id.in_(previous_questions)).first())
        if next_question is None:
            current_question = False
        else:
            current_question = next_question.format()
            prev_questions.append(current_question['id'])
        return jsonify({
            'question': current_question,
            'previous_questions': prev_questions
        })

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server error"
        }), 500

    return app
