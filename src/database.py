import sqlite3
from sqlalchemy import create_engine, table
from sqlalchemy.sql import text, select, func
import pandas as pd

def create_connection(database):
    """Create a connection to a SQLite3 database"""
    connection_url = f"sqlite:///{database}"
    return create_engine(connection_url)

def query_data(conn, query):
    """ Execute a query and return the results as a DataFrame """

    df = pd.read_sql_query(query, conn)
    return df