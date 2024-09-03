import curses

class BaseScreen:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)  # Cursor ausblenden
        self.height, self.width = stdscr.getmaxyx()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # C64 Blau auf Schwarz
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Weiß auf Blau
        self.stdscr.bkgd(' ', curses.color_pair(1))

    def draw_border(self):
        self.stdscr.border('|', '|', '-', '-', '+', '+', '+', '+')

    def get_user_input(self):
        return self.stdscr.getkey()

    def display_message(self, message):
        self.stdscr.clear()
        self.draw_border()
        self.stdscr.addstr(self.height // 2, (self.width - len(message)) // 2, message, curses.color_pair(2))
        self.stdscr.refresh()
        self.stdscr.getch()