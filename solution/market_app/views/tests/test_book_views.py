import json
import logging
import os
import shutil
import unittest
import tempfile

from market_app.application import create_application
from market_app.database import init_database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BookViewsTestCase(unittest.TestCase):

    def setUp(self):

        self.instance_directory = tempfile.mkdtemp()
        config_file = os.path.join(self.instance_directory, 'application.cfg')
        with open(config_file, 'w') as fh:
            fh.write("INSTRUMENT = 'test_instrument'")

        self.market_app = create_application(self.instance_directory)
        self.market_app.testing = True

        self.db_fd, self.market_app.config['DATABASE'] = tempfile.mkstemp()
        self.market_app.config['TESTING'] = True
        self.app = self.market_app.test_client()
        self.app.testing = True
        with self.market_app.app_context():
            init_database()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.market_app.config['DATABASE'])

        shutil.rmtree(self.instance_directory)

    def test_get_book(self):
        headers = {'Accept': 'application/json'}
        response = self.app.get('/book_ns/book', headers=headers)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.data)
        for keyword in ['instrument', 'current_time', 'store']:
            self.assertIn(keyword, content)
        self.assertEqual('test_instrument', content['instrument'])

    def test_get_book_orders(self):
        headers = {'Accept': 'application/json'}
        response = self.app.get('/book_ns/book/orders', headers=headers)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.data)
        self.assertEqual(len(content), 8)

    def test_get_book_orders_for_trader(self):
        headers = {'Accept': 'application/json'}
        response = self.app.get(
            '/book_ns/book/traders/Jack/orders', headers=headers
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.data)
        self.assertEqual(len(content), 1)

    def test_get_book_stats(self):
        headers = {'Accept': 'application/json'}
        response = self.app.get(
            '/book_ns/book/stats', headers=headers
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.data)
        self.assertEqual(len(content), 6)
        stat_keywords = [
            'bid_price', 'offer_price', 'top_offer', 'top_bid', 'spread',
            'trade_count'
        ]
        for keyword in stat_keywords:
            self.assertIn(keyword, content)

    def test_get_book_trades(self):
        headers = {'Accept': 'application/json'}
        response = self.app.get('/book_ns/book/trades', headers=headers)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.data)
        print 'X' * 50
        print content
        self.assertEqual(len(content), 3)

    def test_get_book_active_bids(self):
        headers = {'Accept': 'application/json'}
        response = self.app.get('/book_ns/book/active_bids', headers=headers)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.data)
        self.assertEqual(len(content), 1)

    def test_get_book_active_offers(self):
        headers = {'Accept': 'application/json'}
        response = self.app.get('/book_ns/book/active_offers', headers=headers)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.data)
        self.assertEqual(len(content), 1)