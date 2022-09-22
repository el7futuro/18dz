# основной файл приложения. здесь конфигурируется фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
# этот файл часто является точкой входа в приложение

# Пример

from flask import Flask
from flask_restx import Api

from config import Config
from models import Movie, Genre, Director
from setup_db import db
# from views.movie.view import movie_ns
# from views.reviews import review_ns

#функция создания основного объекта app
from views.director import director_ns
from views.genre import genre_ns
from views.movie import movie_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


#функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(director_ns)
    create_data(app, db)


#функция
def create_data(app, db):
    with app.app_context():
        db.create_all()
        m1 = Movie(id=1, title='Iron man', description='bla bla bla', trailer='1', year=2000, rating=10.0, genre_id=1, director_id=1)
        m2 = Movie(id=2, title='Iron man 2', description='bla bla 2', trailer='2', year=2010, rating=9.0, genre_id=1, director_id=1)
        g1 = Genre(id=1, name='SciFi')
        g2 = Genre(id=2, name='Horror')
        d1 = Director(id=1, name='Nikita Mihalkov')
        d2 = Director(id=2, name='Kventin Tarantino')

        with db.session.begin():
            db.session.add_all([m1, m2])
            db.session.add_all([g1, g2])
            db.session.add_all([d1, d2])

app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)



