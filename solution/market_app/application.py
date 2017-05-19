"""
Market web application
======================

Expose the Market model as a web service

"""

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


def create_application(instance_path=None):
    # Create the Flask application
    app = Flask(
        __name__, instance_path=instance_path, instance_relative_config=True
    )

    # Configure the application
    app.config.from_object('market_app.default_settings')
    app.config.from_pyfile('application.cfg')

    api = get_api()
    api.init_app(app)

    return app

if __name__ == '__main__':
    import os
    app = create_application(os.path.abspath('potato_instance'))
    app.run()
