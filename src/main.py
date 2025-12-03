import sqlite3
import re
from typing import Optional, List, Dict, Any

class TaxiDatabase:
    def __init__(self, db_path='database.db'):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS passengers (
            passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            rating REAL DEFAULT 5.0
        )
        ''')
        
        self.cursor.execute('''
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
        
        self.cursor.execute('''
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
        
        self.conn.commit()
    
    def validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone: str) -> bool:
        pattern = r'^[+]?[0-9]{10,15}$'
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
        return re.match(pattern, cleaned_phone) is not None
    
    def validate_rating(self, rating: float) -> bool:
        return 0.0 <= rating <= 5.0
    
    def add_passenger(self, full_name: str, phone: str, email: str) -> bool:
        try:
            if not self.validate_phone(phone):
                print("Некорректный формат телефона!")
                return False
            
            if email and not self.validate_email(email):
                print("Некорректный формат email!")
                return False
            
            self.cursor.execute('''
            INSERT INTO passengers (full_name, phone, email)
            VALUES (?, ?, ?)
            ''', (full_name, phone, email))
            self.conn.commit()
            print(f"Пассажир '{full_name}' успешно добавлен!")
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении пассажира: {e}")
            return False
    
    def get_passengers(self) -> List[Dict]:
        try:
            self.cursor.execute("SELECT * FROM passengers")
            passengers = self.cursor.fetchall()
            
            if not passengers:
                print("Список пассажиров пуст")
                return []
            
            print("\n========== СПИСОК ПАССАЖИРОВ ==========")
            for row in passengers:
                print(f"ID: {row['passenger_id']}, Имя: {row['full_name']}, "
                      f"Телефон: {row['phone']}, Email: {row['email']}, "
                      f"Рейтинг: {row['rating']:.1f}")
            return passengers
        except sqlite3.Error as e:
            print(f"Ошибка при получении пассажиров: {e}")
            return []
    
    def update_passenger(self, passenger_id: int, full_name: str, phone: str, 
                        email: str, rating: float) -> bool:
        try:
            if not self.validate_phone(phone):
                print("Некорректный формат телефона!")
                return False
            
            if email and not self.validate_email(email):
                print("Некорректный формат email!")
                return False
            
            if not self.validate_rating(rating):
                print("Рейтинг должен быть от 0 до 5!")
                return False
            
            self.cursor.execute('''
            UPDATE passengers
            SET full_name = ?, phone = ?, email = ?, rating = ?
            WHERE passenger_id = ?
            ''', (full_name, phone, email, rating, passenger_id))
            
            if self.cursor.rowcount == 0:
                print(f"Пассажир с ID {passenger_id} не найден!")
                return False
            
            self.conn.commit()
            print(f"Данные пассажира с ID {passenger_id} успешно обновлены!")
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении пассажира: {e}")
            return False
    
    def delete_passenger(self, passenger_id: int) -> bool:
        try:
            self.cursor.execute('''
            DELETE FROM passengers
            WHERE passenger_id = ?
            ''', (passenger_id,))
            
            if self.cursor.rowcount == 0:
                print(f"Пассажир с ID {passenger_id} не найден!")
                return False
            
            self.conn.commit()
            print(f"Пассажир с ID {passenger_id} успешно удален!")
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при удалении пассажира: {e}")
            return False
    
    def add_driver(self, full_name: str, phone: str, email: str, 
                  car_model: str, car_number: str) -> bool:
        try:
            if not self.validate_phone(phone):
                print("Некорректный формат телефона!")
                return False
            
            if email and not self.validate_email(email):
                print("Некорректный формат email!")
                return False
            
            self.cursor.execute('''
            INSERT INTO drivers (full_name, phone, email, car_model, car_number)
            VALUES (?, ?, ?, ?, ?)
            ''', (full_name, phone, email, car_model, car_number))
            self.conn.commit()
            print(f"Водитель '{full_name}' успешно добавлен!")
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении водителя: {e}")
            return False
    
    def get_drivers(self) -> List[Dict]:
        try:
            self.cursor.execute("SELECT * FROM drivers")
            drivers = self.cursor.fetchall()
            
            if not drivers:
                print("Список водителей пуст")
                return []
            
            print("\n========== СПИСОК ВОДИТЕЛЕЙ ==========")
            for row in drivers:
                print(f"ID: {row['driver_id']}, Имя: {row['full_name']}, "
                      f"Телефон: {row['phone']}, Email: {row['email']}, "
                      f"Рейтинг: {row['rating']:.1f}, Автомобиль: {row['car_model']}, "
                      f"Номер: {row['car_number']}")
            return drivers
        except sqlite3.Error as e:
            print(f"Ошибка при получении водителей: {e}")
            return []
    
    def update_driver(self, driver_id: int, full_name: str, phone: str, 
                     email: str, rating: float, car_model: str, car_number: str) -> bool:
        try:
            if not self.validate_phone(phone):
                print("Некорректный формат телефона!")
                return False
            
            if email and not self.validate_email(email):
                print("Некорректный формат email!")
                return False
            
            if not self.validate_rating(rating):
                print("Рейтинг должен быть от 0 до 5!")
                return False
            
            self.cursor.execute('''
            UPDATE drivers
            SET full_name = ?, phone = ?, email = ?, rating = ?, 
                car_model = ?, car_number = ?
            WHERE driver_id = ?
            ''', (full_name, phone, email, rating, car_model, car_number, driver_id))
            
            if self.cursor.rowcount == 0:
                print(f"Водитель с ID {driver_id} не найден!")
                return False
            
            self.conn.commit()
            print(f"Данные водителя с ID {driver_id} успешно обновлены!")
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении водителя: {e}")
            return False
    
    def delete_driver(self, driver_id: int) -> bool:
        try:
            self.cursor.execute('''
            DELETE FROM drivers
            WHERE driver_id = ?
            ''', (driver_id,))
            
            if self.cursor.rowcount == 0:
                print(f"Водитель с ID {driver_id} не найден!")
                return False
            
            self.conn.commit()
            print(f"Водитель с ID {driver_id} успешно удален!")
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при удалении водителя: {e}")
            return False
    
    def add_ride(self, passenger_id: int, driver_id: int, pickup_location: str, 
                 dropoff_location: str, price: float, status: str = 'pending') -> bool:
        try:
            if price < 0:
                print("Цена не может быть отрицательной!")
                return False
            
            if status not in ['pending', 'active', 'completed', 'cancelled']:
                print("Некорректный статус поездки!")
                return False
            
            self.cursor.execute('''
            INSERT INTO rides (passenger_id, driver_id, pickup_location, 
                             dropoff_location, price, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (passenger_id, driver_id, pickup_location, dropoff_location, price, status))
            self.conn.commit()
            print(f"Поездка успешно добавлена!")
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении поездки: {e}")
            return False
    
    def get_rides(self, ride_id: Optional[int] = None) -> List[Dict]:
        try:
            if ride_id:
                self.cursor.execute('''
                SELECT
                    rides.*,
                    passengers.full_name AS passenger_name,
                    drivers.full_name AS driver_name
                FROM rides
                LEFT JOIN passengers ON rides.passenger_id = passengers.passenger_id
                LEFT JOIN drivers ON rides.driver_id = drivers.driver_id
                WHERE rides.ride_id = ?
                ''', (ride_id,))
                
                result = self.cursor.fetchone()
                if result:
                    print(f"\n========== ПОЕЗДКА #{result['ride_id']} ==========")
                    print(f"Пассажир: {result['passenger_name']}")
                    print(f"Водитель: {result['driver_name']}")
                    print(f"Откуда: {result['pickup_location']}")
                    print(f"Куда: {result['dropoff_location']}")
                    print(f"Цена: {result['price']} руб.")
                    print(f"Статус: {result['status']}")
                    print(f"Дата: {result['ride_date']}")
                    return [result]
                else:
                    print(f"Поездка с ID {ride_id} не найдена!")
                    return []
            else:
                self.cursor.execute('''
                SELECT
                    rides.*,
                    passengers.full_name AS passenger_name,
                    drivers.full_name AS driver_name
                FROM rides
                LEFT JOIN passengers ON rides.passenger_id = passengers.passenger_id
                LEFT JOIN drivers ON rides.driver_id = drivers.driver_id
                ''')
                
                rides = self.cursor.fetchall()
                if not rides:
                    print("Список поездок пуст")
                    return []
                
                print("\n========== СПИСОК ПОЕЗДОК ==========")
                for row in rides:
                    print(f"ID: {row['ride_id']}, Пассажир: {row['passenger_name']}, "
                          f"Водитель: {row['driver_name']}, Цена: {row['price']} руб., "
                          f"Статус: {row['status']}")
                return rides
        except sqlite3.Error as e:
            print(f"Ошибка при получении поездок: {e}")
            return []
    
    def update_ride_status(self, ride_id: int, status: str) -> bool:
        try:
            if status not in ['pending', 'active', 'completed', 'cancelled']:
                print("Некорректный статус поездки!")
                return False
            
            self.cursor.execute('''
            UPDATE rides
            SET status = ?
            WHERE ride_id = ?
            ''', (status, ride_id))
            
            if self.cursor.rowcount == 0:
                print(f"Поездка с ID {ride_id} не найдена!")
                return False
            
            self.conn.commit()
            print(f"Статус поездки с ID {ride_id} успешно обновлен!")
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении статуса поездки: {e}")
            return False
    
    def delete_ride(self, ride_id: int) -> bool:
        try:
            self.cursor.execute('''
            DELETE FROM rides
            WHERE ride_id = ?
            ''', (ride_id,))
            
            if self.cursor.rowcount == 0:
                print(f"Поездка с ID {ride_id} не найдена!")
                return False
            
            self.conn.commit()
            print(f"Поездка с ID {ride_id} успешно удалена!")
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при удалении поездки: {e}")
            return False
    
    def get_count_of_rides(self) -> int:
        try:
            self.cursor.execute("SELECT COUNT(*) FROM rides")
            result = self.cursor.fetchone()[0]
            print(f"\nОбщее количество поездок: {result}")
            return result
        except sqlite3.Error as e:
            print(f"Ошибка при подсчете поездок: {e}")
            return 0
    
    def get_count_of_complete_rides(self) -> int:
        try:
            self.cursor.execute("SELECT COUNT(*) FROM rides WHERE status = 'completed'")
            result = self.cursor.fetchone()[0]
            print(f"Количество завершенных поездок: {result}")
            return result
        except sqlite3.Error as e:
            print(f"Ошибка при подсчете завершенных поездок: {e}")
            return 0
    
    def get_profit(self) -> float:
        try:
            self.cursor.execute('''
            SELECT SUM(price)
            FROM rides
            WHERE status = 'completed'
            ''')
            result = self.cursor.fetchone()[0]
            if result is None:
                result = 0
            print(f"Общая выручка за завершенные поездки: {result:.2f} рублей")
            return result
        except sqlite3.Error as e:
            print(f"Ошибка при подсчете выручки: {e}")
            return 0.0
    
    def get_arithmetic_mean_of_profit(self) -> float:
        try:
            self.cursor.execute('SELECT AVG(price) FROM rides')
            result = self.cursor.fetchone()[0]
            if result is None:
                result = 0
            print(f"Средняя стоимость поездки: {result:.2f} рублей")
            return result
        except sqlite3.Error as e:
            print(f"Ошибка при подсчете средней стоимости: {e}")
            return 0.0
    
    def max_and_min_price(self) -> Dict:
        try:
            self.cursor.execute('''
            SELECT
                MIN(price) AS min_price,
                MAX(price) AS max_price
            FROM rides
            ''')
            result = self.cursor.fetchone()
            
            if result['min_price'] is None or result['max_price'] is None:
                print("Нет данных о поездках")
                return {'min_price': 0, 'max_price': 0}
            
            print(f"Минимальная стоимость: {result['min_price']} руб.")
            print(f"Максимальная стоимость: {result['max_price']} руб.")
            return dict(result)
        except sqlite3.Error as e:
            print(f"Ошибка при получении мин/макс цен: {e}")
            return {'min_price': 0, 'max_price': 0}
    
    def price_for_passenger(self) -> List[Dict]:
        try:
            self.cursor.execute('''
            SELECT
                passengers.full_name,
                COALESCE(SUM(rides.price), 0) AS priceofride
            FROM passengers
            LEFT JOIN rides ON passengers.passenger_id = rides.passenger_id
            GROUP BY passengers.passenger_id
            ORDER BY priceofride DESC
            ''')
            
            results = self.cursor.fetchall()
            print("\n========== ТРАТЫ ПАССАЖИРОВ ==========")
            for result in results:
                print(f"{result['full_name']}: {result['priceofride']:.2f} рублей")
            
            return results
        except sqlite3.Error as e:
            print(f"Ошибка при получении трат пассажиров: {e}")
            return []
    
    def who_is_rich(self) -> List[Dict]:
        try:
            self.cursor.execute('''
            SELECT 
                passengers.full_name,
                SUM(rides.price) AS priceofdrive
            FROM rides
            INNER JOIN passengers ON passengers.passenger_id = rides.passenger_id
            GROUP BY passengers.passenger_id
            HAVING SUM(rides.price) > 1000
            ''')
            
            results = self.cursor.fetchall()
            
            if not results:
                print("\nНет пассажиров, потративших более 1000 рублей")
                return []
            
            print("\n========== VIP ПАССАЖИРЫ (траты > 1000 руб.) ==========")
            for result in results:
                print(f"Имя: {result['full_name']}, Потрачено: {result['priceofdrive']:.2f} руб.")
            
            return results
        except sqlite3.Error as e:
            print(f"Ошибка при получении VIP пассажиров: {e}")
            return []
    
    def tariff(self) -> List[Dict]:
        try:
            self.cursor.execute('''
            SELECT
                price,
                ride_id,
                CASE
                    WHEN price <= 400 THEN "Эконом"
                    WHEN price > 400 AND price <= 1000 THEN "Комфорт"
                    ELSE "Премиум"
                END AS category
            FROM rides
            ORDER BY price
            ''')
            
            results = self.cursor.fetchall()
            
            if not results:
                print("Нет данных о поездках")
                return []
            
            print("\n========== КАТЕГОРИИ ТАРИФОВ ==========")
            for result in results:
                print(f"Поездка #{result['ride_id']}: {result['price']} руб. - Тариф: {result['category']}")
            
            return results
        except sqlite3.Error as e:
            print(f"Ошибка при категоризации тарифов: {e}")
            return []
    
    def close(self):
        self.conn.close()


class TaxiApp:
    def __init__(self):
        self.db = TaxiDatabase()
    
    def display_menu(self):
        print("\n" + "="*50)
        print("       СИСТЕМА УПРАВЛЕНИЯ ТАКСИ")
        print("="*50)
        print("\n--- УПРАВЛЕНИЕ ПАССАЖИРАМИ ---")
        print("1.  Показать всех пассажиров")
        print("2.  Добавить пассажира")
        print("3.  Редактировать пассажира")
        print("4.  Удалить пассажира")
        
        print("\n--- УПРАВЛЕНИЕ ВОДИТЕЛЯМИ ---")
        print("5.  Показать всех водителей")
        print("6.  Добавить водителя")
        print("7.  Редактировать водителя")
        print("8.  Удалить водителя")
        
        print("\n--- УПРАВЛЕНИЕ ПОЕЗДКАМИ ---")
        print("9.  Показать все поездки")
        print("10. Показать конкретную поездку")
        print("11. Добавить поездку")
        print("12. Изменить статус поездки")
        print("13. Удалить поездку")
        
        print("\n--- СТАТИСТИКА И АНАЛИТИКА ---")
        print("14. Общее количество поездок")
        print("15. Количество завершенных поездок")
        print("16. Общая выручка")
        print("17. Средняя стоимость поездки")
        print("18. Мин/Макс стоимость поездок")
        print("19. Траты по пассажирам")
        print("20. VIP пассажиры (траты > 1000)")
        print("21. Категории тарифов")
        
        print("\n0. Выход")
        print("="*50)
    
    def get_input(self, prompt: str, required: bool = True) -> str:
        value = input(prompt).strip()
        if required and not value:
            print("Это поле обязательно для заполнения!")
            return self.get_input(prompt, required)
        return value
    
    def get_float_input(self, prompt: str) -> float:
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Введите корректное число!")
    
    def get_int_input(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Введите корректное целое число!")
    
    def handle_add_passenger(self):
        print("\n--- ДОБАВЛЕНИЕ ПАССАЖИРА ---")
        full_name = self.get_input("Введите ФИО: ")
        phone = self.get_input("Введите телефон: ")
        email = self.get_input("Введите email (или нажмите Enter для пропуска): ", required=False)
        
        self.db.add_passenger(full_name, phone, email or None)
    
    def handle_update_passenger(self):
        print("\n--- РЕДАКТИРОВАНИЕ ПАССАЖИРА ---")
        self.db.get_passengers()
        
        passenger_id = self.get_int_input("\nВведите ID пассажира для редактирования: ")
        full_name = self.get_input("Введите новое ФИО: ")
        phone = self.get_input("Введите новый телефон: ")
        email = self.get_input("Введите новый email (или нажмите Enter для пропуска): ", required=False)
        rating = self.get_float_input("Введите новый рейтинг (0-5): ")
        
        self.db.update_passenger(passenger_id, full_name, phone, email or None, rating)
    
    def handle_delete_passenger(self):
        print("\n--- УДАЛЕНИЕ ПАССАЖИРА ---")
        self.db.get_passengers()
        
        passenger_id = self.get_int_input("\nВведите ID пассажира для удаления: ")
        confirm = self.get_input(f"Вы уверены, что хотите удалить пассажира с ID {passenger_id}? (да/нет): ")
        
        if confirm.lower() in ['да', 'yes', 'y']:
            self.db.delete_passenger(passenger_id)
    
    def handle_add_driver(self):
        print("\n--- ДОБАВЛЕНИЕ ВОДИТЕЛЯ ---")
        full_name = self.get_input("Введите ФИО: ")
        phone = self.get_input("Введите телефон: ")
        email = self.get_input("Введите email (или нажмите Enter для пропуска): ", required=False)
        car_model = self.get_input("Введите модель автомобиля: ")
        car_number = self.get_input("Введите номер автомобиля: ")
        
        self.db.add_driver(full_name, phone, email or None, car_model, car_number)
    
    def handle_update_driver(self):
        print("\n--- РЕДАКТИРОВАНИЕ ВОДИТЕЛЯ ---")
        self.db.get_drivers()
        
        driver_id = self.get_int_input("\nВведите ID водителя для редактирования: ")
        full_name = self.get_input("Введите новое ФИО: ")
        phone = self.get_input("Введите новый телефон: ")
        email = self.get_input("Введите новый email (или нажмите Enter для пропуска): ", required=False)
        rating = self.get_float_input("Введите новый рейтинг (0-5): ")
        car_model = self.get_input("Введите новую модель автомобиля: ")
        car_number = self.get_input("Введите новый номер автомобиля: ")
        
        self.db.update_driver(driver_id, full_name, phone, email or None, rating, car_model, car_number)
    
    def handle_delete_driver(self):
        print("\n--- УДАЛЕНИЕ ВОДИТЕЛЯ ---")
        self.db.get_drivers()
        
        driver_id = self.get_int_input("\nВведите ID водителя для удаления: ")
        confirm = self.get_input(f"Вы уверены, что хотите удалить водителя с ID {driver_id}? (да/нет): ")
        
        if confirm.lower() in ['да', 'yes', 'y']:
            self.db.delete_driver(driver_id)
    
    def handle_add_ride(self):
        print("\n--- ДОБАВЛЕНИЕ ПОЕЗДКИ ---")
        
        print("\nДоступные пассажиры:")
        self.db.get_passengers()
        passenger_id = self.get_int_input("\nВведите ID пассажира: ")
        
        print("\nДоступные водители:")
        self.db.get_drivers()
        driver_id = self.get_int_input("\nВведите ID водителя: ")
        
        pickup_location = self.get_input("Введите адрес посадки: ")
        dropoff_location = self.get_input("Введите адрес высадки: ")
        price = self.get_float_input("Введите стоимость поездки: ")
        
        print("\nДоступные статусы: pending, active, completed, cancelled")
        status = self.get_input("Введите статус (или нажмите Enter для 'pending'): ", required=False) or 'pending'
        
        self.db.add_ride(passenger_id, driver_id, pickup_location, dropoff_location, price, status)
    
    def handle_update_ride_status(self):
        print("\n--- ИЗМЕНЕНИЕ СТАТУСА ПОЕЗДКИ ---")
        self.db.get_rides()
        
        ride_id = self.get_int_input("\nВведите ID поездки: ")
        print("\nДоступные статусы: pending, active, completed, cancelled")
        status = self.get_input("Введите новый статус: ")
        
        self.db.update_ride_status(ride_id, status)
    
    def handle_delete_ride(self):
        print("\n--- УДАЛЕНИЕ ПОЕЗДКИ ---")
        self.db.get_rides()
        
        ride_id = self.get_int_input("\nВведите ID поездки для удаления: ")
        confirm = self.get_input(f"Вы уверены, что хотите удалить поездку с ID {ride_id}? (да/нет): ")
        
        if confirm.lower() in ['да', 'yes', 'y']:
            self.db.delete_ride(ride_id)
    
    def handle_show_specific_ride(self):
        ride_id = self.get_int_input("Введите ID поездки: ")
        self.db.get_rides(ride_id)
    
    def run(self):
        print("\nДобро пожаловать в систему управления такси!")
        
        while True:
            try:
                self.display_menu()
                choice = self.get_input("\nВыберите действие: ")
                
                if choice == '0':
                    print("\nДо свидания!")
                    self.db.close()
                    break
                
                elif choice == '1':
                    self.db.get_passengers()
                elif choice == '2':
                    self.handle_add_passenger()
                elif choice == '3':
                    self.handle_update_passenger()
                elif choice == '4':
                    self.handle_delete_passenger()
                
                elif choice == '5':
                    self.db.get_drivers()
                elif choice == '6':
                    self.handle_add_driver()
                elif choice == '7':
                    self.handle_update_driver()
                elif choice == '8':
                    self.handle_delete_driver()
                
                elif choice == '9':
                    self.db.get_rides()
                elif choice == '10':
                    self.handle_show_specific_ride()
                elif choice == '11':
                    self.handle_add_ride()
                elif choice == '12':
                    self.handle_update_ride_status()
                elif choice == '13':
                    self.handle_delete_ride()
                
                elif choice == '14':
                    self.db.get_count_of_rides()
                elif choice == '15':
                    self.db.get_count_of_complete_rides()
                elif choice == '16':
                    self.db.get_profit()
                elif choice == '17':
                    self.db.get_arithmetic_mean_of_profit()
                elif choice == '18':
                    self.db.max_and_min_price()
                elif choice == '19':
                    self.db.price_for_passenger()
                elif choice == '20':
                    self.db.who_is_rich()
                elif choice == '21':
                    self.db.tariff()
                
                else:
                    print("Неверный выбор! Попробуйте снова.")
                
                input("\nНажмите Enter для продолжения...")
                
            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем. До свидания!")
                self.db.close()
                break
            except Exception as e:
                print(f"\nПроизошла ошибка: {e}")
                input("\nНажмите Enter для продолжения...")


def main():
    app = TaxiApp()
    app.run()


if __name__ == "__main__":
    main()