# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import pymysql
import json
from datetime import datetime

user = "automato"
passw = "MySQLIsFun"
host = "automato.mysql.pythonanywhere-services.com"
database = "automato$schedulin"

app = Flask(__name__)

def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

@app.route('/hello')
def hello():
    return 'Hello from Flask!'

@app.route('/bye')
def bye_bye():
    return 'Bye bye from Flask!'

@app.route("/api/v1/users", methods = ["GET"])
def all_users():
    connection = connect()
    select = """
        SELECT *
        FROM user
        WHERE deletion_date IS NULL;"""
    result = connection.execute(select).fetchall()
    disconnect(connection)
    return jsonify({'result': [dict(row) for row in result]})

@app.route("/api/v1/user/create", methods = ["POST"])
def user_creation():
    parameters = request.get_json()
    name = parameters.get("name")
    email = parameters.get("email")
    status = parameters.get("status")
    creation_date = datetime.now()
    connection = connect()
    insert = """
        INSERT INTO user (name, email, status, creation_date, modification_date)
            VALUES ('{0}', '{1}', '{2}', '{3}', '{3}')""" \
            .format(name, email, status, creation_date)
    connection.execute(insert)
    disconnect(connection)
    return json.dumps({'result': "OK"})

@app.route("/api/v1/user/<string:_id>/update", methods = ["PUT"])
def user_update(_id):
    parameters = request.get_json()
    _id = int(_id)
    status = parameters.get("status")
    modification_date = datetime.now()
    connection = connect()
    update = """
        UPDATE user
        SET status = '{0}',
            modification_date = '{1}'
        WHERE id = {2}
            AND deletion_date IS NULL""".format(status, modification_date, _id)
    connection.execute(update)
    disconnect(connection)
    return json.dumps({'result': "OK"})

@app.route("/api/v1/user/<string:_id>/delete", methods = ["PUT"])
def user_delete(_id):
    #parameters = request.get_json()
    _id = int(_id)
    deletion_date = datetime.now()
    connection = connect()
    delete = """
        UPDATE user
        SET deletion_date = '{0}'
        WHERE id = {1}""".format(deletion_date, _id)
    connection.execute(delete)
    disconnect(connection)
    return json.dumps({'result': "OK"})







