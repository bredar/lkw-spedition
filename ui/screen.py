import curses
import time
from game.truck import CargoType
from .base_screen import BaseScreen
from .main_menu_screen import MainMenuScreen
from .company_menu_screen import CompanyMenuScreen
from .personnel_screen import PersonnelScreen
from .order_screen import OrderScreen

class Screen(BaseScreen):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.main_menu_screen = MainMenuScreen(stdscr)
        self.company_menu_screen = CompanyMenuScreen(stdscr)
        self.personnel_screen = PersonnelScreen(stdscr)
        self.order_screen = OrderScreen(stdscr)

    def display_loading_screen(self):
        self.stdscr.clear()
        self.draw_border()
        ascii_art = r"""
  _     _  __      __    ____  ____  ____  ____  __  ____  __  __   __ _  
 / \   / \(  )    /__\  (  _ \( ___)(  _ \(_  _)(  )(  _ \(  )(  ) (  ( \ 
( o ) ( o ))(__  /(__)\  )___/ )__)  )   / _)(_  )(  )___/ )( / (_/\/    /
 \_/   \_/(____)(__)(__)(__)  (____)(_)\_)(____)(__)(__)  (__)\_____\_)__)
        """
        lines = ascii_art.split('\n')
        start_y = max(0, (self.height - len(lines)) // 2)
        for i, line in enumerate(lines):
            if start_y + i < self.height:
                self.stdscr.addstr(start_y + i, max(0, (self.width - len(line)) // 2), line[:self.width-1], curses.color_pair(1) | curses.A_BOLD)
        
        if start_y + len(lines) + 2 < self.height:
            self.stdscr.addstr(start_y + len(lines) + 2, max(0, (self.width - 20) // 2), "BRED GAMES PRÄSENTIERT", curses.color_pair(1) | curses.A_BOLD)
        if start_y + len(lines) + 4 < self.height:
            self.stdscr.addstr(start_y + len(lines) + 4, max(0, (self.width - 20) // 2), "LÄDT...", curses.color_pair(1) | curses.A_BOLD)
        
        self.stdscr.refresh()
        time.sleep(3)  # Zeige den Ladebildschirm für 3 Sekunden an

    def display_main_menu(self):
        self.main_menu_screen.display()

    def display_company_menu(self, company, current_date):
        self.company_menu_screen.display(company, current_date)

    def display_fleet(self, trucks):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "FUHRPARK", curses.color_pair(1) | curses.A_BOLD)
        for i, truck in enumerate(trucks, start=1):
            self.stdscr.addstr(i+2, 2, f"{i}. {truck}", curses.color_pair(1))
        self.stdscr.addstr(len(trucks)+4, 2, "DRUECKE EINE TASTE ZUM FORTFAHREN...", curses.color_pair(1))
        self.stdscr.refresh()
        self.stdscr.getch()

    def display_orders(self, orders):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "AUFTRAEGE", curses.color_pair(1) | curses.A_BOLD)
        for i, order in enumerate(orders, start=1):
            self.stdscr.addstr(i+2, 2, f"{i}. {order}", curses.color_pair(1))
        self.stdscr.addstr(len(orders)+4, 2, "WAEHLE EINEN AUFTRAG (NUMMER) ODER 0 ZUM ZURUECK:", curses.color_pair(1))
        self.stdscr.refresh()

    def get_user_input(self):
        return self.stdscr.getkey()

    def display_message(self, message):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(self.height // 2, (self.width - len(message)) // 2, message, curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.refresh()
        self.stdscr.getch()

    def get_player_name(self):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(2, 2, "GIB DEINEN NAMEN EIN:", curses.color_pair(1))
        curses.echo()
        name = self.stdscr.getstr(3, 2, 20).decode('utf-8')
        curses.noecho()
        return name

    def get_company_name(self):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(2, 2, "GIB DEN NAMEN DEINER SPEDITION EIN:", curses.color_pair(1))
        curses.echo()
        name = self.stdscr.getstr(3, 2, 20).decode('utf-8')
        curses.noecho()
        return name

    def display_fleet_menu(self, trucks):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "FUHRPARK MANAGEMENT", curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(3, 2, "1. LKW KAUFEN", curses.color_pair(1))
        self.stdscr.addstr(4, 2, "2. LKW VERKAUFEN", curses.color_pair(1))
        self.stdscr.addstr(6, 2, "AKTUELLE LKWS:", curses.color_pair(1))
        for i, truck in enumerate(trucks, start=1):
            self.stdscr.addstr(i+6, 2, f"{truck}", curses.color_pair(1))
        self.stdscr.addstr(len(trucks)+8, 2, "0. ZURUECK", curses.color_pair(1))
        self.stdscr.addstr(len(trucks)+10, 2, "WAEHLE EINE OPTION:", curses.color_pair(1))
        self.stdscr.refresh()

    def display_truck_purchase_menu(self, available_trucks, player_money):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "LKW KAUFEN", curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(2, 2, f"VERFUEGBARES GELD: {player_money}", curses.color_pair(1))
        for i, truck in enumerate(available_trucks, start=1):
            self.stdscr.addstr(i+3, 2, f"{i}. {truck.model} - PREIS: {truck.price} - TYP: {truck.cargo_type.value}", curses.color_pair(1))
        self.stdscr.addstr(len(available_trucks)+5, 2, "0. ZURUECK", curses.color_pair(1))
        self.stdscr.addstr(len(available_trucks)+7, 2, "WAEHLE EINEN LKW ZUM KAUFEN (0 ZUM ABBRECHEN):", curses.color_pair(1))
        self.stdscr.refresh()
        return self.get_user_input()