from flask import g, current_app
import sqlite3 as db

from .models.market_db import SQLStore


def get_connection():
    if not hasattr(g, 'db_connection'):
        db_connection = db.connect(
            current_app.config['DATABASE'],
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
    store.create_order('Joe', 'limit', 'sell', 10.50, None) # should make a trade
    

def close_db(error):
    """Closes the database again at the end of the request.
    
    This function must be registerd to be called in the teardow of the Flask
    appcontext. 
    """
    if hasattr(g, 'db_connection'):
        g.db_connection.close()
