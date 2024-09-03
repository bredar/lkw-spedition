from .truck import Truck, CargoType
from .order import Order

class Company:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.trucks = []
        self.drivers = []
        self.orders = []
        self.completed_orders = []

    def buy_truck(self, model, capacity, fuel_efficiency, price, cargo_type):
        if self.owner.subtract_money(price):
            truck = Truck(model, capacity, fuel_efficiency, price, cargo_type)
            self.trucks.append(truck)
            return truck
        return None

    def sell_truck(self, truck):
        if truck in self.trucks:
            self.trucks.remove(truck)
            self.owner.add_money(truck.price * 0.7)  # 70% des ursprünglichen Preises
            return True
        return False

    def hire_driver(self, name, salary, skill_level):
        driver = Driver(name, salary, skill_level)
        self.drivers.append(driver)
        return driver

    def fire_driver(self, driver):
        if driver in self.drivers:
            self.drivers.remove(driver)
            return True
        return False

    def assign_driver_to_truck(self, driver, truck):
        if driver in self.drivers and truck in self.trucks:
            driver.assign_truck(truck)
            truck.assign_driver(driver)
            return True
        return False

    def add_order(self, order):
        self.orders.append(order)

    def complete_order(self, order, current_time):
        if order in self.orders:
            self.orders.remove(order)
            order.complete()
            penalty = order.calculate_penalty(current_time)
            final_payment = order.payment - penalty
            self.owner.add_money(final_payment)
            self.completed_orders.append(order)
            return final_payment
        return 0

    def get_available_trucks_for_order(self, order):
        return [truck for truck in self.trucks if truck.cargo_type == order.cargo_type and truck.capacity >= order.amount]

    def assign_order_to_truck(self, order, truck):
        if truck in self.get_available_trucks_for_order(order):
            return truck.load_cargo(order.amount, order.cargo_type)
        return False

    def get_active_orders(self):
        return [order for order in self.orders if not order.is_completed]

    def get_overdue_orders(self, current_time):
        return [order for order in self.orders if order.is_overdue(current_time)]

    def calculate_total_revenue(self):
        return sum(order.payment for order in self.completed_orders)

    def __str__(self):
        return f"Unternehmen: {self.name}, Besitzer: {self.owner.name}, LKWs: {len(self.trucks)}, Fahrer: {len(self.drivers)}, Aktive Aufträge: {len(self.get_active_orders())}"