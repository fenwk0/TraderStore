import json
import os
import unittest
import tempfile

from market_app.application import create_application
from market_app.database import init_database


class BookViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.market_app = create_application()

        self.db_fd, self.market_app.config['DATABASE'] = tempfile.mkstemp()
        self.market_app.config['TESTING'] = True
        with self.market_app.app_context():
            init_database()

        self.client = self.market_app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.market_app.config['DATABASE'])

    def test_get_book(self):
        headers = {'Accept': 'application/json'}
        response = self.client.get('/store_ns/book', headers=headers)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.data)
        self.assertIn('store', content)