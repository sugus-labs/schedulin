from sqlalchemy import create_engine
from datetime import datetime
from faker import Faker
import random

user = "automato"
passw = "MySQLIsFun"
host = "automato.mysql.pythonanywhere-services.com"
database = "automato$schedulin"

db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
conn = db.connect()

now = datetime.now()

timetables_lst = [

    """INSERT INTO timetable (start_time, end_time, creation_date)
           VALUES ('09:00', '10:30', '{0}')""".format(now),
    """INSERT INTO timetable (start_time, end_time, creation_date)
           VALUES ('10:30', '12:00', '{0}')""".format(now),
    """INSERT INTO timetable (start_time, end_time, creation_date)
           VALUES ('12:00', '13:30', '{0}')""".format(now),
    """INSERT INTO timetable (start_time, end_time, creation_date)
           VALUES ('13:30', '15:00', '{0}')""".format(now),
    """INSERT INTO timetable (start_time, end_time, creation_date)
           VALUES ('15:00', '16:30', '{0}')""".format(now),
    """INSERT INTO timetable (start_time, end_time, creation_date)
           VALUES ('16:30', '18:00', '{0}')""".format(now),
    """INSERT INTO timetable (start_time, end_time, creation_date)
           VALUES ('18:00', '19:30', '{0}')""".format(now),
    """INSERT INTO timetable (start_time, end_time, creation_date)
           VALUES ('19:30', '21:00', '{0}')""".format(now),
    """INSERT INTO timetable (start_time, end_time, creation_date)
           VALUES ('21:00', '22:30', '{0}')""".format(now),

    """INSERT INTO timetable (start_time, end_time, creation_date)
           VALUES ('10:00', '22:00', '{0}')""".format(now),

    """INSERT INTO timetable (start_time, end_time, creation_date)
           VALUES ('10:00', '16:00', '{0}')""".format(now),
    """INSERT INTO timetable (start_time, end_time, creation_date)
           VALUES ('16:00', '22:00', '{0}')""".format(now),

    ]

resources_lst = [

    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (4, 'PADEL', '', 4, 0.50, 12, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (5, 'PADEL', '', 4, 0.75, 24, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (6, 'PADEL', '', 4, 0.75, 24, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (7, 'PADEL', '', 4, 1.75, 2, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type,
    description, max_pax, price, hours_in_advance, creation_date)
           VALUES (8, 'PADEL', '', 4, 0.75, 12, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (9, 'PADEL', '', 4, 1.75, 2, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (10, 'PADEL', '', 4, 2.50, 2, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (11, 'PADEL', '', 4, 2.50, 2, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (12, 'PADEL', '', 4, 1.75, 2, '{0}')""".format(now),


    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (14, 'PISCINA', '', 6, 0.00, 2, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (15, 'PISCINA', '', 6, 0.00, 2, '{0}')""".format(now),


    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (14, 'GIMNASIO', '', 6, 3.00, 2, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (15, 'GIMNASIO', '', 6, 5.00, 2, '{0}')""".format(now),

    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (13, 'SALA COMUN', '', 6, 5.00, 2, '{0}')""".format(now),

    ]

f = Faker()

status_lst = ["ACTIVE", "INACTIVE"]
names_lst = []
for num in range(180):
    name = f.name()
    names_lst.append(
        [
            name,
            name.lower().replace(" ", "."),
            random.choices(status_lst,
                weights = [90, 10], k = 1)[0]
        ])

users_lst = [

    """INSERT INTO user (name, email, status, creation_date)
           VALUES ('{0}', '{1}@mail.com', '{2}', '{3}')""" \
        .format(name[0], name[1], name[2], now) for name in names_lst
    ]

# USERS     - random.randint(8, 187)
# RESOURCE  - random.randint(5, 19)
# status    -
#     status_lst = ["CONFIRMED", "CANCELLED", "EXECUTED"]
#     random.choices(status_lst,
#          weights = [85, 13, 2], k = 1)[0]
# num_pax   - random.randint(1, 7)
# fake.date_between(start_date='-10y', end_date='+30y')

status_lst = ["CONFIRMED", "CANCELLED", "EXECUTED"]
reservations_lst = []
for num in range(4000):
    resource = random.randint(5, 18)
    user = random.randint(8, 187)
    num_pax = random.randint(1, 8)
    status = random.choices(status_lst,
          weights = [65, 33, 2], k = 1)[0]
    date = f.date_between(start_date = '-10y', end_date = '-8y')
    reservations_str = """INSERT INTO reservation (resource_id, user_id, start_time, num_pax, status, date, creation_date)
            VALUES ({0}, {1}, NULL, {2}, '{3}', '{4}', '{5}')""" \
            .format(resource, user, num_pax, status, date, now),
    reservations_lst.append(reservations_str)

#reservations_lst = [
#    """INSERT INTO reservation (resource_id, user_id, start_time, num_pax, status, date, creation_date)
#           VALUES (1, 1, '09:00:00', 2, 'CONFIRMED', '2022-10-31', '{0}')""".format(now),
#    ]

inserts_lst = [
    timetables_lst,
    resources_lst,
    users_lst,
    reservations_lst
]

for lst in inserts_lst:
    for t in lst:
        #print(t[0])
        conn.execute(t)

conn.close()

#SELECT
#    r.id AS reservation_id,
#    r.date AS reservation_date,
#    r.status AS reservation_status,
#    u.name AS user_name,
#    u.email AS user_email,
#    re.type AS resource_type,
#    re.price AS price,
#    t.start_time,
#    t.end_time
#FROM (
#    SELECT id, date, status, user_id, resource_id
#    FROM reservation) AS r
#LEFT JOIN (
#    SELECT id, name, email
#    FROM user) AS u
#ON r.user_id = u.id
#LEFT JOIN (
#    SELECT id, type, price, timetable_id
#    FROM resource) AS re
#ON r.resource_id = re.id
#LEFT JOIN (
#    SELECT id, start_time, end_time
#    FROM timetable) AS t
#ON re.timetable_id = t.id;

#ALTER TABLE reservation
#ADD date DATE;

#ALTER TABLE reservation
#MODIFY COLUMN start_time VARCHAR(20);