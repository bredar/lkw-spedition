from .company import Company

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 200000  # Erhöhtes Startkapital auf 200.000

    def create_company(self, company_name):
        self.company = Company(company_name, self)

    def get_balance(self):
        return self.money

    def add_money(self, amount):
        self.money += amount

    def subtract_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        return False

    def __str__(self):
        return f"Spieler: {self.name}, Kontostand: {self.money}"