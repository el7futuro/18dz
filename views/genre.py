from flask import request
from flask_restx import Resource, Namespace
from models import genres_schema, Genre, genre_schema
from setup_db import db




genre_ns = Namespace('')


@genre_ns.route('/genres')
class genresView(Resource):
    def get(self):
        query = Genre.query
        return genres_schema.dump(query.all()), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genre_ns.route('/genres/<int:uid>')
class genreView(Resource):

    def get(self, uid: int):  # Получение данных
        try:
            genre = Genre.query.get(uid)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return "", 404

    def put(self, uid):  # Замена данных
        genre = Genre.query.get(uid)
        req_json = request.json
        genre.name = req_json.get("name")

        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        genre = Genre.query.get(uid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204
