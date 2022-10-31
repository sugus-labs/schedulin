# A very simple Flask Hello World app for you to get started with...

<<<<<<< HEAD
from flask import Flask, jsonify
from sqlalchemy import create_engine
from datetime import datetime
from flask_restx import Api, Namespace, Resource, \
    reqparse, inputs, fields

=======
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import pymysql
import json
from datetime import datetime
>>>>>>> c510a28ec5ed78cba857ffbb3fbd3277b9324052

user = "automato"
passw = "MySQLIsFun"
host = "automato.mysql.pythonanywhere-services.com"
database = "automato$schedulin"

app = Flask(__name__)

<<<<<<< HEAD
app.config["SQLALCHEMY_DATABASE_URI"] = host
app.config["SQLALCHEMY_DATABASE_URI"] = host

api = Api(app, version = '1.0',
    title = 'The famous automato API',
    description = """
        The automato API is an API to manage reservations
        inside a neighborhood community.""",
    contact = "gustavo.martinvela@opendeusto.es",
    endpoint = "/api/v1"
)

user_model = api.model(
    'user', {
        'id': fields.Integer,
        'name': fields.String(required = True),
        'email': fields.String(required = True),
        'status': fields.String(enum = ['ACTIVE', 'INACTIVE']),
})

timetable_model = api.model(
    'timetable', {
        'id': fields.Integer,
        'start_time': fields.String(required = True),
        'end_time': fields.String(required = True),
})

resource_model = api.model(
    'resource', {
        'id': fields.Integer,
        'timetable_id': fields.Integer,
        'type': fields.String(required = True),
        'description': fields.String,
        'max_pax': fields.Integer(min = 0),
        'price': fields.Integer(min = 0),
        'hours_in_advance': fields.Integer(min = 0),
})

reservation_model = api.model(
    'reservation', {
        'id': fields.Integer,
        'resource_id': fields.Integer,
        'user_id': fields.Integer,
        'start_time': fields.String(required = True),
        'num_pax': fields.Integer(min = 0),
        'status': fields.String(enum = ['CONFIRMED', 'CANCELLED', 'EXECUTED']),
})

=======
>>>>>>> c510a28ec5ed78cba857ffbb3fbd3277b9324052
def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

<<<<<<< HEAD
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
            WHERE deletion_date IS NULL
            LIMIT 10;"""
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
        help = 'The status of the user. Values are: ACTIVE, INACTIVE',
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
        return jsonify({'result': "OK"})

user_update_parser = reqparse.RequestParser()
user_update_parser.add_argument('status', type = str,
        help = 'The status of the user. ACTIVE or INACTIVE',
        location = 'form')

@users.route("/user/<string:id>")
@users.doc(params = {'id': 'The ID of the user'})
class select_user(Resource):

    @api.response(404, "USER not found")
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
        return jsonify({'result': "OK"})

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
        return jsonify({'result': "OK"})

timetables = Namespace('timetables',
    description = 'All operations related to timetables',
    path='/api/v1')
api.add_namespace(timetables)

@timetables.route("/timetables")
class all_timetables(Resource):
    def get(self):
        connection = connect()
        select = """
            SELECT *
            FROM timetable
            WHERE deletion_date IS NULL
            LIMIT 10;"""
        result = connection.execute(select).fetchall()
        disconnect(connection)
        return jsonify({'result': [dict(row) for row in result]})

timetable_creation_parser = reqparse.RequestParser()
timetable_creation_parser.add_argument('start_time', type = str,
        help = 'The start time of the schedule',
        location = 'form')
timetable_creation_parser.add_argument('end_time', type = str,
        help = 'The end time of the schedule',
        location = 'form')

@timetables.route("/timetable")
#@users.doc(params = {'id': 'The ID of the user'})
class create_timetable(Resource):

    @api.doc(parser = timetable_creation_parser)
    @api.expect(timetable_creation_parser)
    def post(self):
        args = timetable_creation_parser.parse_args()
        start_time = args['start_time']
        end_time = args['end_time']
        creation_date = datetime.now()
        connection = connect()
        insert = """
            INSERT INTO timetable (start_time, end_time, creation_date, modification_date)
                VALUES ('{0}', '{1}', '{2}', '{2}')""" \
                .format(start_time, end_time, creation_date)
        connection.execute(insert)
        disconnect(connection)
        return jsonify({'result': "OK"})

timetable_update_parser = reqparse.RequestParser()
timetable_update_parser.add_argument('start_time', type = str,
        help = 'The start time of the schedule',
        location = 'form')
timetable_update_parser.add_argument('end_time', type = str,
        help = 'The end time of the schedule',
        location = 'form')

@timetables.route("/timetable/<string:id>")
@timetables.doc(params = {'id': 'The ID of the timetable'})
class select_timetable(Resource):

    @api.response(404, "TIMETABLE not found")
    def get(self, id):
        id = int(id)
        connection = connect()
        select = """
            SELECT *
            FROM timetable
            WHERE id = {0}
                AND deletion_date IS NULL;""".format(id)
        result = connection.execute(select).fetchall()
        disconnect(connection)
        return jsonify({'result': [dict(row) for row in result]})

    @api.doc(parser = timetable_update_parser)
    @api.expect(timetable_update_parser)
    def put(self, id):
        id = int(id)
        args = timetable_creation_parser.parse_args()
        start_time = args['start_time']
        end_time = args['end_time']
        modification_date = datetime.now()
        connection = connect()
        update = """
            UPDATE timetable
            SET start_time = '{0}',
                end_time = '{1}',
                modification_date = '{2}'
            WHERE id = {3}
                AND deletion_date IS NULL""".format(
                    start_time, end_time, modification_date, id)
        connection.execute(update)
        disconnect(connection)
        return jsonify({'result': "OK"})

    def delete(self, id):
        id = int(id)
        deletion_date = datetime.now()
        connection = connect()
        delete = """
            UPDATE timetable
            SET deletion_date = '{0}'
            WHERE id = {1}""".format(deletion_date, id)
        connection.execute(delete)
        disconnect(connection)
        return jsonify({'result': "OK"})

resources = Namespace('resources',
    description = 'All operations related to resources',
    path='/api/v1')
api.add_namespace(resources)

@resources.route("/resources")
class all_resources(Resource):
    def get(self):
        connection = connect()
        select = """
            SELECT *
            FROM resource
            WHERE deletion_date IS NULL
            LIMIT 10;"""
        result = connection.execute(select).fetchall()
        disconnect(connection)
        return jsonify({'result': [dict(row) for row in result]})

resource_creation_parser = reqparse.RequestParser()
resource_creation_parser.add_argument('timetable_id', type = int,
        help = 'The id of the timetable associated',
        location = 'form')
resource_creation_parser.add_argument('type', type = str,
        help = 'The type of the resource',
        location = 'form')
resource_creation_parser.add_argument('description', type = str,
        help = 'The description of the resource',
        location = 'form')
resource_creation_parser.add_argument('max_pax', type = int,
        help = 'The maximum number of persons simultaneously in the resource',
        location = 'form')
resource_creation_parser.add_argument('price', type = float,
        help = 'The price of the resource in the timetable',
        location = 'form')
resource_creation_parser.add_argument('hours_in_advance', type = int,
        help = 'The minimum hours in advance to reserve',
        location = 'form')

@resources.route("/resource")
#@users.doc(params = {'id': 'The ID of the user'})
class create_resource(Resource):

    @api.doc(parser = resource_creation_parser)
    @api.expect(resource_creation_parser)
    def post(self):
        args = resource_creation_parser.parse_args()
        timetable_id = args['timetable_id']
        type = args['type']
        description = args['description']
        if description.upper() == 'NONE':
            description = None
        max_pax = args['max_pax']
        price = args['price']
        hours_in_advance = args['hours_in_advance']
        creation_date = datetime.now()
        connection = connect()
        insert = """
            INSERT INTO resource (timetable_id, type, description,
                max_pax, price, hours_in_advance, creation_date, modification_date)
                VALUES ({0}, '{1}', '{2}', {3}, {4}, {5},
                '{6}', '{6}')""" \
                .format(timetable_id, type, description, max_pax,
                    price, hours_in_advance, creation_date)
        connection.execute(insert)
        disconnect(connection)
        return jsonify({'result': "OK"})

resource_update_parser = reqparse.RequestParser()
resource_update_parser.add_argument('timetable_id', type = int,
        help = 'The id of the timetable associated',
        location = 'form')
resource_update_parser.add_argument('type', type = str,
        help = 'The type of the resource',
        location = 'form')
resource_update_parser.add_argument('description', type = str,
        help = 'The description of the resource',
        location = 'form')
resource_update_parser.add_argument('max_pax', type = int,
        help = 'The maximum number of persons simultaneously in the resource',
        location = 'form')
resource_update_parser.add_argument('price', type = float,
        help = 'The price of the resource in the timetable',
        location = 'form')
resource_update_parser.add_argument('hours_in_advance', type = int,
        help = 'The minimum hours in advance to reserve',
        location = 'form')

@resources.route("/resource/<string:id>")
@resources.doc(params = {'id': 'The ID of the resource'})
class select_resource(Resource):

    @api.response(404, "RESOURCE not found")
    def get(self, id):
        id = int(id)
        connection = connect()
        select = """
            SELECT *
            FROM resource
            WHERE id = {0}
                AND deletion_date IS NULL;""".format(id)
        result = connection.execute(select).fetchall()
        disconnect(connection)
        return jsonify({'result': [dict(row) for row in result]})

    @api.doc(parser = resource_update_parser)
    @api.expect(resource_update_parser)
    def put(self, id):
        id = int(id)
        args = resource_creation_parser.parse_args()
        timetable_id = args['timetable_id']
        type = args['type']
        description = args['description']
        if description:
            if description.upper() == 'NONE':
                description = None
        max_pax = args['max_pax']
        price = args['price']
        hours_in_advance = args['hours_in_advance']
        modification_date = datetime.now()
        connection = connect()
        update = """
            UPDATE resource
            SET timetable_id = {0},
                type = '{1}',
                description = '{2}',
                max_pax = {3},
                price = {4},
                hours_in_advance = {5},
                modification_date = '{6}'
            WHERE id = {7}
                AND deletion_date IS NULL""" \
                .format(timetable_id, type, description, max_pax,
                    price, hours_in_advance, modification_date, id)
        connection.execute(update)
        disconnect(connection)
        return jsonify({'result': "OK"})

    def delete(self, id):
        id = int(id)
        deletion_date = datetime.now()
        connection = connect()
        delete = """
            UPDATE resource
            SET deletion_date = '{0}'
            WHERE id = {1}""".format(deletion_date, id)
        connection.execute(delete)
        disconnect(connection)
        return jsonify({'result': "OK"})

reservations = Namespace('reservations',
    description = 'All operations related to reservations',
    path='/api/v1')
api.add_namespace(reservations)

@reservations.route("/reservations")
class all_reservations(Resource):
    def get(self):
        connection = connect()
        select = """
            SELECT *
            FROM reservation
            WHERE deletion_date IS NULL
            LIMIT 10;"""
        result = connection.execute(select).fetchall()
        disconnect(connection)
        return jsonify({'result': [dict(row) for row in result]})

reservation_creation_parser = reqparse.RequestParser()
reservation_creation_parser.add_argument('resource_id', type = int,
        help = 'The id of the resource associated',
        location = 'form')
reservation_creation_parser.add_argument('user_id', type = int,
        help = 'The id of the user associated',
        location = 'form')
reservation_creation_parser.add_argument('start_time', type = str,
        help = 'The start time of the reservation',
        location = 'form')
reservation_creation_parser.add_argument('num_pax', type = int,
        help = 'The number of persons simultaneously in the reservation',
        location = 'form')
reservation_creation_parser.add_argument('status', type = str,
        help = 'The status of the reservation. Values are: CONFIRMED, CANCELLED, EXECUTED',
        location = 'form')
reservation_creation_parser.add_argument('date', type = inputs.date_from_iso8601,
        help = 'The date of the reservation',
        location = 'form')

@reservations.route("/reservation")
#@users.doc(params = {'id': 'The ID of the user'})
class create_reservation(Resource):

    @api.doc(parser = reservation_creation_parser)
    @api.expect(reservation_creation_parser)
    def post(self):
        args = reservation_creation_parser.parse_args()
        resource_id = args['resource_id']
        user_id = args['user_id']
        start_time = args['start_time']
        num_pax = args['num_pax']
        status = args['status']
        date = args['date']
        creation_date = datetime.now()
        connection = connect()
        insert = """
            INSERT INTO reservation (resource_id, user_id, start_time,
                num_pax, status, date, creation_date, modification_date)
                VALUES ({0}, {1}, '{2}', {3}, '{4}', '{5}', '{6}', '{6}')""" \
                .format(resource_id, user_id, start_time,
                num_pax, status, date, creation_date)
        connection.execute(insert)
        disconnect(connection)
        return jsonify({'result': "OK"})

reservation_update_parser = reqparse.RequestParser()
reservation_update_parser.add_argument('resource_id', type = int,
        help = 'The id of the resource associated',
        location = 'form')
reservation_update_parser.add_argument('user_id', type = int,
        help = 'The id of the user associated',
        location = 'form')
reservation_update_parser.add_argument('start_time', type = str,
        help = 'The start time of the reservation',
        location = 'form')
reservation_update_parser.add_argument('num_pax', type = int,
        help = 'The number of persons simultaneously in the reservation',
        location = 'form')
reservation_update_parser.add_argument('status', type = str,
        help = 'The status of the reservation. Values are: CONFIRMED, CANCELLED, EXECUTED',
        location = 'form')
reservation_update_parser.add_argument('date', type = inputs.date_from_iso8601,
        help = 'The date of the reservation',
        location = 'form')

@reservations.route("/reservation/<string:id>")
@reservations.doc(params = {'id': 'The ID of the reservation'})
class select_reservation(Resource):

    @api.response(404, "RESERVATION not found")
    def get(self, id):
        id = int(id)
        connection = connect()
        select = """
            SELECT *
            FROM reservation
            WHERE id = {0}
                AND deletion_date IS NULL;""".format(id)
        result = connection.execute(select).fetchall()
        disconnect(connection)
        return jsonify({'result': [dict(row) for row in result]})

    @api.doc(parser = reservation_update_parser)
    @api.expect(reservation_update_parser)
    def put(self, id):
        id = int(id)
        args = reservation_update_parser.parse_args()
        resource_id = args['resource_id']
        user_id = args['user_id']
        start_time = args['start_time']
        num_pax = args['num_pax']
        status = args['status']
        date = args['date']
        modification_date = datetime.now()
        connection = connect()
        update = """
            UPDATE reservation
            SET resource_id = {0},
                user_id = {1},
                start_time = '{2}',
                num_pax = {3},
                status = '{4}',
                date = '{5}',
                modification_date = '{6}'
            WHERE id = {7}
                AND deletion_date IS NULL""" \
                .format(resource_id, user_id, start_time,
                num_pax, status, date, modification_date, id)
        connection.execute(update)
        disconnect(connection)
        return jsonify({'result': "OK"})

    def delete(self, id):
        id = int(id)
        deletion_date = datetime.now()
        connection = connect()
        delete = """
            UPDATE reservation
            SET deletion_date = '{0}'
            WHERE id = {1}""".format(deletion_date, id)
        connection.execute(delete)
        disconnect(connection)
        return jsonify({'result': "OK"})

@reservations.route("/reservation/findByDate/<string:date>")
@reservations.doc(params = {'date': 'The day of the reservation'})
class find_reservation_by_day(Resource):

    @api.response(404, "RESERVATION not found")
    def get(self, date):
        connection = connect()
        select = """
            SELECT *
            FROM reservation
            WHERE date = '{0}';""".format(date)
        result = connection.execute(select).fetchall()
        disconnect(connection)
        return jsonify({'result': [dict(row) for row in result]})

=======
@app.route('/hello')
def hello():
    return 'Hello from Flask!'
>>>>>>> c510a28ec5ed78cba857ffbb3fbd3277b9324052


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







