import sqlite3 as sqlite3

# create Users table
db_file = "./nftDatabase.db"
con = sqlite3.connect(db_file)
cur = con.cursor()


def read_sentiment(collection):
    sql = '''SELECT Sentiment FROM (
    SELECT Sentiment, id FROM NFTSentiment ORDER BY id) WHERE NftName = ? '''
    cur.execute(sql, (collection,))
    return cur.fetchall()  # return fetched tuple of results


def get_max_id(collection):
    sql = '''SELECT MAX(id) FROM NFTSentiment WHERE NftName = ?'''
    cur.execute(sql, (collection,))
    return cur.fetchall()[0][0]


def check_if_exists(collection):
    sql = '''SELECT * FROM NFTSentiment WHERE NftName = ?'''
    cur.execute(sql, (collection,))
    return not cur.fetchall()[0] == []


def write_sentiment(collection, sentiment):
    if not check_if_exists(collection):
        sql = '''INSERT INTO NFTSentiment VALUES(? ? ?)'''
        cur.execute(sql, (collection, 1, sentiment))
        return

    max_id = get_max_id(collection)

    sql = '''UPDATE NFTSentiment
             SET id = id - 1
             WHERE NftName = ?'''
    cur.execute(sql, (collection,))

    sql = '''DELETE FROM NFTSentiment 
             WHERE NftName = ? 
             AND id = 0'''
    cur.execute(sql, (collection,))

    sql = '''INSERT INTO NFTSentiment VALUES(? ? ?)'''
    cur.execute(sql, (collection, max_id, sentiment))
