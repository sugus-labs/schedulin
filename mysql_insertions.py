from sqlalchemy import create_engine
from datetime import datetime
from faker import Faker
import random
from tqdm import tqdm

user = "schedulin"
passw = "MySQLIsFun"
host = "35.231.228.133"
database = "schedulin"

resources_dict = {  
    1: "09:00",
    2: "10:30",
    3: "12:00",
    4: "13:30",
    5: "15:00",
    6: "16:30",
    7: "18:00",
    8: "19:30",
    9: "21:00",
    14: "10:00",
    10: "10:00",
    12: "10:00",
    11: "16:00",
    13: "16:00",
}

db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}?autocommit=true' \
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
           VALUES (1, 'PADEL', '', 4, 0.50, 12, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (2, 'PADEL', '', 4, 0.75, 24, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (3, 'PADEL', '', 4, 0.75, 24, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (4, 'PADEL', '', 4, 1.75, 2, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (5, 'PADEL', '', 4, 0.75, 12, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (6, 'PADEL', '', 4, 1.75, 2, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (7, 'PADEL', '', 4, 2.50, 2, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (8, 'PADEL', '', 4, 2.50, 2, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (9, 'PADEL', '', 4, 1.75, 2, '{0}')""".format(now),


    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (11, 'PISCINA', '', 6, 0.00, 2, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (12, 'PISCINA', '', 6, 0.00, 2, '{0}')""".format(now),


    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (11, 'GIMNASIO', '', 6, 3.00, 2, '{0}')""".format(now),
    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (12, 'GIMNASIO', '', 6, 5.00, 2, '{0}')""".format(now),

    """INSERT INTO resource (timetable_id, type, description, max_pax, price, hours_in_advance, creation_date)
           VALUES (10, 'SALA COMUN', '', 6, 5.00, 2, '{0}')""".format(now),

    ]

f = Faker()

status_lst = ["ACTIVE", "INACTIVE"]
names_lst = []
for num in range(380):
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

inserts_dict = {
#    "timetables": timetables_lst,
#    "resources": resources_lst,
#    "users": users_lst,
#    "reservations": reservations_lst
}

for key, lst in inserts_dict.items():
    if key != "reservations":
        for t in lst:
            conn.execute(t)
    else:
        for t in lst:
            conn.execute(t[0])   

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
for num in tqdm(range(3000)):
    resource = random.randint(1, 14)
    user = random.randint(1, 380)
    num_pax = random.randint(1, 7)
    status = random.choices(status_lst,
          weights = [95, 3, 2], k = 1)[0]
    date = f.date_between(start_date = '-2y', end_date = 'now')
#    start_time = conn.execute("""
#        SELECT start_time
#        FROM (
#            SELECT id, timetable_id 
#            FROM resource 
#            WHERE id = {0}) AS R
#        INNER JOIN (
#            SELECT id, start_time
#            FROM timetable) AS T
#        ON R.timetable_id = T.id;
#        """.format(resource)).fetchone()["start_time"]
    start_time = resources_dict[resource]
    random_fail = random.choices([0, 1],
          weights = [2999, 1], k = 1)[0]
    if random_fail == 1:
        start_time = random.choices(["9:00", "10:00", "11:00", "17:00", "19:00"],
          weights = [2, 2, 2, 2, 2], k = 1)[0]   
    reservations_str = """INSERT INTO reservation (resource_id, user_id, start_time, num_pax, status, date, creation_date)
            VALUES ({0}, {1}, '{2}', {3}, '{4}', '{5}', '{6}')""" \
            .format(resource, user, start_time, num_pax, status, date, now)
    reservations_lst.append(reservations_str)

#reservations_lst = [
#    """INSERT INTO reservation (resource_id, user_id, start_time, num_pax, status, date, creation_date)
#           VALUES (1, 1, '09:00:00', 2, 'CONFIRMED', '2022-10-31', '{0}')""".format(now),
#    ]

inserts_dict = {
#    "timetables": timetables_lst,
#    "resources": resources_lst,
#    "users": users_lst,
    "reservations": reservations_lst
}

for key, lst in inserts_dict.items():
    for t in tqdm(lst):
        conn.execute(t)     

conn.close()
