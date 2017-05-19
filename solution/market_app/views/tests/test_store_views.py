import json
import os
import shutil
import unittest
import tempfile

from dateutil.parser import parse as dt_parse

from market_app.application import create_application
from market_app.database import init_database


class StoreResourceTestCase(unittest.TestCase):

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
        with self.market_app.app_context():
            init_database()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.market_app.config['DATABASE'])

        shutil.rmtree(self.instance_directory)

    def test_get_store(self):
        headers = {'Accept': 'application/json'}
        response = self.app.get('/store_ns/store', headers=headers)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.data)
        self.assertIn('store', content)

    def test_get_orders(self):

        response = self.app.get(
            '/store_ns/orders', headers={'Accept': 'application/json'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        content = json.loads(response.data)

        # init_database() has created two orders in the database
        self.assertEqual(len(content), 8)

    def test_get_order_id(self):

        # Get a valid order id
        order_id = self._get_valid_order_id()

        response = self.app.get(
            '/store_ns/orders/{}'.format(order_id),
            headers={'Accept': 'application/json'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_get_invalid_order_id(self):

        response = self.app.get('/store_ns/orders/xyz')

        self.assertEqual(response.status_code, 404)

    def test_post_new_order(self):
        data = {
            'trader': 'John Doe',
            'order_type': 'market',
            'action': 'buy',
            'price': 10.0,
            "expiry": "2016-09-30T13:05:23.407",
        }

        response = self.app.post(
            '/store_ns/orders', data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)
        self.assertIn('Location', response.headers)

        # get the order and verify the content
        order_location = response.headers['Location']
        response = self.app.get(order_location, content_type='application/json')
        self.assertEqual(200, response.status_code)
        order = json.loads(response.data)

        for key, value in data.items():
            if key == 'expiry':
                self.assertEqual(dt_parse(value), dt_parse(order[key]))
            else:
                self.assertEqual(value, order[key])

    def test_post_new_order_only_required(self):
        data = {
            'trader': 'John Doe',
            'order_type': 'market',
            'action': 'buy',
            'price': 10.0,
        }

        response = self.app.post(
            '/store_ns/orders', data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)

    def test_post_invalid_order_missing_fields(self):
        data = {
            'trader': 'John Doe',
            'order_type': 'market',
        }

        response = self.app.post(
            '/store_ns/orders', data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)

        content = json.loads(response.data)
        self.assertIn('action', content['errors'])
        self.assertIn('price', content['errors'])

    def test_post_invalid_order_invalid_type(self):
        data = {
            'trader': 10,  # set the trader to an integer
            'order_type': 'market',
            'action': 'buy',
            'price': 10.0,
            "expiry": "2016-09-30T13:05:23.407",
        }

        response = self.app.post(
            '/store_ns/orders', data=json.dumps(data),
            content_type='application/json'
        )
        content = json.loads(response.data)

        self.assertEqual(400, response.status_code)
        self.assertIn('trader', content['errors'])

    def test_delete_order(self):

        order_id = self._get_valid_order_id()

        response =  self.app.delete('/store_ns/orders/{}'.format(order_id))

        self.assertEqual(204, response.status_code)

    def test_delete_invalid_order(self):

        response =  self.app.delete('/store_ns/orders/xyz')

        self.assertEqual(404, response.status_code)


    def _get_valid_order_id(self):
        # Get a valid order id
        response = self.app.get(
            '/store_ns/orders', headers={'Accept': 'application/json'}
        )
        content = json.loads(response.data)
        return content[0]['id'] 
