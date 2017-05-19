
import datetime
import logging
import sqlite3 as db
import uuid


logger = logging.getLogger()


order_table_sql = """
create table if not exists orders (
    id text primary key,
    trader text,
    order_type text,
    action text,
    price real,
    expiry timestamp
)
"""

create_order_sql = """
insert into orders values (?, ?, ?, ?, ?, ?)
"""

get_order_sql = """
select * from orders where id = ?
"""

dump_orders_sql = """
select * from orders
"""


event_table_sql = """
create table if not exists events (
    id text primary key,
    order_id text references orders(id),
    action text,
    event_time timestamp
)
"""

create_event_sql = """
insert into events values (?, ?, ?, ?)
"""

get_events_sql = """
select * from events where event_time > ? order by event_time
"""

dump_events_sql = """
select * from events
"""


class SQLStore(object):

    def __init__(self, connection):
        self.connection = connection
        self._create_tables()
        self.__version__ = '1.0' # very naive version management

    def create_order(self, trader, order_type, action, price, expiry=None):
        order_id = uuid.uuid4().get_hex()
        event_id = uuid.uuid4().get_hex()
        if expiry is None:
            expiry = datetime.datetime.max

        with self.connection:
            self.connection.execute(
                create_order_sql,
                (order_id, trader, order_type, action, price, expiry)
            )
            self.connection.execute(
                create_event_sql,
                (event_id, order_id, "create", datetime.datetime.utcnow())
            )

        return order_id

    def cancel_order(self, order_id):
        event_id = uuid.uuid4().get_hex()
        with self.connection:
            self.connection.execute(
                create_event_sql,
                (event_id, order_id, "cancel", datetime.datetime.utcnow())
            )

    def get_events(self, timestamp):
        with self.connection as conn:
            cursor = conn.execute(get_events_sql, (str(timestamp)[:-3],))
            events = cursor.fetchall()
        return events

    def get_order(self, order_id, as_dict=False):
        with self.connection:
            cursor = self.connection.execute(get_order_sql, (order_id,))
            order = cursor.fetchone()
        if as_dict and order is not None:
            order = {key: order[key] for key in order.keys()}
        return order

    def get_orders(self, as_dict=False):
        with self.connection:
            cursor = self.connection.execute(dump_orders_sql)
            orders = cursor.fetchall()
        if as_dict:
            orders = [
                {key: order[key] for key in order.keys()} for order in orders
            ]
        return orders

    def load(self, orders, events):
        with self.connection:
            self.connection.executemany(create_order_sql, orders)
            self.connection.executemany(create_event_sql, events)

    def dump(self):
        with self.connection:
            cursor = self.connection.execute(dump_orders_sql)
            orders = cursor.fetchall()
            cursor = self.connection.execute(dump_events_sql)
            events = cursor.fetchall()
        return orders, events

    #--------------------------------------------------------------------------
    # Internal methods
    #--------------------------------------------------------------------------

    def _create_tables(self):
        with self.connection:
            self.connection.execute(order_table_sql)
            self.connection.execute(event_table_sql)

    def __repr__(self):
        return 'SQLStore connected to {}'.format(str(self.connection))


if __name__ == '__main__':
    import time
    from market import Book
    connection = db.connect(
        ':memory:', detect_types=db.PARSE_DECLTYPES | db.PARSE_COLNAMES)
    store = SQLStore(connection)
    book = Book(store, 'potatoes')

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
