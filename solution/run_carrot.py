''' Entry point to start the Carrot Market web application

To start the web application::

    python run_carrot.py

'''

import os

from market_app.application import create_application
from market_app.database import init_database


def init_db(application):
    """ Initialize the store database with some orders. """

    with application.app_context():
        if not os.path.exists(application.instance_path):
            os.makedirs(application.instance_path)
        init_database()


if __name__ == '__main__':

    app = create_application(os.path.abspath('carrot_instance'))

    init_db(app)
    app.run(debug=True)
