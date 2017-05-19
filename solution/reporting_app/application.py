"""
Reporting web application
=========================

1. Get a running client to connect to a Market web service. You have two options:
   do it by hand which will require a lot of boiler plate code or generate
   a client using swagger.

2. Allow the web service to be configured with a list of book services

3. Expose a first endpoint which return the general statistics for the
   configured books.

4. Expose a second endpoint which returns the number of trades for a given book.
   Try to make the call as efficient as possible (Hint: use a HEAD call)


"""

import os

from flask import Flask
from flask_restplus import Api

from .views.report import report_ns


def get_api():
    api = Api(
        title='Reporting API', version='1.0',
        description='A simple API exposing reporting capabilities for the'
                    ' market example'
    )

    api.add_namespace(report_ns)

    return api


def create_application(instance_path=None):
    # Create the Flask application
    app = Flask(
        __name__, instance_path=instance_path, instance_relative_config=True
    )

    # Configure the application
    app.config.from_pyfile('application.cfg')

    api = get_api()
    api.init_app(app)

    return app
