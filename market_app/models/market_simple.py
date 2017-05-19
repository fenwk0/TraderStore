
import copy
import datetime
import logging
import uuid


logger = logging.getLogger()


class SimpleStore(object):

    def __init__(self):
        self._orders = {}
        self._events = []

    def create_order(self, trader, order_type, action, price, expiry=None):
        order_id = uuid.uuid4().get_hex()
        event_id = uuid.uuid4().get_hex()
        if expiry is None:
            expiry = datetime.datetime.max

        self._orders[order_id] = (order_id, trader, order_type, action, price,
                                  expiry)
        self._events.append((event_id, order_id, "create",
                             datetime.datetime.utcnow()))

    def cancel_order(self, order_id):
        event_id = uuid.uuid4().get_hex()
        self._events.append((event_id, order_id, "cancel",
                             datetime.datetime.utcnow()))

    def get_events(self, timestamp):
        return [event for event in self._events
                if event[-1] > timestamp]

    def get_order(self, order_id):
        return self._orders[order_id]

    def load(self, orders, events):
        self._orders = {order.id: order for order in orders}
        self._events = list(sorted(events, key=lambda event: event[-1]))

    def dump(self):
        return self._orders.values(), copy.copy(self._events)

if __name__ == '__main__':
    import time
    from market import Book
    store = SimpleStore()
    book = Book(store)

    store.create_order('Joe', 'limit', 'sell', 10.50, None)
    time.sleep(1)
    store.create_order('Jane', 'limit', 'sell', 10.25, None)
    time.sleep(1)
    store.create_order('Bob', 'limit', 'sell', 10.75, None)
    time.sleep(1)
    store.create_order('Melvin', 'limit', 'sell', 11.00, None)
    time.sleep(1)

    store.create_order('Pierre', 'limit', 'buy', 9.50, None)
    time.sleep(1)
    store.create_order('Joel', 'limit', 'buy', 9.25, None)
    time.sleep(1)
    store.create_order('Geno', 'limit', 'buy', 9.75, None)
    time.sleep(1)
    store.create_order('Ellen', 'limit', 'buy', 9.50, None)
    time.sleep(1)

    book.process_events()
    print("Bid price: {:6.2f}".format(book.bid_price))
    print("Offer price: {:6.2f}".format(book.offer_price))

    store.create_order('Arnold', 'limit', 'sell', 10.00)
    time.sleep(1)
    book.process_events()

    for order in book.active_offers:
        print("{:.<20s} {:6.2f} {}".format(order.trader, order.price, order.action))

    for order in book.trader_orders('Geno'):
        if order.active:
            store.cancel_order(order.id)
            time.sleep(1)
    book.process_events()

    print("Bid price: {:6.2f}".format(book.bid_price))
    print("Offer price: {:6.2f}".format(book.offer_price))

    store.create_order('Juan', 'market', 'buy', None)
    time.sleep(1)
    book.process_events()

    print("Bid price: {:6.2f}".format(book.bid_price))
    print("Offer price: {:6.2f}".format(book.offer_price))

    for order in book.active_offers:
        print("cancel", order)
        store.cancel_order(order.id)
        time.sleep(1)
    book.process_events()

    print("Bid price: {:6.2f}".format(book.bid_price))
    print("Offer price: {:6.2f}".format(book.offer_price))
