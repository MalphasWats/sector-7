import curses
import traceback

#screen = None

def main_menu(screen):
    screen.clear()
    curses.curs_set(0)
    size = screen.getmaxyx()
    screen.addstr(0, 0, " Sector 7", curses.A_REVERSE)
    
    screen.insnstr(" "*size[1], size[1], curses.A_REVERSE)
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    
    screen.addstr(2, 0, "                    Sector 7 - Main Menu\n\n")
    
    #TODO: check for saved games
    screen.addstr("        1. Continue  [no games found]\n", curses.color_pair(1))
    screen.addstr("        2. New Game\n")
    screen.addstr("        3. Load Game [no games found]\n", curses.color_pair(1))
        
    while True:
        event = screen.getch()
        if event == ord('q'): break
        elif event == ord('2'): start_new_game(screen)
        
        
def start_new_game(screen):
    #init game data
    sector = None
    
    play(screen, sector)
    
    
def play(screen, sector):
    screen.clear()
    
    size = screen.getmaxyx()
    screen.addstr(0, 0, " Sector 7 | Day x", curses.A_REVERSE)
    screen.insnstr(" "*size[1], size[1], curses.A_REVERSE)