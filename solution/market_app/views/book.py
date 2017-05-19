from flask import url_for, request, current_app
from flask_restplus import Resource, Namespace, fields, abort

from market_app.models.market import Book
from market_app.models.market_db import SQLStore
from market_app.database import get_connection

book_ns = Namespace('book_ns', description='Book')

book_model = book_ns.model(
    'Book', {
        'instrument': fields.String(required=True),
        'current_time': fields.DateTime(required=True),
        'store': fields.String(required=True)
    }
)

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

statistics_model = book_ns.model(
    'Statistics', {
        'bid_price': fields.Float(required=True),
        'offer_price': fields.Float(required=True),
        'top_offer': fields.Nested(order_model),
        'top_bid': fields.Nested(order_model),
        'spread': fields.Float(required=True),
        'trade_count': fields.Integer(required=True),

    }
)


def get_book():
    connection = get_connection()
    store = SQLStore(connection)
    instrument = current_app.config['INSTRUMENT']
    book = Book(store, instrument)
    book.process_events()
    return book


class BookView(Resource):

    @book_ns.marshal_with(book_model)
    def get(self):
        """ Returns a description of the book."""

        book = get_book()
        return {
            'instrument': book.instrument,
            'current_time': book.current_time,
            'store': repr(book.store)
        }


class BookOrderView(Resource):

    @book_ns.marshal_list_with(order_model)
    def get(self):
        """ Return the list of orders for the book.

        """
        book = get_book()
        return book.orders.values()


@book_ns.doc(params={'trader': 'Trader name'})
class BookTraderOrderView(Resource):

    @book_ns.marshal_list_with(order_model)
    def get(self, trader=None):
        """ Return the list of orders for the book.

        If trader is not None, return the list of orders for the given trader.

        """

        book = get_book()

        if trader is not None:
            return list(book.trader_orders(trader))
        else:
            abort(404)


class BookStatsView(Resource):

    @book_ns.marshal_with(statistics_model)
    def get(self):

        book = get_book()

        return {
            'bid_price': book.bid_price,
            'offer_price': book.offer_price,
            'top_bid': book.top_bid,
            'top_offer': book.top_offer,
            'spread': book.spread,
            'trade_count': len(book.trades)
        }


class BookTradeView(Resource):

    @book_ns.marshal_list_with(trade_model)
    def get(self):

        book = get_book()
        print '-' * 50
        print 'DEBUG ' , book.trades
        return book.trades

@book_ns.route('/book/active_bids')
class BookActiveBidsView(Resource):

    @book_ns.marshal_list_with(order_model)
    def get(self):

        book = get_book()
        # Returning a set() does not serialize properly with Flask-RESTFul
        return list(book.active_bids)

@book_ns.route('/book/active_offers')
class BookActiveOffersView(Resource):

    @book_ns.marshal_list_with(order_model)
    def get(self):

        book = get_book()
        # Returning a set() does not serialize properly with Flask-RESTFul
        return list(book.active_offers)


book_ns.add_resource(BookView, '/book', endpoint='book')
book_ns.add_resource(BookOrderView, '/book/orders', endpoint='book_orders')
book_ns.add_resource(
    BookTraderOrderView, '/book/traders/<trader>/orders',
    endpoint='book_orders_per_trader'
)
book_ns.add_resource(BookStatsView, '/book/stats', endpoint='book_stats')
book_ns.add_resource(BookTradeView, '/book/trades', endpoint='book_trades')



