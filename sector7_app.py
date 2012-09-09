import sector7.interface as interface
import curses

if __name__ == '__main__':

    curses.wrapper(interface.main_menu)