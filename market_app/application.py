"""
Market web application
======================

Expose the Market model as a web service

"""

from os.path import exists, join

from flask import Flask
from flask_restplus import Api

from .views.store import store_ns
from .views.book import book_ns


def get_api():
    api = Api(
        title='Market API', version='1.0.1',
        description='A simple application exposing the Market to the web'
    )

    api.add_namespace(store_ns)
    api.add_namespace(book_ns)

    return api


def create_application(instance_directory=None):

    if instance_directory is not None and not exists(instance_directory):
        raise RuntimeError('Instance directory does not exist')

    # Create the Flask application
    app = Flask(__name__, instance_path=instance_directory)

    # Configure the application
    app.config.update(
        dict(
            DATABASE=join(app.instance_path, 'market.db'),
            INSTRUMENT='potatoes',
            SECRET_KEY='development key',
        )
    )

    api = get_api()
    api.init_app(app)

    return app

if __name__ == '__main__':

    app = create_application()
    app.run()
