import sqlite3
import re

def create_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passengers (
        passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        rating REAL DEFAULT 5.0
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS drivers (
        driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        rating REAL DEFAULT 5.0,
        car_model TEXT,
        car_number TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rides (
        ride_id INTEGER PRIMARY KEY AUTOINCREMENT,
        passenger_id INTEGER,
        driver_id INTEGER,
        pickup_location TEXT,
        dropoff_location TEXT,
        price REAL,
        status TEXT DEFAULT 'pending',
        ride_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (passenger_id) REFERENCES passengers (passenger_id),
        FOREIGN KEY (driver_id) REFERENCES drivers (driver_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS support_tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        passenger_id INTEGER,
        driver_id INTEGER,
        ride_id INTEGER,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT DEFAULT 'open',
        priority TEXT DEFAULT 'normal',
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        resolved_date DATETIME,
        response TEXT,
        FOREIGN KEY (passenger_id) REFERENCES passengers (passenger_id),
        FOREIGN KEY (driver_id) REFERENCES drivers (driver_id),
        FOREIGN KEY (ride_id) REFERENCES rides (ride_id)
    )
    ''')
    
    conn.commit()

def add_passenger(conn, full_name, phone, email):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO passengers (full_name, phone, email)
    VALUES (?, ?, ?)
    ''', (full_name, phone, email))
    conn.commit()
    print(f"Пассажир '{full_name}' добавлен")

def get_passengers(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passengers")
    passengers = cursor.fetchall()
    
    if not passengers:
        print("\nНет пассажиров в базе")
        return passengers
    
    print("\n========== ПАССАЖИРЫ ==========")
    for row in passengers:
        print(f"ID: {row['passenger_id']}, Имя: {row['full_name']}, Телефон: {row['phone']}, Email: {row['email']}, Рейтинг: {row['rating']}")
    return passengers

def update_passenger(conn, passenger_id, full_name, phone, email, rating):
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE passengers
    SET full_name = ?, phone = ?, email = ?, rating = ?
    WHERE passenger_id = ?
    ''', (full_name, phone, email, rating, passenger_id))
    conn.commit()
    print(f"Пассажир с ID {passenger_id} обновлен")

def delete_passenger(conn, passenger_id):
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM passengers
    WHERE passenger_id = ?
    ''', (passenger_id,))
    conn.commit()
    print(f"Пассажир с ID {passenger_id} удален")

def add_driver(conn, full_name, phone, email, car_model, car_number):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO drivers (full_name, phone, email, car_model, car_number)
    VALUES (?, ?, ?, ?, ?)
    ''', (full_name, phone, email, car_model, car_number))
    conn.commit()
    print(f"Водитель '{full_name}' добавлен")

def get_drivers(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM drivers")
    drivers = cursor.fetchall()
    
    if not drivers:
        print("\nНет водителей в базе")
        return drivers
    
    print("\n========== ВОДИТЕЛИ ==========")
    for row in drivers:
        print(f"ID: {row['driver_id']}, Имя: {row['full_name']}, Телефон: {row['phone']}, Автомобиль: {row['car_model']}, Номер: {row['car_number']}")
    return drivers

def update_driver(conn, driver_id, full_name, phone, email, rating, car_model, car_number):
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE drivers
    SET full_name = ?, phone = ?, email = ?, rating = ?, car_model = ?, car_number = ?
    WHERE driver_id = ?
    ''', (full_name, phone, email, rating, car_model, car_number, driver_id))
    conn.commit()
    print(f"Водитель с ID {driver_id} обновлен")

def delete_driver(conn, driver_id):
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM drivers
    WHERE driver_id = ?
    ''', (driver_id,))
    conn.commit()
    print(f"Водитель с ID {driver_id} удален")

def add_ride(conn, passenger_id, driver_id, pickup_location, dropoff_location, price, status='pending'):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO rides (passenger_id, driver_id, pickup_location, dropoff_location, price, status)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (passenger_id, driver_id, pickup_location, dropoff_location, price, status))
    conn.commit()
    print("Поездка добавлена")

def get_rides(conn, ride_id=None):
    cursor = conn.cursor()
    
    if ride_id:
        cursor.execute('''
        SELECT
            rides.*,
            passengers.full_name AS passenger_name,
            drivers.full_name AS driver_name
        FROM rides
        LEFT JOIN passengers ON rides.passenger_id = passengers.passenger_id
        LEFT JOIN drivers ON rides.driver_id = drivers.driver_id
        WHERE rides.ride_id = ?
        ''', (ride_id,))
        
        result = cursor.fetchone()
        if result:
            print(f"\nПоездка #{result['ride_id']}")
            print(f"Пассажир: {result['passenger_name']}")
            print(f"Водитель: {result['driver_name']}")
            print(f"Откуда: {result['pickup_location']}")
            print(f"Куда: {result['dropoff_location']}")
            print(f"Цена: {result['price']} руб.")
            print(f"Статус: {result['status']}")
        else:
            print(f"Поездка с ID {ride_id} не найдена")
        return result
    else:
        cursor.execute('''
        SELECT
            rides.*,
            passengers.full_name AS passenger_name,
            drivers.full_name AS driver_name
        FROM rides
        LEFT JOIN passengers ON rides.passenger_id = passengers.passenger_id
        LEFT JOIN drivers ON rides.driver_id = drivers.driver_id
        ''')
        
        rides = cursor.fetchall()
        
        if not rides:
            print("\nНет поездок в базе")
            return rides
        
        print("\n========== ПОЕЗДКИ ==========")
        for row in rides:
            print(f"ID: {row['ride_id']}, Пассажир: {row['passenger_name']}, Водитель: {row['driver_name']}, Цена: {row['price']} руб., Статус: {row['status']}")
        return rides

def update_ride_status(conn, ride_id, status):
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE rides
    SET status = ?
    WHERE ride_id = ?
    ''', (status, ride_id))
    conn.commit()
    print(f"Статус поездки {ride_id} изменен на {status}")

def delete_ride(conn, ride_id):
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM rides
    WHERE ride_id = ?
    ''', (ride_id,))
    conn.commit()
    print(f"Поездка {ride_id} удалена")

def create_support_ticket(conn, passenger_id, driver_id, ride_id, category, description, priority='normal'):
    cursor = conn.cursor()
    
    if passenger_id == '':
        passenger_id = None
    if driver_id == '':
        driver_id = None
    if ride_id == '':
        ride_id = None
        
    cursor.execute('''
    INSERT INTO support_tickets (passenger_id, driver_id, ride_id, category, description, priority, status)
    VALUES (?, ?, ?, ?, ?, ?, 'open')
    ''', (passenger_id, driver_id, ride_id, category, description, priority))
    conn.commit()
    
    ticket_id = cursor.lastrowid
    print(f"\nОбращение создано. Номер тикета: {ticket_id}")
    return ticket_id

def get_support_tickets(conn, status_filter=None):
    cursor = conn.cursor()
    
    if status_filter:
        cursor.execute('''
        SELECT 
            ticket_id,
            category,
            priority,
            status,
            passenger_id,
            driver_id,
            ride_id,
            description,
            response,
            created_date
        FROM support_tickets
        WHERE status = ?
        ORDER BY ticket_id DESC
        ''', (status_filter,))
    else:
        cursor.execute('''
        SELECT 
            ticket_id,
            category,
            priority,
            status,
            passenger_id,
            driver_id,
            ride_id,
            description,
            response,
            created_date
        FROM support_tickets
        ORDER BY ticket_id DESC
        ''')
    
    tickets = cursor.fetchall()
    
    if not tickets:
        print("\n========== ОБРАЩЕНИЯ В ПОДДЕРЖКУ ==========")
        if status_filter:
            print(f"Нет обращений со статусом '{status_filter}'")
        else:
            print("Нет обращений")
        return tickets
    
    print("\n========== ОБРАЩЕНИЯ В ПОДДЕРЖКУ ==========")
    for ticket in tickets:
        print(f"\nТикет #{ticket['ticket_id']}")
        print(f"Категория: {ticket['category']}")
        print(f"Приоритет: {ticket['priority']}")
        print(f"Статус: {ticket['status']}")
        
        if ticket['passenger_id']:
            cursor.execute('SELECT full_name FROM passengers WHERE passenger_id = ?', (ticket['passenger_id'],))
            passenger = cursor.fetchone()
            if passenger:
                print(f"Пассажир: {passenger['full_name']}")
                
        if ticket['driver_id']:
            cursor.execute('SELECT full_name FROM drivers WHERE driver_id = ?', (ticket['driver_id'],))
            driver = cursor.fetchone()
            if driver:
                print(f"Водитель: {driver['full_name']}")
                
        if ticket['ride_id']:
            print(f"Поездка: #{ticket['ride_id']}")
            
        print(f"Описание: {ticket['description']}")
        
        if ticket['response']:
            print(f"Ответ поддержки: {ticket['response']}")
            
        print(f"Дата создания: {ticket['created_date']}")
        print("-" * 40)
    
    return tickets

def respond_to_ticket(conn, ticket_id, response):
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE support_tickets
    SET response = ?, status = 'in_progress'
    WHERE ticket_id = ?
    ''', (response, ticket_id))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"Ответ на тикет #{ticket_id} добавлен")
    else:
        print(f"Тикет #{ticket_id} не найден")

def close_ticket(conn, ticket_id):
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE support_tickets
    SET status = 'closed', resolved_date = CURRENT_TIMESTAMP
    WHERE ticket_id = ?
    ''', (ticket_id,))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"Тикет #{ticket_id} закрыт")
    else:
        print(f"Тикет #{ticket_id} не найден")

def get_ticket_statistics(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM support_tickets")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM support_tickets WHERE status = 'open'")
    open_tickets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM support_tickets WHERE status = 'in_progress'")
    in_progress = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM support_tickets WHERE status = 'closed'")
    closed = cursor.fetchone()[0]
    
    cursor.execute('''
    SELECT category, COUNT(*) as count
    FROM support_tickets
    GROUP BY category
    ORDER BY count DESC
    ''')
    categories = cursor.fetchall()
    
    print("\n========== СТАТИСТИКА ПОДДЕРЖКИ ==========")
    print(f"Всего обращений: {total}")
    print(f"Открытых: {open_tickets}")
    print(f"В работе: {in_progress}")
    print(f"Закрытых: {closed}")
    
    if categories:
        print("\nПо категориям:")
        for cat in categories:
            print(f"  {cat['category']}: {cat['count']}")

def get_count_of_rides(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM rides")
    result = cursor.fetchone()[0]
    print(f"\nКоличество поездок: {result}")
    return result

def get_count_of_complete_rides(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM rides WHERE status = 'completed'")
    result = cursor.fetchone()[0]
    print(f"\nКоличество завершенных поездок: {result}")
    return result

def get_profit(conn):
    cursor = conn.cursor()
    cursor.execute('''
    SELECT SUM(price)
    FROM rides
    WHERE status = 'completed'
    ''')
    result = cursor.fetchone()[0]
    if result is None:
        result = 0
    print(f"Общая выручка: {result} рублей")
    return result

def get_arithmetic_mean_of_profit(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT AVG(price) FROM rides')
    result = cursor.fetchone()[0]
    if result is None:
        result = 0
    print(f"Средняя стоимость поездки: {result:.2f} рублей")
    return result

def max_and_min_price(conn):
    cursor = conn.cursor()
    cursor.execute('''
    SELECT
        MIN(price) AS min_price,
        MAX(price) AS max_price
    FROM rides
    ''')
    result = cursor.fetchone()
    
    if result['min_price'] is None:
        print("Нет данных о поездках")
    else:
        print(f"Минимальная стоимость: {result['min_price']} руб.")
        print(f"Максимальная стоимость: {result['max_price']} руб.")
    return result

def price_for_passenger(conn):
    cursor = conn.cursor()
    cursor.execute('''
    SELECT
        passengers.full_name,
        SUM(rides.price) AS priceofride
    FROM passengers
    LEFT JOIN rides ON passengers.passenger_id = rides.passenger_id
    GROUP BY passengers.passenger_id
    ORDER BY priceofride DESC
    ''')
    
    results = cursor.fetchall()
    
    if not results:
        print("\nНет данных")
        return
    
    print("\n========== ТРАТЫ ПАССАЖИРОВ ==========")
    for result in results:
        if result['priceofride']:
            print(f"{result['full_name']}: {result['priceofride']} рублей")
        else:
            print(f"{result['full_name']}: 0 рублей")

def who_is_rich(conn):
    cursor = conn.cursor()
    cursor.execute('''
    SELECT 
        passengers.full_name,
        SUM(rides.price) AS priceofdrive
    FROM rides
    INNER JOIN passengers ON passengers.passenger_id = rides.passenger_id
    GROUP BY passengers.passenger_id
    HAVING SUM(rides.price) > 1000
    ''')
    
    results = cursor.fetchall()
    
    if not results:
        print("\nНет пассажиров с тратами более 1000 рублей")
        return
    
    print("\n========== БОГАТЫЕ ПАССАЖИРЫ ==========")
    for result in results:
        print(f"Имя: {result['full_name']}, Потратил: {result['priceofdrive']} руб.")

def tariff(conn):
    cursor = conn.cursor()
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
    
    results = cursor.fetchall()
    
    if not results:
        print("\nНет данных о поездках")
        return
    
    print("\n========== ТАРИФЫ ==========")
    for result in results:
        print(f"Поездка #{result['ride_id']}: {result['price']} руб. - {result['category']}")

def show_menu():
    print("\n" + "="*50)
    print("СИСТЕМА УПРАВЛЕНИЯ ТАКСИ")
    print("="*50)
    print("\n--- ПАССАЖИРЫ ---")
    print("1. Показать пассажиров")
    print("2. Добавить пассажира")
    print("3. Изменить пассажира")
    print("4. Удалить пассажира")
    
    print("\n--- ВОДИТЕЛИ ---")
    print("5. Показать водителей")
    print("6. Добавить водителя")
    print("7. Изменить водителя")
    print("8. Удалить водителя")
    
    print("\n--- ПОЕЗДКИ ---")
    print("9. Показать поездки")
    print("10. Показать конкретную поездку")
    print("11. Добавить поездку")
    print("12. Изменить статус поездки")
    print("13. Удалить поездку")
    
    print("\n--- ПОДДЕРЖКА ---")
    print("14. Создать обращение")
    print("15. Показать все обращения")
    print("16. Показать открытые обращения")
    print("17. Ответить на обращение")
    print("18. Закрыть обращение")
    print("19. Статистика поддержки")
    
    print("\n--- СТАТИСТИКА ---")
    print("20. Количество поездок")
    print("21. Завершенные поездки")
    print("22. Общая выручка")
    print("23. Средняя стоимость")
    print("24. Мин/Макс цены")
    print("25. Траты пассажиров")
    print("26. Богатые пассажиры")
    print("27. Тарифы")
    
    print("\n0. Выход")
    print("="*50)

def main():
    conn = create_connection()
    create_tables(conn)
    
    while True:
        show_menu()
        choice = input("\nВыберите действие: ")
        
        if choice == '0':
            print("До свидания!")
            break
        
        elif choice == '1':
            get_passengers(conn)
        
        elif choice == '2':
            full_name = input("ФИО: ")
            phone = input("Телефон: ")
            email = input("Email: ")
            add_passenger(conn, full_name, phone, email)
        
        elif choice == '3':
            get_passengers(conn)
            try:
                passenger_id = int(input("ID пассажира: "))
                full_name = input("Новое ФИО: ")
                phone = input("Новый телефон: ")
                email = input("Новый email: ")
                rating = float(input("Новый рейтинг: "))
                update_passenger(conn, passenger_id, full_name, phone, email, rating)
            except ValueError:
                print("Неверный формат данных")
        
        elif choice == '4':
            get_passengers(conn)
            try:
                passenger_id = int(input("ID для удаления: "))
                delete_passenger(conn, passenger_id)
            except ValueError:
                print("Неверный ID")
        
        elif choice == '5':
            get_drivers(conn)
        
        elif choice == '6':
            full_name = input("ФИО: ")
            phone = input("Телефон: ")
            email = input("Email: ")
            car_model = input("Модель авто: ")
            car_number = input("Номер авто: ")
            add_driver(conn, full_name, phone, email, car_model, car_number)
        
        elif choice == '7':
            get_drivers(conn)
            try:
                driver_id = int(input("ID водителя: "))
                full_name = input("Новое ФИО: ")
                phone = input("Новый телефон: ")
                email = input("Новый email: ")
                rating = float(input("Новый рейтинг: "))
                car_model = input("Новая модель авто: ")
                car_number = input("Новый номер авто: ")
                update_driver(conn, driver_id, full_name, phone, email, rating, car_model, car_number)
            except ValueError:
                print("Неверный формат данных")
        
        elif choice == '8':
            get_drivers(conn)
            try:
                driver_id = int(input("ID для удаления: "))
                delete_driver(conn, driver_id)
            except ValueError:
                print("Неверный ID")
        
        elif choice == '9':
            get_rides(conn)
        
        elif choice == '10':
            try:
                ride_id = int(input("ID поездки: "))
                get_rides(conn, ride_id)
            except ValueError:
                print("Неверный ID")
        
        elif choice == '11':
            get_passengers(conn)
            try:
                passenger_id = int(input("ID пассажира: "))
                get_drivers(conn)
                driver_id = int(input("ID водителя: "))
                pickup = input("Откуда: ")
                dropoff = input("Куда: ")
                price = float(input("Цена: "))
                status = input("Статус (pending/active/completed/cancelled): ") or 'pending'
                add_ride(conn, passenger_id, driver_id, pickup, dropoff, price, status)
            except ValueError:
                print("Неверный формат данных")
        
        elif choice == '12':
            get_rides(conn)
            try:
                ride_id = int(input("ID поездки: "))
                status = input("Новый статус (pending/active/completed/cancelled): ")
                update_ride_status(conn, ride_id, status)
            except ValueError:
                print("Неверный ID")
        
        elif choice == '13':
            get_rides(conn)
            try:
                ride_id = int(input("ID для удаления: "))
                delete_ride(conn, ride_id)
            except ValueError:
                print("Неверный ID")
        
        elif choice == '14':
            print("\n--- СОЗДАНИЕ ОБРАЩЕНИЯ ---")
            print("От кого обращение?")
            print("1. От пассажира")
            print("2. От водителя")
            print("3. Общее обращение")
            sender_type = input("Выберите: ")
            
            passenger_id = None
            driver_id = None
            ride_id = None
            
            try:
                if sender_type == '1':
                    get_passengers(conn)
                    passenger_id = input("ID пассажира (или Enter для пропуска): ")
                    if passenger_id:
                        passenger_id = int(passenger_id)
                    else:
                        passenger_id = None
                        
                elif sender_type == '2':
                    get_drivers(conn)
                    driver_id = input("ID водителя (или Enter для пропуска): ")
                    if driver_id:
                        driver_id = int(driver_id)
                    else:
                        driver_id = None
                
                related_to_ride = input("Связано с поездкой? (да/нет): ")
                if related_to_ride.lower() in ['да', 'yes', 'y']:
                    get_rides(conn)
                    ride_id = input("ID поездки (или Enter для пропуска): ")
                    if ride_id:
                        ride_id = int(ride_id)
                    else:
                        ride_id = None
                
                print("\nКатегории: жалоба, вопрос, предложение, техническая_проблема, оплата, другое")
                category = input("Категория обращения: ")
                description = input("Описание проблемы: ")
                print("Приоритет: low, normal, high")
                priority = input("Приоритет (по умолчанию normal): ") or 'normal'
                
                create_support_ticket(conn, passenger_id, driver_id, ride_id, category, description, priority)
            except ValueError:
                print("Неверный формат данных")
        
        elif choice == '15':
            get_support_tickets(conn)
        
        elif choice == '16':
            get_support_tickets(conn, 'open')
        
        elif choice == '17':
            get_support_tickets(conn, 'open')
            try:
                ticket_id = int(input("ID тикета для ответа: "))
                response = input("Текст ответа: ")
                respond_to_ticket(conn, ticket_id, response)
            except ValueError:
                print("Неверный ID")
        
        elif choice == '18':
            get_support_tickets(conn, 'in_progress')
            try:
                ticket_id = int(input("ID тикета для закрытия: "))
                close_ticket(conn, ticket_id)
            except ValueError:
                print("Неверный ID")
        
        elif choice == '19':
            get_ticket_statistics(conn)
        
        elif choice == '20':
            get_count_of_rides(conn)
        
        elif choice == '21':
            get_count_of_complete_rides(conn)
        
        elif choice == '22':
            get_profit(conn)
        
        elif choice == '23':
            get_arithmetic_mean_of_profit(conn)
        
        elif choice == '24':
            max_and_min_price(conn)
        
        elif choice == '25':
            price_for_passenger(conn)
        
        elif choice == '26':
            who_is_rich(conn)
        
        elif choice == '27':
            tariff(conn)
        
        else:
            print("Неверный выбор!")
        
        input("\nНажмите Enter...")
    
    conn.close()

if __name__ == "__main__":
    main()