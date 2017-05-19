from flask import current_app
from flask_restplus import Namespace, Resource, fields

from market_app.database import get_connection
from market_app.models.market_db import SQLStore
from market_app.models.market import Book, Order, Trade
from market_app.views.store import BaseStore

book_ns = Namespace('book_ns')

# Define your Flask-RESTplus models here

book_ns = Namespace('book_ns', description='Book related operations')

book_model = book_ns.model(
    'Book', {
        'instrument': fields.String(required=True),
        'current_time': fields.DateTime(required=True),
        'store': fields.String(required=True)
    }
)


class BaseBookResource(Resource):
    @property
    def book(self):
        connection = get_connection()
        store = SQLStore(connection)
        book = Book(store, current_app.config['INSTRUMENT'])
        book.process_events()
        return book


class BookResource(BaseBookResource):
    # /book endpoint
    @book_ns.marshal_list_with(book_model)
    def get(self):
        """ Return the book instrument; the type of commodity the book contains and the store its connected to """

        results = self.book

        return results

    @book_ns.expect(book_model, validate=True)
    def post(self):
        """ Create a new order. """

        # payload = request.json


        # order_id = self.store.create_order(**payload)
        # location = url_for('order', order_id=order_id)
        # return 'Order created', 201, {'Location': location}


order_model = book_ns.model(
    'BookOrder', {
        'id': fields.String(required=False),
        'trader': fields.String(required=True),
        'order_type': fields.String(enum=['limit', 'market'], required=True),
        'action': fields.String(enum=['sell', 'buy'], required=True),
        'price': fields.Float(required=True),
        'expiry': fields.DateTime(required=False),
        'timestamp': fields.DateTime(required=False),
        'traded': fields.Boolean(),
        'cancelled': fields.Boolean(),
        'expired': fields.Boolean(),
        'active': fields.Boolean(),

    }
)

trade_model = book_ns.model(
    'Trade', {
        'id': fields.String(required=False),
        'bid': fields.Nested(order_model),
        'offer': fields.Nested(order_model),
        'price': fields.Float(required=True),
        'timestamp': fields.DateTime(required=False),

    }
)


class TradeResource(BaseBookResource):
    # /book/trades endpoint
    @book_ns.marshal_list_with(trade_model)
    def get(self):
        """ Return the trades contained in a book """

        results = self.book.trades

        return results


# /book endpoint

# /book/trades endpoint

# /book/trader/<trader_id>/orders endpoint

# /book/active_offers endpoint

# /book/active_bids endpoint

# /book/stats endpoint

book_ns.add_resource(BookResource, '/book', endpoint='book')
book_ns.add_resource(TradeResource, '/trades', endpoint='trades')
