import pymongo
from urllib.parse import quote_plus

user = "automato"
passw = "MySQLIsFun"
host = "mongodb-schedulin.hlbmw0g.mongodb.net"
database = "schedulin"

def connect():
    client = pymongo.MongoClient(
        "mongodb+srv://{0}:{1}@{2}/?retryWrites=true&w=majority" \
            .format(user, passw, host), tls = False)
    print("Connected to the MongoDB database {0}!" \
        .format(client.list_databases()))
    conn = client[database]
    return conn

app = connect()
