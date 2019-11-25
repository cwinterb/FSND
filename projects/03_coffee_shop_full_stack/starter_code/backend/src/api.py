import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# ROUTES
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    drinks_short = [drink.short() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks_short,
        'code': 200
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def new_drink(token):
    req_data = request.get_json()
    title = req_data.get('title', None)
    recipe = req_data.get('recipe', None)
    drink = Drink(title=title, recipe=json.dumps(recipe))
    drink.insert()
    drink = drink.long()
    return jsonify({
        'success': True,
        'drink': drink
    })


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(token):
    drinks = Drink.query.all()
    drinks_long = [drink.long() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks_long,
        'code': 200
    })


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(token, id):
    req_data = request.get_json()
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        drink.title = req_data.get('title', None)
        drink.recipe = json.dumps(req_data.get('recipe', None))
        drink.update()
        drink_long = [drink.long()]
    except DatabaseError:
        abort(404)
    finally:
        return jsonify({
            'success': True,
            'drinks': drink_long,
            'code': 200
        })


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)
    drink.delete()
    return jsonify({
        'success': True,
        'delete': id
    })

# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error":  404,
        "message": "not found"
    }), 404


@app.errorhandler(403)
def not_authorized(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "not authorized"
    }), 403