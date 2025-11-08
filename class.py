class Passenger:
    def __init__(self, passenger_id, full_name, phone, email, rating):
        self.passenger_id = passenger_id
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.rating = rating

    def __repr__(self):
        return f"Passenger(passenger_id = '{self.passenger_id}',full_name='{self.full_name}', phone='{self.phone}', email='{self.email}', rating={self.rating})"
    
    def is_vip(self):
        if self.rating >= 4.8:
            return "Он вип"
        else:
            return "Он нормис"

    def get_masked_phone(self):
        start = self.phone[0:4]
        middle = "***"
        end = self.phone[7:]
        return start+middle+end

class Driver:
    def __init__(self, driver_id, full_name, phone, email, rating, balance, car_model, car_number):
        self.driver_id = driver_id
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.rating = rating
        self.balance = balance
        self.car_model = car_model
        self.car_number = car_number

    def __repr__(self):
        return f"Driver(driver_id = '{self.driver_id}', full_name='{self.full_name}', phone='{self.phone}', email='{self.email}', rating={self.rating}, balance='{self.balance}', car_model='{self.car_model}', car_number='{self.car_number}')"

class Support:
    def __init__(self, support_id, ticket, passenger_id, driver_id, full_name, phone, email, status, balance):
        self.support_id = support_id
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.rating = rating
        self.balance = balance
        self.status = status
        self.driver_id = driver_id
        self.passenger_id = passenger_id
        self.ticket = ticket

    def __repr__(self):
        return f"Support(support_id = '{self.support_id}', full_name='{self.full_name}', phone='{self.phone}', email='{self.email}', rating={self.rating}, balance='{self.balance}', status='{self.status}', driver_id='{self.driver_id}', passenger_id='{passenger_id}', ticket='{self.ticket}')"

class Ride:
    def __init__(self, ride_id, passenger_id, driver_id, start_point, end_point, price, created_at, completed_at, status):
        self.ride_id = ride_id
        self.passenger_id = passenger_id
        self.driver_id = driver_id
        self.start_point = start_point
        self.end_point = end_point
        self.price = price
        self.created_at = created_at
        self.completed_at = completed_at
        self.status = status

    def __repr__(self):
        return f"Ride(ride_id='{self.ride_id}', passenger_id='{self.passenger_id}', driver_id='{self.driver_id}', start_point='{self.start_point}', end_point='{self.end_point}', price='{self.price}', created_at='{self.created_at}', completed_at='{self.completed_at}', status='{self.status}')"


passenger = Passenger(1, "Иван Иванов", "+79213402130", "deb1l@mail.ru", 4.9)

print(f"{passenger}\n{passenger.is_vip()}\n{passenger.get_masked_phone()}")