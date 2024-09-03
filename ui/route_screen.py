from .base_screen import BaseScreen
import curses
import time

class RouteScreen(BaseScreen):
    def display_route_planning(self, trucks, backlog):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "ROUTENPLANUNG", curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(3, 2, "VERFÜGBARE LKWS:", curses.color_pair(1))
        for i, truck in enumerate(trucks, start=1):
            driver_info = f", Fahrer: {truck.driver.name}" if truck.driver else ", Kein Fahrer"
            status = "In Weiterbildung" if truck.driver and truck.driver.in_training else "Verfügbar"
            self.stdscr.addstr(i+3, 2, f"{i}. {truck}{driver_info} - Status: {status}", curses.color_pair(1))
        self.stdscr.addstr(len(trucks)+5, 2, "0. ZURÜCK", curses.color_pair(1))
        self.stdscr.addstr(len(trucks)+7, 2, "WÄHLE EINEN LKW FÜR DIE ROUTENPLANUNG (0 ZUM ABBRECHEN):", curses.color_pair(1))
        self.stdscr.refresh()
        return self.get_user_input()

    def select_order(self, backlog, direction):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, f"AUFTRAG FÜR {direction} AUSWÄHLEN", curses.color_pair(1) | curses.A_BOLD)
        for i, order in enumerate(backlog, start=1):
            self.stdscr.addstr(i+2, 2, f"{i}. {order}", curses.color_pair(1))
        self.stdscr.addstr(len(backlog)+4, 2, "L. LEERFAHRT", curses.color_pair(1))
        self.stdscr.addstr(len(backlog)+5, 2, "0. ZURÜCK", curses.color_pair(1))
        self.stdscr.addstr(len(backlog)+7, 2, "WÄHLE EINEN AUFTRAG, 'L' FÜR LEERFAHRT ODER '0' ZUM ABBRECHEN:", curses.color_pair(1))
        self.stdscr.refresh()
        choice = self.get_user_input()
        if choice.lower() == 'l':
            return "LEERFAHRT"
        elif choice.isdigit() and 1 <= int(choice) <= len(backlog):
            return backlog[int(choice) - 1]
        return None

    def display_animated_trips(self, trips):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(1, 2, "TAGESABLAUF", curses.color_pair(1) | curses.A_BOLD)
        
        max_y, max_x = self.stdscr.getmaxyx()
        road_y = max_y // 2
        self.stdscr.hline(road_y, 1, curses.ACS_HLINE, max_x - 2)

        for trip in trips:
            truck = trip['truck']
            start = trip['start']
            end = trip['end']
            is_empty = trip['empty']
            success = trip['success']

            self.stdscr.addstr(road_y - 2, 2, f"LKW: {truck.model}", curses.color_pair(1))
            self.stdscr.addstr(road_y - 1, 2, f"Von: {start} Nach: {end}", curses.color_pair(1))
            self.stdscr.addstr(road_y + 1, 2, "Leerfahrt" if is_empty else "Mit Ladung", curses.color_pair(1))

            for x in range(2, max_x - 3):
                self.stdscr.addch(road_y, x, '█')
                self.stdscr.refresh()
                time.sleep(0.05)  # Anpassbare Verzögerung für die Animation

            if is_empty:
                self.stdscr.addstr(road_y + 3, 2, "Leerfahrt abgeschlossen!", curses.color_pair(1))
            elif success:
                self.stdscr.addstr(road_y + 3, 2, "Auftrag erfolgreich abgeschlossen!", curses.color_pair(1))
            else:
                self.stdscr.addstr(road_y + 3, 2, "Probleme bei der Lieferung!", curses.color_pair(1))
            self.stdscr.refresh()
            time.sleep(1)  # Pause zwischen den Fahrten

        self.stdscr.addstr(max_y - 2, 2, "Drücken Sie eine Taste, um fortzufahren...", curses.color_pair(1))
        self.stdscr.refresh()
        self.stdscr.getch()