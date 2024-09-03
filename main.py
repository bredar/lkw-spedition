import curses
from ui.screen import Screen
from game.game import Game

def main(stdscr):
    screen = Screen(stdscr)
    game = Game(screen)
    game.run()

if __name__ == "__main__":
    curses.wrapper(main)