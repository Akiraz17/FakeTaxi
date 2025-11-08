import sqlite3

conn = sqlite3.connect('database.db')

conn.row_factory = sqlite3.Row

cursor1 = conn.cursor()
cursor2 = conn.cursor()
cursor3 = conn.cursor()

cursor1.execute("SELECT * FROM passengers")
cursor2.execute("SELECT * FROM drivers")
cursor3.execute("SELECT * FROM rides")


passengers_row = cursor1.fetchall()
drivers_row = cursor2.fetchall()
rides_row = cursor3.fetchall()

print("======Информация о пассажирах======")

for row1 in passengers_row:
    print(f"ID: {row1['passenger_id']}, Name: {row1['full_name']}, Phone: {row1['phone']}, Email: {row1['email']}")

print("======Информация о водителях======")

for row2 in drivers_row:
    print(f"ID: {row2['driver_id']}, Name: {row2['full_name']}, Phone: {row2['phone']}, Email: {row2['email']}, Balance: {row2['balance']}, Car: {row2['car_model']}, Car Number: {row2['car_number']}")

print("======Информация о поездках======")

for row3 in rides_row:
    print(f"Passenger ID: {row3['passenger_id']}, Driver ID: {row3['driver_id']}, Start Point: {row3['start_point']}, End Point: {row3['end_point']}, Price: {row3['price']}, Status: {row3['status']}")


