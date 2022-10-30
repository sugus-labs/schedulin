# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import pymysql
import json
from datetime import datetime
from flask_restx.representations import output_json
from flask_restx import Api, Namespace, Resource, reqparse

user = "automato"
passw = "MySQLIsFun"
host = "automato.mysql.pythonanywhere-services.com"
database = "automato$schedulin"

app = Flask(__name__)
api = Api(app, version = '1.0',
    title = 'The famous automato API',
    description = """
        The automato API is an API to manage reservations
        inside a neighborhood community.""",
    contact = "gustavo.martinvela@opendeusto.es",
    endpoint = "/api/v1"
)

def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

basics = Namespace('basics',
    description = 'Basic operations',
    path='/api/v1')
api.add_namespace(basics)

@basics.route('/hello')
class hello_swagger(Resource):

    def get(self):
        return 'Hello from Flask!'

@basics.route('/bye')
class bye_swagger(Resource):

    def get(self):
        return 'Bye bye from Flask!'

users = Namespace('users',
    description = 'All operations related to users',
    path='/api/v1')
api.add_namespace(users)

@users.route("/users")
class all_users(Resource):
    def get(self):
        connection = connect()
        select = """
            SELECT *
            FROM user
            WHERE deletion_date IS NULL;"""
        result = connection.execute(select).fetchall()
        disconnect(connection)
        return jsonify({'result': [dict(row) for row in result]})

user_creation_parser = reqparse.RequestParser()
user_creation_parser.add_argument('name', type = str,
        help = 'The name and surnames of the user',
        location = 'form')
user_creation_parser.add_argument('email', type = str,
        help = 'The main email of the user to communicate with',
        location = 'form')
user_creation_parser.add_argument('status', type = str,
        help = 'The status of the user. ACTIVE or INACTIVE',
        location = 'form')

@users.route("/user")
#@users.doc(params = {'id': 'The ID of the user'})
class create_user(Resource):

    @api.doc(parser = user_creation_parser)
    @api.expect(user_creation_parser)
    def post(self):
        args = user_creation_parser.parse_args()
        name = args['name']
        email = args['email']
        status = args['status']
        creation_date = datetime.now()
        connection = connect()
        insert = """
            INSERT INTO user (name, email, status, creation_date, modification_date)
                VALUES ('{0}', '{1}', '{2}', '{3}', '{3}')""" \
                .format(name, email, status, creation_date)
        connection.execute(insert)
        disconnect(connection)
        return json.dumps({'result': "OK"})

user_update_parser = reqparse.RequestParser()
user_update_parser.add_argument('status', type = str,
        help = 'The status of the user. ACTIVE or INACTIVE',
        location = 'form')

@users.route("/user/<string:id>")
@users.doc(params = {'id': 'The ID of the user'})
class select_user(Resource):

    def get(self, id):
        id = int(id)
        connection = connect()
        select = """
            SELECT *
            FROM user
            WHERE id = {0}
                AND deletion_date IS NULL;""".format(id)
        result = connection.execute(select).fetchall()
        disconnect(connection)
        return jsonify({'result': [dict(row) for row in result]})

    @api.doc(parser = user_update_parser)
    @api.expect(user_update_parser)
    def put(self, id):
        id = int(id)
        args = user_update_parser.parse_args()
        status = args['status']
        modification_date = datetime.now()
        connection = connect()
        update = """
            UPDATE user
            SET status = '{0}',
                modification_date = '{1}'
            WHERE id = {2}
                AND deletion_date IS NULL""".format(status, modification_date, id)
        connection.execute(update)
        disconnect(connection)
        return json.dumps({'result': "OK"})

    def delete(self, id):
        id = int(id)
        deletion_date = datetime.now()
        connection = connect()
        delete = """
            UPDATE user
            SET deletion_date = '{0}'
            WHERE id = {1}""".format(deletion_date, id)
        connection.execute(delete)
        disconnect(connection)
        return json.dumps({'result': "OK"})

timetables = Namespace('timetables',
    description = 'All operations related to timetables',
    path='/api/v1')
api.add_namespace(timetables)

