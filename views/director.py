from flask import request
from flask_restx import Resource, Namespace
from models import Director, directors_schema, director_schema
from setup_db import db




director_ns = Namespace('')


@director_ns.route('/directors')
class directorsView(Resource):
    def get(self):
        query = Director.query
        return directors_schema.dump(query.all()), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@director_ns.route('/directors/<int:uid>')
class directorView(Resource):

    def get(self, uid: int):  # Получение данных
        try:
            director = Director.query.get(uid)
            return director_schema.dump(director), 200
        except Exception as e:
            return "", 404

    def put(self, uid):  # Замена данных
        director = Director.query.get(uid)
        req_json = request.json
        director.name = req_json.get("name")

        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        director = Director.query.get(uid)
        db.session.delete(director)
        db.session.commit()
        return "", 204