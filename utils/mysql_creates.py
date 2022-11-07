from sqlalchemy import create_engine

user = "schedulin"
passw = "MySQLIsFun"
host = "35.231.228.133"
database = "schedulin"

db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
conn = db.connect()

#databases = conn.execute(
#    "SHOW DATABASES;"
#)

#for db in databases.fetchall():
#    print(db)

timetable_creation = """
    CREATE TABLE IF NOT EXISTS timetable (
        id INT AUTO_INCREMENT PRIMARY KEY,
        start_time VARCHAR(20),
        end_time VARCHAR(20),
        creation_date TIMESTAMP,
        modification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        deletion_date TIMESTAMP
    )  ENGINE=INNODB;
"""

resource_creation = """
    CREATE TABLE IF NOT EXISTS resource (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timetable_id INTEGER,
        type VARCHAR(255),
        description VARCHAR(2000),
        max_pax INTEGER,
        price DECIMAL(4, 2),
        hours_in_advance INTEGER,
        creation_date TIMESTAMP,
        modification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        deletion_date TIMESTAMP,
        FOREIGN KEY(timetable_id) REFERENCES timetable(id)
    )  ENGINE=INNODB;
"""

user_creation = """
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        status VARCHAR(255),
        creation_date TIMESTAMP,
        modification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        deletion_date TIMESTAMP
    )  ENGINE=INNODB;
"""

reservation_creation = """
    CREATE TABLE IF NOT EXISTS reservation (
        id INT AUTO_INCREMENT PRIMARY KEY,
        resource_id INTEGER,
        user_id INTEGER,
        start_time TIME,
        num_pax INTEGER,
        status VARCHAR(255),
        creation_date TIMESTAMP,
        modification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        deletion_date TIMESTAMP,
        date DATE,
        FOREIGN KEY(resource_id) REFERENCES resource(id),
        FOREIGN KEY(user_id) REFERENCES user(id)
    )  ENGINE=INNODB;
"""

conn.execute(timetable_creation)
conn.execute(resource_creation)
conn.execute(user_creation)
conn.execute(reservation_creation)
