from flask import Flask, request
from flask_restx import Resource, Namespace
from models import Movie, movies_schema, movie_schema
from setup_db import db





movie_ns = Namespace('')

@movie_ns.route('/movies')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        year = request.args.get('year')
        query = Movie.query
        if director_id:
            query = query.filter(Movie.director_id == director_id)
        if genre_id:
            query = query.filter(Movie.genre_id == genre_id)
        if year:
            query = query.filter(Movie.year == year)
        return movies_schema.dump(query.all()), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201



@movie_ns.route('/movies/<int:uid>')
class MovieView(Resource):

    def get(self, uid: int):    # Получение данных
        try:
            movie = Movie.query.get(uid)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return "", 404

    def put(self, uid):  # Замена данных
        movie = Movie.query.get(uid)
        req_json = request.json
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        movie = Movie.query.get(uid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204
