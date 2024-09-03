import random

class Driver:
    def __init__(self, name, salary, skill_level):
        self.name = name
        self.salary = salary
        self.skill_level = skill_level
        self.assigned_truck = None

    def assign_truck(self, truck):
        self.assigned_truck = truck

    def remove_truck(self):
        self.assigned_truck = None

    def __str__(self):
        return f"Fahrer: {self.name}, Fähigkeit: {self.skill_level}, Gehalt: {self.salary}"

    @staticmethod
    def generate_random_driver():
        names = ["Hans", "Fritz", "Klaus", "Peter", "Dieter", "Wolfgang", "Jürgen", "Uwe", "Ralf", "Günther"]
        name = random.choice(names)
        skill_level = random.randint(1, 10)
        salary = 2000 + (skill_level * 200)  # Grundgehalt 2000, plus 200 pro Fähigkeitspunkt
        return Driver(name, salary, skill_level)