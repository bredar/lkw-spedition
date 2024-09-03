from .player import Player
from .company import Company
from .order import Order
from .truck import Truck, CargoType
import random
from datetime import datetime, timedelta
import pickle
import os

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = None
        self.company = None
        self.current_time = datetime.now()
        self.cities = ["Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart"]

    def run(self):
        while True:
            self.screen.display_main_menu()
            choice = self.screen.get_user_input()
            if choice == '1':
                self.start_new_game()
            elif choice == '2':
                self.load_game()
            elif choice == '3':
                self.show_instructions()
            elif choice == '4':
                break
            else:
                self.screen.display_message("Ungültige Eingabe. Bitte wähle 1-4.")

    def start_new_game(self):
        player_name = self.screen.get_player_name()
        company_name = self.screen.get_company_name()
        self.player = Player(player_name)
        self.company = Company(company_name, self.player)
        self.game_loop()

    def game_loop(self):
        while True:
            self.screen.display_company_menu(self.company)
            choice = self.screen.get_user_input()
            if choice == '1':
                self.manage_fleet()
            elif choice == '2':
                self.manage_personnel()
            elif choice == '3':
                self.view_finances()
            elif choice == '4':
                self.manage_orders()
            elif choice == '5':
                self.plan_routes()
            elif choice == '6':
                self.perform_maintenance()
            elif choice.lower() == 'q':
                break
            else:
                self.screen.display_message("Ungültige Eingabe. Bitte wähle 1-6 oder 'q' zum Beenden.")

    def manage_fleet(self):
        while True:
            self.screen.display_fleet_menu(self.company.trucks)
            choice = self.screen.get_user_input()
            if choice == '1':
                self.buy_truck()
            elif choice == '2':
                self.sell_truck()
            elif choice == '0':
                break
            else:
                self.screen.display_message("UNGUELTIGE EINGABE. BITTE WAEHLE 1, 2 ODER 0.")

    def buy_truck(self):
        available_trucks = [
            Truck("GENERAL CARGO 5000", 20, 30, 50000, CargoType.GENERAL),
            Truck("COOLFREEZE 3000", 15, 35, 70000, CargoType.REFRIGERATED),
            Truck("LIQUIDHAULER 2000", 25, 40, 80000, CargoType.LIQUID),
            Truck("HAZMAT SPECIAL", 18, 38, 90000, CargoType.HAZARDOUS),
            Truck("LIVESTOCK EXPRESS", 22, 32, 75000, CargoType.LIVESTOCK)
        ]
        
        while True:
            choice = self.screen.display_truck_purchase_menu(available_trucks, self.company.owner.money)
            if choice == '0':
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(available_trucks):
                selected_truck = available_trucks[int(choice) - 1]
                if self.company.buy_truck(selected_truck.model, selected_truck.capacity, 
                                          selected_truck.fuel_efficiency, selected_truck.price, 
                                          selected_truck.cargo_type):
                    self.screen.display_message(f"LKW {selected_truck.model} ERFOLGREICH GEKAUFT!")
                    self.save_game()  # Spiel nach dem Kauf speichern
                else:
                    self.screen.display_message("NICHT GENUG GELD FUER DIESEN LKW!")
            else:
                self.screen.display_message("UNGUELTIGE EINGABE. BITTE WAEHLE EINE GUELTIGE NUMMER.")

    def sell_truck(self):
        # Implementierung folgt
        self.screen.display_message("VERKAUFEN VON LKWS NOCH NICHT IMPLEMENTIERT.")

    def manage_orders(self):
        if not self.company.orders:
            self.generate_orders()
        self.screen.display_orders(self.company.orders)
        choice = self.screen.get_user_input()
        if choice.isdigit() and 0 < int(choice) <= len(self.company.orders):
            order = self.company.orders[int(choice) - 1]
            # Hier könnten wir die Logik zum Annehmen eines Auftrags implementieren

    def generate_orders(self):
        for _ in range(5):  # Generiere 5 zufällige Aufträge
            self.company.add_order(Order.generate_random_order(self.cities, self.current_time))

    # Platzhalter-Methoden für noch nicht implementierte Funktionen
    def manage_personnel(self):
        self.screen.display_message("Personalverwaltung noch nicht implementiert.")

    def view_finances(self):
        self.screen.display_message("Finanzübersicht noch nicht implementiert.")

    def plan_routes(self):
        self.screen.display_message("Routenplanung noch nicht implementiert.")

    def perform_maintenance(self):
        self.screen.display_message("Wartung noch nicht implementiert.")

    def load_game(self):
        if os.path.exists('savegame.dat'):
            with open('savegame.dat', 'rb') as f:
                save_data = pickle.load(f)
            self.player = save_data['player']
            self.company = save_data['company']
            self.current_time = save_data['current_time']
            self.cities = save_data['cities']
            self.screen.display_message("SPIEL ERFOLGREICH GELADEN!")
            self.game_loop()
        else:
            self.screen.display_message("KEIN SPIELSTAND GEFUNDEN!")

    def show_instructions(self):
        self.screen.display_message("Anleitung noch nicht implementiert.")

    def save_game(self):
        save_data = {
            'player': self.player,
            'company': self.company,
            'current_time': self.current_time,
            'cities': self.cities
        }
        with open('savegame.dat', 'wb') as f:
            pickle.dump(save_data, f)
        self.screen.display_message("SPIEL GESPEICHERT!")