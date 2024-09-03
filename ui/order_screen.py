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

    def display_assign_order_menu(self, orders, trucks):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "AUFTRAG ZUWEISEN", curses.color_pair(2) | curses.A_BOLD)
        self.stdscr.addstr(3, 2, "VERFUEGBARE AUFTRAEGE:", curses.color_pair(2))
        for i, order in enumerate(orders, start=1):
            self.stdscr.addstr(i+3, 2, f"{i}. {order}", curses.color_pair(2))
        self.stdscr.addstr(len(orders)+5, 2, "VERFUEGBARE LKWS:", curses.color_pair(2))
        for i, truck in enumerate(trucks, start=1):
            self.stdscr.addstr(len(orders)+i+5, 2, f"{i}. {truck}", curses.color_pair(2))
        self.stdscr.addstr(len(orders)+len(trucks)+7, 2, "WAEHLE EINEN AUFTRAG UND DANN EINEN LKW (0 ZUM ABBRECHEN):", curses.color_pair(2))
        self.stdscr.refresh()
        order_choice = self.get_user_input()
        if order_choice == '0':
            return None, None
        self.stdscr.addstr(len(orders)+len(trucks)+9, 2, "WAEHLE EINEN LKW (0 ZUM ABBRECHEN):", curses.color_pair(2))
        self.stdscr.refresh()
        truck_choice = self.get_user_input()
        if truck_choice == '0':
            return None, None
        return order_choice, truck_choice