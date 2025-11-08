import sqlite3

conn = sqlite3.connect('database.db')

conn.row_factory = sqlite3.Row

cursor = conn.cursor()

def add_passenger(full_name, phone, email):

    cursor.execute('''
    INSERT INTO passengers (full_name, phone, email)
    VALUES (?, ?, ?)
    ''', (full_name,phone,email))
    conn.commit()

def get_passengers():

    cursor.execute("SELECT * FROM passengers")
    passengers = cursor.fetchall()
    for row in passengers:
        print(f"ID: {row['passenger_id']}, Имя: {row['full_name']}, Телефон: {row['phone']}, Email: {row['email']}, Рейтинг: {row['rating']}")
    return passengers

def update_passenger(passenger_id, full_name, phone, email, rating):

    cursor.execute('''
    UPDATE passengers
    SET full_name = ?, phone = ?, email = ?, rating = ?
    WHERE passenger_id = ?
    ''', (full_name, phone, email, rating, passenger_id))
    
    conn.commit()

def delete_passenger(passenger_id):

    cursor.execute('''
    DELETE FROM passengers
    WHERE passenger_id = ?
    ''', (passenger_id,))

    conn.commit()

add_passenger('Артём Китов', '+79999999999', 'a.kitov@gmail.com')
get_passengers()
update_passenger(passenger_id=4, phone="+79954323000", full_name='Артём Китов', email='a.kitov@gmail.com', rating=5.0)
delete_passenger(2)
