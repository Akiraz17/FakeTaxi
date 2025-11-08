import sqlite3

conn = sqlite3.connect('database.db')

conn.row_factory = sqlite3.Row

cursor = conn.cursor()

def get_rides(ride_id):
    cursor.execute('''
    SELECT
        rides.*,
        passengers.full_name AS passenger_name,
        drivers.full_name AS driver_name
    FROM rides
    JOIN passengers ON rides.passenger_id = passengers.passenger_id
    JOIN drivers ON rides.driver_id = drivers.driver_id
    WHERE rides.ride_id = ?
    ''', (ride_id,))

    result = cursor.fetchone()

    return result


ride = get_rides(ride_id=4)

print(f"Поездка #{ride['ride_id']}")
print(f"Пассажир - {ride['passenger_name']}")
print(f"Водитель - {ride['driver_name']}")

def get_count_of_rides():
    cursor.execute("SELECT COUNT(*) FROM rides")

    result = cursor.fetchone()[0]

    print(f"\nКоличество поездок: {result}")

    return result

get_count_of_rides()


def get_count_of_complete_rides():
    cursor.execute("SELECT COUNT(*) FROM rides WHERE status = 'completed'")
    
    result = cursor.fetchone()[0]

    print(f"\nКоличество завершенных поездок: {result}\n")

    return result

get_count_of_complete_rides()


def get_profit():
    cursor.execute('''
    SELECT SUM(price)
    FROM RIDES
    WHERE status = 'completed'
    ''')

    result = cursor.fetchone()[0]

    print(f"Общая выручка за поездки: {result} рублей.\n")

    return result

get_profit()


def get_arithmetic_mean_of_profit():
    cursor.execute('''
    SELECT AVG(price)
    FROM rides
    ''')

    result = cursor.fetchone()[0]

    print(f"Среднее арифмитическое стоимости поездок: {result:.2f} рублей.\n")

    return result

get_arithmetic_mean_of_profit()

def max_and_min_price():
    cursor.execute('''
    SELECT
        MIN(price) AS min_price,
        MAX(price) AS max_price
    FROM rides
    ''')

    result = cursor.fetchone()

    print(f"Максимальная стоимость: {result['max_price']}")
    print(f"Минимальная стоимость: {result['min_price']}\n")

    return result


max_and_min_price()

def price_for_passenger():
    cursor.execute('''
    SELECT
        passengers.full_name,
        SUM(price) AS priceofride
    FROM passengers
    LEFT JOIN rides ON passengers.passenger_id = rides.passenger_id
    GROUP BY passengers.passenger_id
    ORDER BY priceofride DESC
    ''')

    for result in cursor.fetchall():
        print(f"{result['full_name']}: {result['priceofride']} рублей")

    return result


price_for_passenger()


def who_is_rich():
    cursor.execute('''
    SELECT 
        passengers.full_name,
        SUM(rides.price) AS priceofdrive
    FROM rides
    INNER JOIN passengers ON passengers.passenger_id = rides.passenger_id
    GROUP BY rides.price
    HAVING SUM(price) > 1000
    ''')

    print("\n======Самые богатые люди======\n")

    for result in cursor.fetchall():
        print(f"Имя: {result['full_name']}, Сколько заплатил: {result['priceofdrive']}")

    print("\n")
    return result

who_is_rich()

def tariff():
    cursor.execute('''
    SELECT
        price,
        ride_id,
        CASE
            WHEN price <= 400 THEN "Эконом"
            WHEN price > 400 AND price <= 1000 THEN "Комфорт"
            ELSE "Премиум"
        END AS category
    FROM rides
    ''')

    for result in cursor.fetchall():
        print(f"Поездка: #{result['ride_id']}, Стоимость: {result['price']}, Тариф: {result['category']}")

    print("\n")

    return result


tariff()

conn.close()