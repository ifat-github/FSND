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

# db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = list(map(Drink.short, Drink.query.all()))
    result = {
        "success": True,
        "drinks": drinks
    }

    return jsonify(result)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(payload):
    drinks = list(map(Drink.long, Drink.query.all()))
    result = {
        "success": True,
        "drinks": drinks
    }

    return jsonify(result)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    body = request.get_json()
    new_title = body.get('title')
    new_recipe = json.dumps(body.get('recipe'))
    print(new_recipe, new_title)

    if not new_title or not new_recipe:
        abort(422)

    try:
        drink = Drink(
            title=new_title,
            recipe=new_recipe)
        Drink.insert(drink)

    except BaseException:
        abort(422)

    return jsonify({
        'success': True,
        'drinks': drink.long()
    }), 200


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(payload, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        if drink is None:
            abort(404)

        body = request.get_json()
        new_title = body.get('title', None)
        new_recipe = json.dumps(body.get('recipe'))

        if not new_title or not new_recipe:
            abort(422)

        drink.title = new_title
        drink.recipe = new_recipe
        drink.update()

    except BaseException:
        abort(422)

    drinks = Drink.query.filter(Drink.id == id).one_or_none().long()
    result = {
        "success": True,
        "drinks": drinks
    }

    return jsonify(result)


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            'success': True,
            'delete': id
        })

    except BaseException:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


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
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "auth error"
    }), 400
