import datetime
import logging
import uuid

logger = logging.getLogger()


class Order(object):
    """ An order in a book or a trade

    Parameters
    ----------
    id : UUID
        A unique ID for the order.
    trader : string
        The name of the trader who placed the order.
    order_type : 'market' or 'limit'
        Market orders are acted upon immediately at the best available price,
        while limit orders persist until the limit price or better is available
        or the order expires.
    action : 'buy' or 'sell'
        Whether the order is a bid or an offer.
    price : float or None
        For limit orders, this is the limit price.  For market orders, this is
        the limit price of the order can't be immediately filled.
    expiry : datetime
        The timestamp for the expiry of the order.
    timestamp : datetime
        The time the order was entered into the system.

    Attributes
    ----------
    traded : bool
        Whether or not the order has resulted in a trade.
    cancelled : bool
        Whether or not the order was cancelled.
    expired : bool
        Whether or not the order has expired.
    active : bool
        Whether or not the order is currently active for trading.

    """

    def __init__(self, id, trader, order_type, action, price, expiry,
                 timestamp):
        self.id = id
        self.trader = trader
        self.order_type = order_type
        self.action = action
        self.price = price
        self.expiry = expiry
        self.timestamp = timestamp

        self.traded = False
        self.cancelled = False
        self.expired = False

    def expire(self, current_time):
        """ Change the expiry state of the order based on the current time """
        if self.expiry is not None and not self.expired:
            self.expired = (self.expiry <= current_time)

    @property
    def active(self):
        return not (self.traded or self.cancelled or self.expired)

    def __repr__(self):
        return (u"{self.__class__.__name__}({self.id!r}, {self.trader!r}, " +
                u"{self.order_type!r}, {self.action!r}, {self.price!r}, " +
                u"{self.expiry!r}, {self.timestamp!r})").format(self=self)


class Trade(object):
    """ A completed trade

    Parameters
    ----------
    id : UUID
        A unique ID for the order.
    bid : Order
        The order for the buy side of the trade.
    offer : Order
        The order for the sell side of the trade.
    price : float
        The price at which the trade occurred.
    timestamp : datetime
        The time the deal was made.
    """

    def __init__(self, bid, offer, price, timestamp):
        self.id = uuid.uuid4()
        self.bid = bid
        self.offer = offer
        self.price = price
        self.timestamp = timestamp

        # mark the orders as traded, so they are no longer active
        self.bid.traded = True
        self.offer.traded = True


def _bid_priority(bid):
    """ Compute the priority of a bid. Smaller values are higher priority.
    """
    # because we want higher bid prices to have higher priority, we take
    # negatives to make them have a smaller value.
    return (-bid.price, bid.timestamp)


def _offer_priority(offer):
    """ Compute the priority of an offer. Smaller values are higher priority.
    """
    return (-offer.price, offer.timestamp)


class Book(object):
    """ A limit order book

    The book relies on an event store that tracks order creation and cancelling
    and uses that information to compute the state of the market as events are
    processed.

    Parameters
    ----------
    store : Store
        An event store that holds the list of events.
    instrument : str
        The name of the instrument being traded.

    Attributes
    ----------
    current_time : datetime
        The UTC timestamp of the last order processed.
    trades : list
        All completed trades, from earliest to latest.
    orders : dict
        A dictionary mapping order id to order instance containing all orders
        that have been processed, including inactive orders.
    active_bids : set or Orders
        All currently active bid orders.
    active_offers : set or Orders
        All currently active offer orders.

    Properties
    ----------
    top_bid : Order or None
        The earliest bid at the highest price.  If there are no bids, the value
        is None.
    top_offer : Order or None
        The earliest offer at the lowest price.  If there are no offers, the
        value is None.
    bid_price : Float
        The price of the top bid.  If there are no bids, the value is 0.
    offer_price : Float
        The price of the top offer.  If there are no offers, the value is inf.
    spread : Float
        The difference between the bid price and the offer price.

    """

    def __init__(self, store, instrument='sack of potatoes'):
        self.store = store
        self.instrument = instrument
        self.reset()
        self.active_offers = set()
        self.active_bids = set()

    def reset(self):
        """ Reset the book to a blank state """
        self.current_time = datetime.datetime.min
        self.orders = {}
        self.trades = []

    def process_events(self):
        """ Query for all new events and update the book's state """
        for event in self.store.get_events(self.current_time):
            self._process_event(*event)

    def trader_orders(self, trader):
        return {order for order in self.orders.values()
                if order.trader == trader}

    def all_trader_orders(self):
        orders = {}
        for order in self.orders.values():
            trader_orders = orders.get(order.trader, set())
            trader_orders.add(order)
        return orders

    @property
    def top_bid(self):
        if self.active_bids:
            return min(self.active_bids, key=_bid_priority)
        else:
            return None

    @property
    def top_offer(self):
        if self.active_offers:
            return min(self.active_offers, key=_offer_priority)
        else:
            return None

    @property
    def bid_price(self):
        if self.top_bid is not None:
            return self.top_bid.price
        return 0.0

    @property
    def offer_price(self):
        if self.top_offer is not None:
            return self.top_offer.price
        return float('inf')

    @property
    def spread(self):
        return self.offer_price - self.bid_price

    # --------------------------------------------------------------------------
    # Internal methods
    # --------------------------------------------------------------------------

    def _process_event(self, event_id, order_id, action, event_time):
        """ Process a single event

        This advances the current time to the event's timestamp and then
        processes the assocaiated order according to the action type.

        Parameters
        ----------
        event_id : uuid
            The uuid of the event.
        order_id : uuid
            The uuid of the associated order.
        action : 'create' or 'cancel'
            The type of action to perform on the order.
        event_time : datetime
            The UTC time that the event occurred.
        """
        self._update_book_time(event_time)

        if action == 'create':
            self._new_order(order_id, event_time)
        elif action == 'cancel':
            self._cancel_order(order_id)
        else:
            logger.error('Unknown event action: {}'.format(action))

    def _update_book_time(self, timestamp):
        """ Update state of the book based on the given timestamp

        This sets the current_time attribute to the new value, checks for
        expired orders, and updates the sets of active bids and offers.
        """

        self.current_time = timestamp

        # check for expired orders
        for order in self.orders.values():
            order.expire(timestamp)

        # update active bids and offers
        self.active_bids = {order for order in self.orders.values()
                            if order.active and order.action == 'buy'}
        self.active_offers = {order for order in self.orders.values()
                              if order.active and order.action == 'sell'}

    def _new_order(self, order_id, timestamp):
        """ Create a new Order object using data from the store """
        order_data = self.store.get_order(order_id)
        order = Order(*order_data, timestamp=timestamp)

        if order.action == 'buy':
            self._process_bid(order)
        elif order.action == 'sell':
            self._process_offer(order)
        else:
            logger.error('Unknown order action: {}'.format(order.action))

    def _cancel_order(self, order_id):
        """ Cancel an order based on order_id """
        try:
            order = self.orders[order_id]
        except KeyError:
            logger.error("Can't find order {}.".format(order_id))
            return

        if order.active:
            order.cancelled = True
            if order.action == 'buy':
                self.active_bids.discard(order)
            elif order.action == 'sell':
                self.active_offers.discard(order)

    def _process_bid(self, bid):
        """ Process a buy order

        We look for the top offer in the book, and if it matches we create a
        trade, removing the top offer from the active offers.
        If there is no top offer in the book, we add the order to the current
        set of orders, and if it is a limit order, it is added to the active
        bids.  A market order which can't be filled is cancelled.
        """
        offer = self.top_offer
        if offer and (bid.order_type == 'market' or offer.price <= bid.price):
            # top offer matches bid, so make a trade and remove offer
            self.active_offers.discard(offer)
            trade = Trade(bid, offer, offer.price, self.current_time)
            self.trades.append(trade)
        elif bid.order_type == 'market':
            # market orders which can't be filled are cancelled.
            bid.cancelled = True
        else:
            # limit orders which can't be filled become active bids.
            self.active_bids.add(bid)
        # record that we have seen bid
        self.orders[bid.id] = bid

    def _process_offer(self, offer):
        """ Process a sell order

        We look for the top bid in the book, and if it matches we create a
        trade, removing the top bid from the active bids.
        If there is no top offer in the book, we add the order to the current
        set of orders, and if it is a limit order, it is added to the active
        offers.  A market order which can't be filled is cancelled.
        """
        bid = self.top_bid
        if bid and (offer.order_type == 'market' or offer.price <= bid.price):
            # top bid matches offer, so make a trade and remove bid
            self.active_bids.discard(bid)
            trade = Trade(bid, offer, bid.price, self.current_time)
            self.trades.append(trade)
        elif offer.order_type == 'market':
            # market orders which can't be filled are cancelled.
            offer.cancelled = True
        else:
            # limit orders which can't be filled become active offers.
            self.active_offers.add(offer)
        # record that we have seen offer
        self.orders[offer.id] = offer
