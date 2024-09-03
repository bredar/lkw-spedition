import random

class Driver:
    def __init__(self, name, salary, skill_level, safety, reliability, speed):
        self.name = name
        self.salary = salary
        self.skill_level = skill_level
        self.safety = safety  # Fahrsicherheit (1-10)
        self.reliability = reliability  # Zuverlässigkeit (1-10)
        self.speed = speed  # Fahrtempo (1-10)
        self.assigned_truck = None
        self.in_training = False
        self.training_days_left = 0

    def assign_truck(self, truck):
        self.assigned_truck = truck

    def remove_truck(self):
        self.assigned_truck = None

    def __str__(self):
        assigned = f", LKW: {self.assigned_truck.model}" if self.assigned_truck else ", Nicht zugewiesen"
        return f"Fahrer: {self.name}, Fähigkeit: {self.skill_level}, Gehalt: {self.salary}, Sicherheit: {self.safety}, Zuverlässigkeit: {self.reliability}, Tempo: {self.speed}{assigned}"

    @staticmethod
    def generate_random_driver():
        names = ["Hans", "Fritz", "Klaus", "Peter", "Dieter", "Wolfgang", "Jürgen", "Uwe", "Ralf", "Günther"]
        name = random.choice(names)
        skill_level = random.randint(1, 10)
        safety = random.randint(1, 10)
        reliability = random.randint(1, 10)
        speed = random.randint(1, 10)
        salary = 2000 + (skill_level * 200) + (safety * 100) + (reliability * 100) + (speed * 100)
        return Driver(name, salary, skill_level, safety, reliability, speed)

    def train(self):
        self.skill_level = min(10, self.skill_level + 1)
        self.safety = min(10, self.safety + 1)
        self.reliability = min(10, self.reliability + 1)
        self.speed = min(10, self.speed + 1)
        self.salary = int(self.salary * 1.1)  # 10% Gehaltserhöhung nach der Weiterbildung