import sqlite3
from dbutils.pooled_db import PooledDB

def connect_to_database():
    pool = PooledDB(sqlite3, maxconnections=10, check_same_thread=False, database="timmins_db.db")
    return sqlite3.connect("timmins_db.db")
