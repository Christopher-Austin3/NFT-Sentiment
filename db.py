import sqlite3 as sqlite3

# create Users table
db_file = "./nftDatabase.db"


def create_connection():
    conn = sqlite3.connect(db_file)
    return conn


def read_sentiment():
    return 1


def write_sentiment():
    pass
