import sqlite3

conn = sqlite3.connect('database.db')

conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS passengers (
        passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone TEXT NOT NULL UNIQUE,
        email TEXT UNIQUE,
        rating REAL DEFAULT 5.0
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS drivers (
               driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
               full_name TEXT NOT NULL,
               phone TEXT NOT NULL UNIQUE,
               email TEXT UNIQUE,
               rating REAL DEFAULT 5.0,
               balance REAL NOT NULL,
               status TEXT DEFAULT 'waiting' CHECK(status IN ('working', 'waiting', 'pending')),
               car_model TEXT,
               car_number TEXT
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS support (
               support_id INTEGER PRIMARY KEY AUTOINCREMENT,
               ticket TEXT,
               passenger_id INTEGER NOT NULL,
               driver_id INTEGER NOT NULL,
               full_name TEXT NOT NULL,
               phone TEXT NOT NULL UNIQUE,
               email TEXT UNIQUE,
               status TEXT DEFAULT 'waiting' CHECK(status IN ('working', 'waiting', 'pending')),
               balance REAL NOT NULL,
               FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE CASCADE,
               FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id) ON DELETE CASCADE
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS rides (
               ride_id INTEGER PRIMARY KEY AUTOINCREMENT,
               passenger_id INTEGER NOT NULL,
               driver_id INTEGER NOT NULL,
               support_id INTEGER, 
               start_point TEXT NOT NULL,
               end_point TEXT NOT NULL,
               price REAL NOT NULL,
               created_at TEXT DEFAULT (datetime('now','localtime')),
               completed_at TEXT,
               status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'in_progress', 'completed', 'cancelled')),
               FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE CASCADE,
               FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id) ON DELETE CASCADE,
               FOREIGN KEY (support_id) REFERENCES support(support_id) ON DELETE CASCADE
)
''')

passengers_data = [
        ('Иван Иванов', '+79001231239', 'ivan2007@gmail.com'),
        ('Пётр Петров', '+79321102401', 'petrushka@gmail.com'),
        ('Матвей Смирнов', '+78992101333', 'smirnov2005@mail.ru')
]

cursor.executemany('''
INSERT INTO passengers (full_name, phone, email)
VALUES (?, ?, ?)
''', passengers_data)


drivers_data = [
        ('Андрей Аллахов', '+78005343123', 'io123@mail.ru', 0.0, 'Lada Granta', 'A666УЕ152'),
        ('Алексей Лаков', '+78499999000', 'fioqwepwqr@outlook.com', 524.0, 'BMW M5', 'В004КО777')
]

cursor.executemany('''
INSERT INTO drivers (full_name, phone, email, balance, car_model, car_number)
VALUES (?, ?, ?, ?, ?, ?)
''', drivers_data)

rides_data = [
        ('1','1', 'Кащенко 5', 'Проспект Ленина 68', 6969, 'pending'),
        ('2','1', 'Казанское Шоссе 12к6', 'Фантастика', 320.12, 'completed'),
        ('2', '2', 'Минина 24к1', 'CyberX', 490, 'cancelled'),
        ('3','1', 'Парк Культуры', 'Улица Белинского', 2310, 'pending'),
        ('3','2', 'КиберPride', 'Метро Горьковская', 324, 'in_progress')
]

cursor.executemany('''
INSERT INTO rides (passenger_id, driver_id, start_point, end_point, price, status)
VALUES (?,?,?,?,?,?)
''', rides_data)

conn.commit()

conn.close()
