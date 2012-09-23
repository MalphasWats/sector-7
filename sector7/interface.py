import curses
import traceback

import celestials

class Canvas:
    screen = None
    size = (0, 0)
    colors = []
    
    def __init__(self, screen):
        self.screen = screen
        self.size = screen.getmaxyx()
        
    def addColor(self, color):
        self.colors.append(color)


def main_menu(screen):

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    
    canvas = Canvas(screen)
    canvas.addColor(curses.color_pair(0))
    canvas.addColor(curses.color_pair(2))
    canvas.addColor(curses.color_pair(1))

    while True:

        screen.clear()
        curses.curs_set(0)
        size = canvas.size
        screen.addstr(0, 0, " Sector 7", curses.A_REVERSE)
    
        screen.insnstr(" "*size[1], size[1], curses.A_REVERSE)
    
        screen.addstr(2, 0, "                    Sector 7 - Main Menu\n\n")
    
        #TODO: check for saved games
        screen.addstr("        1. Continue  [no games found]\n", curses.color_pair(1))
        screen.addstr("        2. New Game\n")
        screen.addstr("        3. Load Game [no games found]\n", curses.color_pair(1))
        screen.addstr("\n        q. Quit\n")
        
        event = screen.getch()
        if event == ord('q'): break
        elif event == ord('2'): start_new_game(canvas)
        
        
def start_new_game(canvas):
    #init game data
    universe = celestials.Universe()
    
    play(canvas, universe)
    
    
def play(canvas, universe):
    size = canvas.size

    while True:
        canvas.screen.clear()
    
        canvas.screen.addstr(0, 0, " Sector 7 | Day %s" % universe.day, curses.A_REVERSE)
        canvas.screen.insnstr(" "*size[1], size[1], curses.A_REVERSE)
    
        canvas.screen.addstr(size[0]-1, 0, " Commands: (b)uild | end (d)ay | (z)oom out | (q)uit", curses.A_REVERSE)
        canvas.screen.insnstr(" "*size[1], size[1], curses.A_REVERSE)
    
        universe.draw(canvas)
        
        event = canvas.screen.getch()
        if event == ord('q'):
            canvas.screen.addstr(size[0]-1, 0, " Are you sure you want to quit? (y)es / (n)o", curses.A_REVERSE)
            canvas.screen.insnstr(" "*size[1], size[1], curses.A_REVERSE)
            event2 = canvas.screen.getch()
            if event2 == ord('y'): break
            else: pass
        elif event == ord('b'):
            y = 2
            x = canvas.size[1]-32
            while True:
                universe.draw(canvas)
                draw_command_window(canvas, y, x)
                universe.current_view.build_options(canvas, y+1, x+2)
                
                event2 = canvas.screen.getch()
                if event2 == ord('x'): break
                else:
                    structure = universe.current_view.get_structure_to_build(event2)
                    if structure:
                        draw_command_window(canvas, y, x)
                        minerals, total_storage = universe.current_view.calculate_minerals()
                        structure.draw_build_options(canvas, y+1, x+2, minerals)
                        while True:
                            event3 = canvas.screen.getch()
                            if event3 == ord('x'): break
                            elif event3 == ord('b'):
                                universe.current_view.build_structure(structure)
                                break
        elif event == ord('d'):
            universe.advance_day()
        elif event == ord('z'): pass
        elif event == ord(' '): pass
        else:
            obj = universe.current_view.get_command_object(event)
            if obj:
                y = 2
                x = canvas.size[1]-32
                while True:
                    draw_command_window(canvas, y, x)
                    obj.draw_command_details(canvas, y+1, x+2)
                    event2 = canvas.screen.getch()
                    if event2 == ord('x'): break
                    elif event2 == ord('c') and obj.build_timer == 0:
                        while True:
                            draw_command_window(canvas, y, x)
                            obj.configure(canvas, y+1, x+2)
                            event3 = canvas.screen.getch()
                            if event3 == ord('x'): break
                            else:
                                #print event3
                                obj.handle_configuration_command(event3)
                
                
def draw_command_window(canvas, y, x):
    height = 18
    canvas.screen.addstr(y, x, " .---------------------------.")
    for rows in range(height):
        canvas.screen.addstr(rows+y+1, x, " |                           |")
        
    canvas.screen.addstr(height+y, x, " `--------------------e(x)it-'")
    canvas.screen.addstr(height+y+1, x, "                              ")
    
    