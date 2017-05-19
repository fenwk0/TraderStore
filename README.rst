Advanced Python capstone exercise
==================================

The goal of the capstone exercise is to build two inter-connected micro-web
services using Flask, Flask-RESTPlus and Swagger.

Starting from the last Flask-RestPlus exercise (ex_5_swaggger_integration),
the capstone exercise will go through the steps of

1. Finish exposing the market model as a web service
2. Generate swagger client based on the swagger API of your market web service.
3. Build a second web service that will expose one report with statistics based
   on a list of market web services [ BONUS ]

Market web service
------------------

- Expose endpoints for the Book (market_app.model.market.Book) within a book
  namespace (e.g. named book_ns). Make sure Order and Trade object serialize
  properly using Flask-RESTFul.

  Required endpoints are:

  - /book_ns/book: returns the store instrument, current time and info about the
    SQLStore
  - /book_ns/book/trades: returns the list of trades
  - /book_ns/book/trades/<trader_id>/orders: return all the orders for the given
    trader
  - /book_ns/book/activate_bids: returns all currently active bid orders
  - /book_ns/book/activate_offers: return all currently active offer orders

- Add a endpoint returning statistics about the book (top_bid, top_offer,
  bid_price, offer_price, count of trades) under /books_ns/book/stats

  Hint: use REST principles and return links to the top orders

- Update the configuration of the web service to define the name of the
  instrument managed by the Book. This change will allow you to run two web
  services with different instruments.

  Hint: http://flask.pocoo.org/docs/0.11/config/


Market client
-------------

- Using the Swagger editor, generate a client for the market web service.


 Hint: You can generate a swagger.json file using for the market_app web
 service using::

        python generate_swagger.py

 Hint: Use editor.swagger.io to generate the client

- Once generated, extract the archive and install the swagger_client into the
  Python environment that will run the reporting web service::

    cd python_client
    pip install -e .


- Test the swagger client and make sure you can query a market service

  Hint: The swagger client connects by default to port 80 on localhost. To
  customize the host to connect to, you can use the ApiClient (see
  `swagger_client.api_client.ApiClient`.

Reporting web service
---------------------

Build a reporting web service that takes a list of Market web service in its
configuration and expose a endpoint which returns the statistics for all the
connected markets and the average statistics for all the markets.

The reporting web service should use the generated Market swagger client.
