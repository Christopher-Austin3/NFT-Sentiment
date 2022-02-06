import sqlite3

con = sqlite3.connect("nftDatabase.db")
cur = con.cursor()
query = '''INSERT INTO NFT (Name, Collection, Sentiment) VALUES (?,?,?)'''
cur.execute(query, ("Test9","doge","0.4"))
con.commit()
con.close()