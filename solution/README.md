Capstone exercise solution
==========================

The solution contains two web application:

- market_app which is a generic app for a given instrument. The instrument is
  configured using the application.cfg file which must be defined in the
  instance directory. Two example instance directories are provided:
  potato_instance and carrot_instance.
- reporting_app which exposes a reporting endpoint that aggregates the
  statistics for a list of market web services defines in its application.cfg
  file (available in the instance directory). An example is available in
  the reporting_instance directory.

The solution also contains the generated Swagger client for the market web
service. The code under `python_client` has been generated using the Swagger
editor and the `swagger.json` file for the `market_app` webservice. For the
sake of simplicity some files unused in the capstone exercise have been removed
from the generated set of files (tests, tox and git integration).

Running the solution
--------------------

Web service ports have been preset in the application.cfg file (see SERVER_NAME
configuration variable)

1. Start the market web services in two different shells:

   python run_potato.py
   python run_carrot.py

2. Install the swagger client in the Python environment that will run the
   reporting web service:

   cd python_client
   pip install -e .

3. In a third shell, start the reporting web service:

   python run_reporting.py

4. Go to http://127.0.0.1:5002/ and use the swagger documentation interface or
   hit directly http://127.0.0.1:5002/report_ns/reports/stats.

