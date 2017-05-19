import sqlite3
import tempfile
import time
import unittest

from market_app.models.market_db import SQLStore
from market_app.models.market import Book


class BookTestCase(unittest.TestCase):

    def setUp(self):

        self.db_fd, db_file = tempfile.mkstemp()
        db_connection = sqlite3.connect(
            db_file,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        # Use an optimized Row factory which allows us to access row content
        # by index or keys
        db_connection.row_factory = sqlite3.Row
        self.store = SQLStore(db_connection)

        self.book = Book(self.store)

    def test_book_create_trade(self):

        self.store.create_order('Geno', 'limit', 'buy', 10.80, None)
        self.store.create_order('Joe', 'limit', 'sell', 10.50, None)

        self.book.process_events()

        self.assertEqual(len(self.book.active_bids), 0)
        self.assertEqual(len(self.book.active_offers), 0)
        self.assertEqual(len(self.book.trades), 1)

    def test_book_has_active_bids(self):

        self.store.create_order('Geno', 'limit', 'buy', 10.90, None)
        self.store.create_order('Joe', 'limit', 'sell', 10.70, None)
        self.store.create_order('Fred', 'limit', 'buy', 10.80, None)

        self.book.process_events()

        self.assertEqual(len(self.book.active_bids), 1)
        self.assertEqual(len(self.book.active_offers), 0)
        self.assertEqual(len(self.book.trades), 1)

    def test_book_has_active_offers(self):
        self.store.create_order('Geno', 'limit', 'buy', 10.90, None)
        self.store.create_order('Joe', 'limit', 'sell', 10.70, None)
        self.store.create_order('Jane', 'limit', 'sell', 10.50, None)

        self.book.process_events()

        self.assertEqual(len(self.book.active_offers), 1)
        self.assertEqual(len(self.book.active_bids), 0)
        self.assertEqual(len(self.book.trades), 1)

    def test_book_top_offer(self):

        self.store.create_order('Jack', 'limit', 'sell', 10.50, None)
        self.store.create_order('Geno', 'limit', 'buy', 10.90, None)
        self.store.create_order('Joe', 'limit', 'sell', 10.70, None)
        self.store.create_order('Jane', 'limit', 'sell', 10.50, None)

        self.book.process_events()

        self.assertEqual(len(self.book.active_offers), 2)
        self.assertEqual(len(self.book.active_bids), 0)
        self.assertEqual(len(self.book.trades), 1)
        self.assertEqual(self.book.top_offer.price, 10.70)
        self.assertEqual(self.book.top_offer.trader, 'Joe')

        self.assertEqual(self.book.offer_price, 10.70)

    def test_book_top_bid(self):

        self.store.create_order('Geno', 'limit', 'buy', 10.90, None)
        self.store.create_order('Joe', 'limit', 'sell', 10.70, None)
        self.store.create_order('Fred', 'limit', 'buy', 10.80, None)
        self.store.create_order('Jack', 'limit', 'buy', 10.90, None)
        self.store.create_order('Andrea', 'limit', 'buy', 11.15, None)

        self.book.process_events()

        self.assertEqual(len(self.book.active_offers), 0)
        self.assertEqual(len(self.book.active_bids), 3)
        self.assertEqual(len(self.book.trades), 1)
        self.assertEqual(self.book.top_bid.price, 11.15)
        self.assertEqual(self.book.top_bid.trader, 'Andrea')

        self.assertEqual(self.book.bid_price, 11.15)

    def test_book_for_web_tests(self):
        self.store.create_order('Geno', 'limit', 'buy', 10.80, None)
        self.store.create_order('Joe', 'limit', 'sell', 10.50, None)
        self.store.create_order('Bob', 'limit', 'sell', 10.75, None)
        self.store.create_order('Jane', 'limit', 'sell', 10.25, None)
        self.store.create_order('Melvin', 'limit', 'sell', 11.00, None)
        self.store.create_order('Pierre', 'limit', 'buy', 12.0, None)
        self.store.create_order('Joel', 'limit', 'buy', 9.25, None)
        self.store.create_order('Jack', 'limit', 'buy', 10.80, None)

        self.book.process_events()

        self.assertEqual(len(self.book.active_offers), 1)
        self.assertEqual(len(self.book.active_bids), 1)
        self.assertEqual(len(self.book.trades), 3)