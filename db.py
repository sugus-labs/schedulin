import pandas as pd
import pymysql
from sqlalchemy import create_engine
import json

user = "automato"
passw = "MySQLIsFun"
host = "automato.mysql.pythonanywhere-services.com"
database = "automato$schedulin"

db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
conn = db.connect()

databases = conn.execute(
    "SHOW DATABASES;"
)

for db in databases.fetchall():
    print(db)