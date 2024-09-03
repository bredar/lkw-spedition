from .base_screen import BaseScreen
import curses

class PersonnelScreen(BaseScreen):
    def display_personnel_menu(self, drivers):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "PERSONALVERWALTUNG", curses.color_pair(2) | curses.A_BOLD)
        self.stdscr.addstr(3, 2, "1. FAHRER EINSTELLEN", curses.color_pair(2))
        self.stdscr.addstr(4, 2, "2. FAHRER ENTLASSEN", curses.color_pair(2))
        self.stdscr.addstr(5, 2, "3. FAHRER LKW ZUWEISEN", curses.color_pair(2))
        self.stdscr.addstr(7, 2, "AKTUELLE FAHRER:", curses.color_pair(2))
        for i, driver in enumerate(drivers, start=1):
            self.stdscr.addstr(i+7, 2, f"{i}. {driver}", curses.color_pair(2))
        self.stdscr.addstr(len(drivers)+9, 2, "0. ZURUECK", curses.color_pair(2))
        self.stdscr.addstr(len(drivers)+11, 2, "WAEHLE EINE OPTION:", curses.color_pair(2))
        self.stdscr.refresh()

    def display_hire_driver_menu(self, available_drivers, company_money):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "FAHRER EINSTELLEN", curses.color_pair(2) | curses.A_BOLD)
        self.stdscr.addstr(2, 2, f"VERFUEGBARES GELD: {company_money}", curses.color_pair(2))
        for i, driver in enumerate(available_drivers, start=1):
            self.stdscr.addstr(i+3, 2, f"{i}. {driver}", curses.color_pair(2))
        self.stdscr.addstr(len(available_drivers)+5, 2, "0. ZURUECK", curses.color_pair(2))
        self.stdscr.addstr(len(available_drivers)+7, 2, "WAEHLE EINEN FAHRER ZUM EINSTELLEN (0 ZUM ABBRECHEN):", curses.color_pair(2))
        self.stdscr.refresh()
        return self.get_user_input()

    def display_fire_driver_menu(self, drivers):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "FAHRER ENTLASSEN", curses.color_pair(2) | curses.A_BOLD)
        for i, driver in enumerate(drivers, start=1):
            self.stdscr.addstr(i+2, 2, f"{i}. {driver}", curses.color_pair(2))
        self.stdscr.addstr(len(drivers)+4, 2, "WAEHLE EINEN FAHRER ZUM ENTLASSEN (0 ZUM ABBRECHEN):", curses.color_pair(2))
        self.stdscr.refresh()
        return self.get_user_input()

    def display_assign_driver_menu(self, drivers, trucks):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "FAHRER LKW ZUWEISEN", curses.color_pair(2) | curses.A_BOLD)
        self.stdscr.addstr(3, 2, "VERFUEGBARE FAHRER:", curses.color_pair(2))
        for i, driver in enumerate(drivers, start=1):
            self.stdscr.addstr(i+3, 2, f"{i}. {driver}", curses.color_pair(2))
        self.stdscr.addstr(len(drivers)+5, 2, "VERFUEGBARE LKWS:", curses.color_pair(2))
        for i, truck in enumerate(trucks, start=1):
            self.stdscr.addstr(len(drivers)+i+5, 2, f"{i}. {truck}", curses.color_pair(2))
        self.stdscr.addstr(len(drivers)+len(trucks)+7, 2, "WAEHLE EINEN FAHRER (0 ZUM ABBRECHEN):", curses.color_pair(2))
        self.stdscr.refresh()
        driver_choice = self.get_user_input()
        if driver_choice == '0':
            return None, None
        self.stdscr.addstr(len(drivers)+len(trucks)+9, 2, "WAEHLE EINEN LKW (0 ZUM ABBRECHEN):", curses.color_pair(2))
        self.stdscr.refresh()
        truck_choice = self.get_user_input()
        if truck_choice == '0':
            return None, None
        return driver_choice, truck_choice