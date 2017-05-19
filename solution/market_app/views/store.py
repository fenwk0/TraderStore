from flask import url_for, request
from flask_restplus import Resource, Namespace, fields

from market_app.models.market_db import SQLStore
from market_app.database import get_connection

store_ns = Namespace('store_ns', description='Store related operations')

# An order has no id when received it is created
order_model = store_ns.model(
    'Order', {
        'id': fields.String(required=False),
        'trader': fields.String(required=True),
        'order_type': fields.String(enum=['limit', 'market'], required=True),
        'action': fields.String(enum=['sell', 'buy'], required=True),
        'price': fields.Float(required=True),
        'expiry': fields.DateTime(required=False)
    }
)


class BaseStore(Resource):
    @property
    def store(self):
        connection = get_connection()
        return SQLStore(connection)


class Store(BaseStore):

    def get(self):
        """ Returns a description of the store."""

        return {'store': repr(self.store)}


class Orders(BaseStore):

    @store_ns.marshal_list_with(order_model)
    def get(self):
        """ Return the list of orders in the store."""

        results = self.store.get_orders(as_dict=True)

        return results

    @store_ns.expect(order_model, validate=True)
    def post(self):
        """ Create a new order. """

        payload = request.json

        # convert expiry date to datetime object
        if 'expiry' in payload:
            payload['expiry'] = order_model['expiry'].parse(payload['expiry'])

        order_id = self.store.create_order(**payload)
        location = url_for('order', order_id=order_id)
        return 'Order created', 201, {'Location': location}


@store_ns.response(404, 'Invalid order')
class Order(BaseStore):

    @store_ns.marshal_with(order_model)
    def get(self, order_id):
        """ Return an existing order. """

        # Asking for the result as dict to make sure the marshalling layer
        # works as expected. marshal_with() does not support using a Row object.
        order = self.store.get_order(order_id, as_dict=True)
        if order is None:
            return 'Invalid Order', 404
        else:
            return order

    @store_ns.response(204, 'Order deleted')
    def delete(self, order_id):
        """ Delete an existing order."""

        valid_ids = [order['id'] for order in self.store.get_orders()]
        order_exists = order_id in valid_ids
        if order_exists:
            self.store.cancel_order(order_id)
            return 'Order deleted', 204
        else:
            store_ns.abort(404, 'Invalid order')

store_ns.add_resource(Store, '/store', endpoint='store')
store_ns.add_resource(Orders, '/orders', endpoint='orders')
store_ns.add_resource(Order, '/orders/<order_id>', endpoint='order')
