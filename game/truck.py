from enum import Enum

class CargoType(Enum):
    GENERAL = "Allgemeine Fracht"
    REFRIGERATED = "Kühlgut"
    LIQUID = "Flüssigkeiten"
    HAZARDOUS = "Gefahrgut"
    LIVESTOCK = "Lebendtiere"

class Truck:
    def __init__(self, model, capacity, fuel_efficiency, price, cargo_type):
        self.model = model
        self.capacity = capacity  # in Tonnen
        self.fuel_efficiency = fuel_efficiency  # Liter pro 100 km
        self.price = price
        self.cargo_type = cargo_type
        self.driver = None
        self.current_cargo = 0
        self.fuel = 100  # Startet mit vollem Tank
        self.current_order = None

    def assign_driver(self, driver):
        self.driver = driver

    def remove_driver(self):
        self.driver = None

    def load_cargo(self, amount, cargo_type):
        if self.cargo_type != cargo_type:
            return False
        if self.current_cargo > 0:
            return False  # LKW ist bereits beladen
        if self.current_cargo + amount <= self.capacity:
            self.current_cargo += amount
            return True
        return False

    def unload_cargo(self):
        unloaded = self.current_cargo
        self.current_cargo = 0
        return unloaded

    def refuel(self, amount):
        self.fuel += amount
        if self.fuel > 100:
            self.fuel = 100

    def drive(self, distance):
        fuel_needed = (distance / 100) * self.fuel_efficiency
        if fuel_needed <= self.fuel:
            self.fuel -= fuel_needed
            return True
        return False

    def assign_order(self, order):
        self.current_order = order

    def __str__(self):
        return f"LKW: {self.model}, Typ: {self.cargo_type.value}, Kapazität: {self.capacity}t, Treibstoff: {self.fuel}%"