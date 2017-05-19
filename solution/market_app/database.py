import os
import sqlite3 as db

from flask import g, current_app

from .models.market_db import SQLStore


def get_connection():
    if not hasattr(g, 'db_connection'):
        db_file = os.path.join(
            current_app.instance_path, current_app.config['DATABASE']
        )
        db_connection = db.connect(
            db_file,
            detect_types=db.PARSE_DECLTYPES | db.PARSE_COLNAMES
        )
        # Use an optimized Row factory which allows us to access row content
        # by index or keys
        db_connection.row_factory = db.Row

        # assign the object to the global application context
        g.db_connection = db_connection

    return g.db_connection


def init_database():
    # This function should only be used within an application context
    conn = get_connection()
    store = SQLStore(conn)
    store.create_order('Geno', 'limit', 'buy', 10.80, None)
    store.create_order('Joe', 'limit', 'sell', 10.50, None)
    store.create_order('Bob', 'limit', 'sell', 10.75, None)
    store.create_order('Jane', 'limit', 'sell', 10.25, None)
    store.create_order('Melvin', 'limit', 'sell', 11.00, None)
    store.create_order('Pierre', 'limit', 'buy', 12.0, None)
    store.create_order('Joel', 'limit', 'buy', 9.25, None)
    store.create_order('Jack', 'limit', 'buy', 10.80, None)


def close_db(error):
    """Closes the database again at the end of the request.
    
    This function must be registered to be called in the tearDown of the Flask
    appcontext. 
    """
    if hasattr(g, 'db_connection'):
        g.db_connection.close()
