from .base_screen import BaseScreen
import curses

class OrderScreen(BaseScreen):
    def display_orders(self, orders):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "AUFTRAEGE", curses.color_pair(2) | curses.A_BOLD)
        for i, order in enumerate(orders, start=1):
            self.stdscr.addstr(i+2, 2, f"{i}. {order}", curses.color_pair(2))
        self.stdscr.addstr(len(orders)+4, 2, "WAEHLE EINEN AUFTRAG (NUMMER) ODER 0 ZUM ZURUECK:", curses.color_pair(2))
        self.stdscr.refresh()
        return self.get_user_input()

    def display_assign_order_menu(self, order, available_trucks):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "AUFTRAG ZUWEISEN", curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(3, 2, f"AUFTRAG: {order}", curses.color_pair(1))
        self.stdscr.addstr(5, 2, "VERFÜGBARE LKWS:", curses.color_pair(1))
        for i, truck in enumerate(available_trucks, start=1):
            self.stdscr.addstr(i+5, 2, f"{i}. {truck}", curses.color_pair(1))
        self.stdscr.addstr(len(available_trucks)+7, 2, "WÄHLE EINEN LKW (0 ZUM ABBRECHEN):", curses.color_pair(1))
        self.stdscr.refresh()
        return self.get_user_input()