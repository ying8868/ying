import pymongo 

def getConn(host,post):
    conn = pymongo.MongoClient(host,post)
    return  conn.ying

 