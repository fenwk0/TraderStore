''' Entry point to start the Reporting web application

To start the web application::

    python run_report.py

'''

import os

from reporting_app.application import create_application


if __name__ == '__main__':

    app = create_application(os.path.abspath('reporting_instance'))

    app.run(debug=True)
