import curses
import time
from game.truck import CargoType

class Screen:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)  # Cursor ausblenden
        self.height, self.width = stdscr.getmaxyx()
        curses.start_color()
        curses.use_default_colors()
        
        # C64 Blau (Hintergrund)
        curses.init_color(curses.COLOR_BLUE, 0, 0, 1000)
        
        # C64 Hellblau (Text)
        curses.init_color(curses.COLOR_CYAN, 529, 843, 843)
        
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLUE)  # Hellblau auf Blau
        self.stdscr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)

    def display_loading_screen(self):
        self.stdscr.clear()
        self.draw_border()
        ascii_art = r"""
    _     _  ____      __    ____  ____  ____  ____  __  ____  __  __   __ _   ____  __  _  _  _  _  _     __   ____  __  ____    __  ___  __ _ 
    / \   / )(  _ \    /__\  (  _ \( ___)(  _ \(_  _)(  )(_  _)/  \(  ) (  ( \ / ___)(  )( \/ )/ )( \/ \   /  \ (_  _)/  \(  _ \  /  \/ __)(  / )
    ) (  / /  ) __/   /(__)\  )___/ )__)  )   / _)(_  )(   )( (  O ))(__/)(  ( \\___ \ )( / \/ \) \/ (/ (  (  O ) _)((  O ))   / (  O)\__ \ )  ( 
    \_)\/(_) (__)    (__)(__)(__) (____)(_)\_)(____)(__) (__) \__/(____)\__\_)(____/(__)\_)(_/\____/\_)   \__/ (__)  \__/(__\_)  \__/(___/(__\_)
        """
        self.stdscr.addstr(2, (self.width - len(ascii_art.split('\n')[1])) // 2, ascii_art, curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(self.height - 4, (self.width - 20) // 2, "BRED GAMES PRÄSENTIERT", curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(self.height - 2, (self.width - 20) // 2, "LÄDT...", curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.refresh()
        time.sleep(3)  # Zeige den Ladebildschirm für 3 Sekunden an

    def display_main_menu(self):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(2, 5, "LKW-SPEDITION SIMULATOR C64", curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(5, 5, "1. SPEDITION GRUENDEN", curses.color_pair(1))
        self.stdscr.addstr(6, 5, "2. SPIEL LADEN", curses.color_pair(1))
        self.stdscr.addstr(7, 5, "3. ANLEITUNG", curses.color_pair(1))
        self.stdscr.addstr(8, 5, "4. BEENDEN", curses.color_pair(1))
        self.stdscr.addstr(10, 5, "WAEHLE EINE OPTION (1-4):", curses.color_pair(1))
        self.stdscr.refresh()

    def display_company_menu(self, company):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, f"SPEDITION: {company.name:<20}", curses.color_pair(1))
        self.stdscr.addstr(1, 40, f"KONTO: {company.owner.money:<6}", curses.color_pair(1))
        self.stdscr.addstr(3, 2, "1. FUHRPARK", curses.color_pair(1))
        self.stdscr.addstr(4, 2, "2. PERSONAL", curses.color_pair(1))
        self.stdscr.addstr(5, 2, "3. FINANZEN", curses.color_pair(1))
        self.stdscr.addstr(3, 20, "4. AUFTRAEGE", curses.color_pair(1))
        self.stdscr.addstr(4, 20, "5. ROUTENPLANUNG", curses.color_pair(1))
        self.stdscr.addstr(5, 20, "6. WARTUNG", curses.color_pair(1))
        self.stdscr.addstr(7, 2, "NACHRICHTEN:", curses.color_pair(1))
        self.stdscr.addstr(8, 2, "NEUE AUFTRAEGE VERFUEGBAR", curses.color_pair(1))
        self.stdscr.addstr(10, 2, "BEFEHL:", curses.color_pair(1))
        self.stdscr.refresh()

    def draw_border(self):
        self.stdscr.border('|', '|', '-', '-', '+', '+', '+', '+')

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