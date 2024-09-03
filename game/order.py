from .truck import CargoType
import random
from datetime import datetime, timedelta

class Order:
    def __init__(self, start_city, end_city, cargo_type, amount, payment, deadline):
        self.start_city = start_city
        self.end_city = end_city
        self.cargo_type = cargo_type
        self.amount = amount  # in Tonnen
        self.payment = payment
        self.deadline = deadline
        self.is_completed = False

    def complete(self):
        self.is_completed = True

    def is_overdue(self, current_time):
        return current_time > self.deadline

    def calculate_penalty(self, current_time):
        if not self.is_overdue(current_time):
            return 0
        days_overdue = (current_time - self.deadline).days
        return min(self.payment * 0.1 * days_overdue, self.payment)

    @staticmethod
    def generate_random_order(cities, current_time):
        start_city = random.choice(cities)
        end_city = random.choice([city for city in cities if city != start_city])
        cargo_type = random.choice(list(CargoType))
        amount = random.randint(5, 25)  # zwischen 5 und 25 Tonnen
        payment = amount * random.randint(100, 200)  # 100-200 pro Tonne
        deadline = current_time + timedelta(days=random.randint(1, 5))

        return Order(start_city, end_city, cargo_type, amount, payment, deadline)

    def __str__(self):
        return f"Auftrag: {self.amount}t {self.cargo_type.value} von {self.start_city} nach {self.end_city}, Zahlung: {self.payment}"