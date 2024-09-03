from .player import Player
from .company import Company
from .order import Order
from .truck import Truck, CargoType
from .driver import Driver
from ui.personnel_screen import PersonnelScreen
from ui.order_screen import OrderScreen
from ui.route_screen import RouteScreen  # Neue Import-Anweisung
import random
from datetime import date, timedelta
import pickle
import os

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.personnel_screen = PersonnelScreen(screen.stdscr)
        self.order_screen = OrderScreen(screen.stdscr)
        self.route_screen = RouteScreen(screen.stdscr)
        self.player = None
        self.company = None
        self.current_date = date(2000, 1, 1)
        self.daily_money = []
        self.cities = ["Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart"]

    def run(self):
        self.screen.display_loading_screen()
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
        self.generate_orders()
        self.screen.display_message(f"Neues Spiel gestartet! Willkommen, {player_name}!")
        self.game_loop()

    def game_loop(self):
        while True:
            self.screen.display_company_menu(self.company, self.current_date)
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
            elif choice == '7':
                self.start_day()
            elif choice == '8':
                self.view_accepted_orders()
            elif choice.lower() == 'q':
                break
            else:
                self.screen.display_message("Ungültige Eingabe. Bitte wähle 1-8 oder 'q' zum Beenden.")

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
                    self.save_game()
                else:
                    self.screen.display_message("NICHT GENUG GELD FUER DIESEN LKW!")
            else:
                self.screen.display_message("UNGUELTIGE EINGABE. BITTE WAEHLE EINE GUELTIGE NUMMER.")

    def sell_truck(self):
        self.screen.display_message("VERKAUFEN VON LKWS NOCH NICHT IMPLEMENTIERT.")

    def manage_orders(self):
        while True:
            choice = self.order_screen.display_orders(self.company.orders)
            if choice == '0':
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(self.company.orders):
                order = self.company.orders[int(choice) - 1]
                if self.company.accept_order(order):
                    self.screen.display_message(f"Auftrag angenommen und ins Backlog verschoben.")
                    self.company.orders.remove(order)  # Entferne den Auftrag aus der orders-Liste
                else:
                    self.screen.display_message("Fehler beim Annehmen des Auftrags.")
            else:
                self.screen.display_message("UNGUELTIGE EINGABE. BITTE WAEHLE EINE GUELTIGE NUMMER.")

    def plan_routes(self):
        while True:
            choice = self.route_screen.display_route_planning(self.company.trucks, self.company.backlog)
            if choice == '0':
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(self.company.trucks):
                truck = self.company.trucks[int(choice) - 1]
                self.assign_routes_to_truck(truck)
            else:
                self.screen.display_message("UNGUELTIGE EINGABE. BITTE WAEHLE EINE GUELTIGE NUMMER.")

    def assign_routes_to_truck(self, truck):
        if truck.driver is None or truck.driver.in_training:
            self.screen.display_message("DIESER LKW HAT KEINEN VERFÜGBAREN FAHRER!")
            return

        outbound_order = self.route_screen.select_order(self.company.backlog, "Hinweg")
        if outbound_order is None:
            return

        if outbound_order == "LEERFAHRT":
            inbound_orders = self.company.backlog
        else:
            inbound_orders = [order for order in self.company.backlog if order.start_city == outbound_order.end_city]
            inbound_orders.append("LEERFAHRT")

        inbound_order = self.route_screen.select_order(inbound_orders, "Rückweg")
        if inbound_order is None:
            return

        # Hinweg zuweisen
        if outbound_order != "LEERFAHRT":
            truck.current_order = outbound_order
            self.company.backlog.remove(outbound_order)
            self.company.assigned_orders.append(outbound_order)

        # Rückweg zuweisen
        if inbound_order != "LEERFAHRT":
            self.company.backlog.remove(inbound_order)
            self.company.assigned_orders.append(inbound_order)

        # Nachricht anzeigen
        outbound_msg = "Leerfahrt" if outbound_order == "LEERFAHRT" else f"Auftrag: {outbound_order}"
        inbound_msg = "Leerfahrt" if inbound_order == "LEERFAHRT" else f"Auftrag: {inbound_order}"
        self.screen.display_message(f"Dem LKW {truck.model} wurde zugewiesen:\nHinweg: {outbound_msg}\nRückweg: {inbound_msg}")

        self.save_game()

    def generate_orders(self):
        for _ in range(5):
            self.company.add_order(Order.generate_random_order(self.cities, self.current_date))

    def manage_personnel(self):
        while True:
            self.personnel_screen.display_personnel_menu(self.company.drivers)
            choice = self.personnel_screen.get_user_input()
            if choice == '1':
                self.hire_driver()
            elif choice == '2':
                self.fire_driver()
            elif choice == '3':
                self.assign_driver_to_truck()
            elif choice == '4':
                self.train_driver()
            elif choice == '0':
                break
            else:
                self.screen.display_message("UNGUELTIGE EINGABE. BITTE WAEHLE 1, 2, 3, 4 ODER 0.")

    def hire_driver(self):
        available_drivers = [Driver.generate_random_driver() for _ in range(3)]
        while True:
            choice = self.personnel_screen.display_hire_driver_menu(available_drivers, self.company.owner.money)
            if choice == '0':
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(available_drivers):
                selected_driver = available_drivers[int(choice) - 1]
                if self.company.hire_driver(selected_driver):
                    self.screen.display_message(f"FAHRER {selected_driver.name} EINGESTELLT!\n"
                                                f"Sicherheit: {selected_driver.safety}\n"
                                                f"Zuverlässigkeit: {selected_driver.reliability}\n"
                                                f"Tempo: {selected_driver.speed}")
                    self.save_game()
                    break
                else:
                    self.screen.display_message("NICHT GENUG GELD, UM DEN FAHRER EINZUSTELLEN!")
            else:
                self.screen.display_message("UNGUELTIGE EINGABE. BITTE WAEHLE EINE GUELTIGE NUMMER.")

    def fire_driver(self):
        if not self.company.drivers:
            self.screen.display_message("KEINE FAHRER ZUM ENTLASSEN!")
            return
        
        choice = self.personnel_screen.display_fire_driver_menu(self.company.drivers)
        if choice.isdigit() and 1 <= int(choice) <= len(self.company.drivers):
            driver = self.company.drivers[int(choice) - 1]
            if self.company.fire_driver(driver):
                self.screen.display_message(f"FAHRER {driver.name} ENTLASSEN!")
                self.save_game()
            else:
                self.screen.display_message("FEHLER BEIM ENTLASSEN DES FAHRERS!")
        else:
            self.screen.display_message("UNGUELTIGE EINGABE!")

    def assign_driver_to_truck(self):
        if not self.company.drivers or not self.company.trucks:
            self.screen.display_message("NICHT GENUG FAHRER ODER LKWS!")
            return
        
        driver_choice, truck_choice = self.personnel_screen.display_assign_driver_menu(self.company.drivers, self.company.trucks)
        if driver_choice is None or truck_choice is None:
            return
        elif driver_choice.isdigit() and 1 <= int(driver_choice) <= len(self.company.drivers):
            driver = self.company.drivers[int(driver_choice) - 1]
            if truck_choice.isdigit() and 1 <= int(truck_choice) <= len(self.company.trucks):
                truck = self.company.trucks[int(truck_choice) - 1]
                driver.assign_truck(truck)
                truck.assign_driver(driver)
                self.screen.display_message(f"FAHRER {driver.name} DEM LKW {truck.model} ZUGEWIESEN!")
                self.save_game()
            else:
                self.screen.display_message("UNGUELTIGE LKW-AUSWAHL!")
        else:
            self.screen.display_message("UNGUELTIGE FAHRER-AUSWAHL!")

    def train_driver(self):
        if not self.company.drivers:
            self.screen.display_message("KEINE FAHRER ZUM WEITERBILDEN!")
            return
        
        choice = self.personnel_screen.display_training_menu(self.company.drivers)
        if choice.isdigit() and 1 <= int(choice) <= len(self.company.drivers):
            driver = self.company.drivers[int(choice) - 1]
            training_cost = 5000  # Kosten für die Weiterbildung
            if self.company.owner.subtract_money(training_cost):
                driver.train()
                driver.in_training = True
                driver.training_days_left = 7
                self.screen.display_message(f"FAHRER {driver.name} BEFINDET SICH NUN IN WEITERBILDUNG FÜR 7 TAGE!")
                self.save_game()
            else:
                self.screen.display_message("NICHT GENUG GELD FÜR DIE WEITERBILDUNG!")
        else:
            self.screen.display_message("UNGUELTIGE EINGABE!")

    def view_finances(self):
        self.screen.display_message("Finanzübersicht noch nicht implementiert.")

    def perform_maintenance(self):
        self.screen.display_message("Wartung noch nicht implementiert.")

    def load_game(self):
        if os.path.exists('savegame.dat'):
            with open('savegame.dat', 'rb') as f:
                save_data = pickle.load(f)
            self.player = save_data['player']
            self.company = save_data['company']
            self.current_date = save_data['current_date']
            self.cities = save_data['cities']
            self.daily_money = save_data['daily_money']
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
            'current_date': self.current_date,
            'cities': self.cities,
            'daily_money': self.daily_money
        }
        with open('savegame.dat', 'wb') as f:
            pickle.dump(save_data, f)
        self.screen.display_message("SPIEL GESPEICHERT!")

    def start_day(self):
        self.screen.display_message("Tag wird simuliert...")
        self.simulate_day()
        self.current_date += timedelta(days=1)
        self.daily_money.append(self.company.owner.money)
        self.generate_new_drivers()
        self.generate_orders()
        self.save_game()

    def simulate_day(self):
        trips = []
        for driver in self.company.drivers:
            if driver.in_training:
                driver.training_days_left -= 1
                if driver.training_days_left == 0:
                    driver.in_training = False
                    self.screen.display_message(f"FAHRER {driver.name} HAT DIE WEITERBILDUNG ABGESCHLOSSEN!")

        for truck in self.company.trucks:
            if truck.driver and not truck.driver.in_training:
                if truck.current_order == "LEERFAHRT":
                    trips.append({
                        'truck': truck,
                        'start': "Depot",
                        'end': "Depot",
                        'empty': True,
                        'success': True
                    })
                    self.simulate_empty_trip(truck)
                elif truck.current_order:
                    success = self.simulate_trip(truck)
                    trips.append({
                        'truck': truck,
                        'start': truck.current_order.start_city,
                        'end': truck.current_order.end_city,
                        'empty': False,
                        'success': success,
                        'order': truck.current_order
                    })
                    if success:
                        payment = self.company.complete_order(truck.current_order, self.current_date)
                        self.screen.display_message(f"Auftrag abgeschlossen. Einnahmen: {payment}")
                        truck.current_order = None
                    else:
                        self.screen.display_message(f"Auftrag fehlgeschlagen: {truck.current_order}")
                        truck.current_order = None

        self.route_screen.display_animated_trips(trips)

    def simulate_empty_trip(self, truck):
        # Hier können Sie Logik für Leerfahrten implementieren, z.B. Kraftstoffverbrauch, aber kein Einkommen
        fuel_consumption = random.randint(50, 100)  # Beispiel: zufälliger Kraftstoffverbrauch
        truck.fuel -= fuel_consumption
        if truck.fuel < 0:
            truck.fuel = 0
        self.screen.display_message(f"LKW {truck.model} hat eine Leerfahrt durchgeführt. Kraftstoffverbrauch: {fuel_consumption}")

    def simulate_trip(self, truck):
        driver = truck.driver
        order = truck.current_order
        
        # Berechne die Wahrscheinlichkeit für eine erfolgreiche Fahrt
        success_chance = (driver.skill_level + driver.safety + driver.reliability) / 30.0
        
        return random.random() < success_chance

    def generate_new_drivers(self):
        pass