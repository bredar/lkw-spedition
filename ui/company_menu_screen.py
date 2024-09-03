from .base_screen import BaseScreen
import curses

class CompanyMenuScreen(BaseScreen):
    def display(self, company, current_date):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, f"SPEDITION: {company.name:<20}", curses.color_pair(1))
        self.stdscr.addstr(1, 40, f"KONTO: {company.owner.money:<6}", curses.color_pair(1))
        self.stdscr.addstr(2, 2, f"DATUM: {current_date.strftime('%d.%m.%Y')}", curses.color_pair(1))
        self.stdscr.addstr(4, 2, "1. FUHRPARK", curses.color_pair(1))
        self.stdscr.addstr(5, 2, "2. PERSONAL", curses.color_pair(1))
        self.stdscr.addstr(6, 2, "3. FINANZEN", curses.color_pair(1))
        self.stdscr.addstr(4, 20, "4. AUFTRAEGE", curses.color_pair(1))
        self.stdscr.addstr(5, 20, "5. ROUTENPLANUNG", curses.color_pair(1))
        self.stdscr.addstr(6, 20, "6. WARTUNG", curses.color_pair(1))
        self.stdscr.addstr(8, 2, "7. TAG STARTEN", curses.color_pair(1))
        self.stdscr.addstr(9, 2, "8. ANGENOMMENE AUFTRAEGE", curses.color_pair(1))
        self.stdscr.addstr(11, 2, "NACHRICHTEN:", curses.color_pair(1))
        self.stdscr.addstr(12, 2, "NEUE AUFTRAEGE VERFUEGBAR", curses.color_pair(1))
        self.stdscr.addstr(14, 2, "BEFEHL:", curses.color_pair(1))
        self.stdscr.refresh()

    def display_accepted_orders(self, backlog):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "ANGENOMMENE AUFTRAEGE", curses.color_pair(1) | curses.A_BOLD)
        for i, order in enumerate(backlog, start=1):
            self.stdscr.addstr(i+2, 2, f"{i}. {order}", curses.color_pair(1))
        self.stdscr.addstr(len(backlog)+4, 2, "DRUECKE EINE TASTE ZUM FORTFAHREN...", curses.color_pair(1))
        self.stdscr.refresh()
        self.stdscr.getch()