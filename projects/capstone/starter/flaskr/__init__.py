import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from .auth.auth import requires_auth, AuthError

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    setup_db(app)


    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(self):
        actors = [actor.format() for actor in Actor.query.all()]
        result = {
            'success': True,
            'actors': actors
        }

        return jsonify(result)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(self):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        actors = [actor.format() for actor in Actor.query.all()]

        if not name or not age or not gender:
            abort(422)

        try:
            actor = Actor(
                name=name,
                age=age,
                gender=gender)
            Actor.insert(actor)

        except BaseException:
            abort(422)

        return jsonify({
                'success': True,
                'actors': actors
            }), 200


    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(self, actor_id):
        try:
            actor = Actor.query.filter(
                Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor_id
            })

        except BaseException:
            abort(422)

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(self, id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()

            if actor is None:
                abort(404)

            body = request.get_json()
            new_name = body.get('name', None)
            new_age = body.get('age', None)
            new_gender = body.get('gender', None)

            if not new_name or not new_age or not new_gender:
                abort(422)

            actor.name = new_name
            actor.age = new_age
            actor.gender = new_gender
            actor.update()

        except BaseException:
            abort(422)

        actors = [actor.format() for actor in Actor.query.all()]
        result = {
            'success': True,
            'actors': actors
        }

        return jsonify(result)


    @app.route('/movies', methods=['GET'])
    @requires_auth('get:actors')
    def get_movies(self):
        movies = [movie.format() for movie in Movie.query.all()]
        result = {
            'success': True,
            'movies': movies
        }

        return jsonify(result)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(self):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if not title or not release_date:
            abort(422)

        try:
            movie = Movie(
                title=title,
                release_date=release_date)
            Movie.insert(movie)

            return jsonify({
                'success': True
            }), 200

        except BaseException:
            abort(422)


    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(self, movie_id):
        try:
            movie = Movie.query.filter(
                Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie_id
            })

        except BaseException:
            abort(422)


    @app.route('/movies/<movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(self, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()

            if movie is None:
                abort(404)

            body = request.get_json()
            new_title = body.get('title', None)
            new_release_date = body.get('release_date', None)

            if not new_title or not new_release_date:
                abort(422)

            movie.title = new_title
            movie.release_date = new_release_date
            movie.update()

        except BaseException:
            abort(422)

        movies = [movie.format() for movie in Movie.query.all()]
        result = {
            'success': True,
            'movies': movies
        }

        return jsonify(result)


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404


    @app.errorhandler(400)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'auth error'
        }), 400

    @app.errorhandler(403)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'auth error'
        }), 403

    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
        'success': False,
        'error': 403,
        'message': 'unauthorized'
        }), 403
    
    return app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
