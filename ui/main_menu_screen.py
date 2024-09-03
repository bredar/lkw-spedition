from .base_screen import BaseScreen
import curses

class MainMenuScreen(BaseScreen):
    def display(self):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(2, 5, "LKW-SPEDITION SIMULATOR C64", curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(5, 5, "1. SPEDITION GRUENDEN", curses.color_pair(1))
        self.stdscr.addstr(6, 5, "2. SPIEL LADEN", curses.color_pair(1))
        self.stdscr.addstr(7, 5, "3. ANLEITUNG", curses.color_pair(1))
        self.stdscr.addstr(8, 5, "4. BEENDEN", curses.color_pair(1))
        self.stdscr.addstr(10, 5, "WAEHLE EINE OPTION (1-4):", curses.color_pair(1))
        self.stdscr.refresh()