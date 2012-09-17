import random

import buildings
from minerals import Minerals

class Universe:

    def __init__(self):
        random.seed()
    
        self.day = 1
        
        self.sectors = []
        self.sectors.append(Sector(self))
        
        self.current_view = self.sectors[0].systems[0].astronomical_objects[0]
        self.current_view.init_starting_asteroid()
        
        
    def draw(self, canvas):
        self.current_view.draw(canvas)
        
        
        
class Sector:

    def __init__(self, parent):
        self.parent = parent
        
        self.systems = []
        self.systems.append(System(self))
        
        self.name = 'Sector 7'
        
        
    
class System:
    
    def __init__(self, parent):
        self.parent = parent
        self.name = self.generate_system_name()
        
        self.astronomical_objects = []
        self.astronomical_objects.append(Asteroid(self))
        
        
    def generate_system_name(self):
        return 'Solar System'
        
        
class Astronomical_Object:
    
    def __init__(self, parent):
        self.parent = parent
        
        self.minerals = Minerals('medium')
        
        self.name = self.generate_name()
        
        self.structures = []
        self.ships = []
        self.population = []
        self.minerals = Minerals()
        
    
    def generate_name(self):
        return 'Unknown Object'
        
    
    def build_options(self, canvas, y, x):
        canvas.screen.addstr(y, x, "Select a building: ")
        
        
    def calculate_power(self):
        output = 0.0
        draw = 0.0
        for row in self.structures:
            for structure in row:
                if structure:
                    if structure.power_consumption > 0.0:
                        draw += structure.power_consumption
                    elif structure.power_consumption < 0.0:
                        output += abs(structure.power_consumption)
                
        return output, draw
        
        
    def calculate_algae(self):
        output = 0.0
        draw = 0.0
        for row in self.structures:
            for structure in row:
                if structure:
                    if structure.algae_output > 0.0:
                        output += structure.algae_output
                
        return output, draw
        
        
    def calculate_oxygen(self):
        output = 0.0
        draw = 0.0
        for row in self.structures:
            for structure in row:
                if structure:
                    if structure.oxygen_output > 0.0:
                        output += structure.oxygen_output
                
        return output, draw
        
    def calculate_minerals(self):
        minerals = Minerals()
        storage_total = 0
        for row in self.structures:
            for structure in row:
                if structure:
                    for mineral in structure.mineral_storage.quantity.keys():
                        minerals.quantity[mineral] += structure.mineral_storage.quantity[mineral]   
                        storage_total += structure.mineral_storage.quantity[mineral]
                        
        return minerals, storage_total
    
    
class Asteroid(Astronomical_Object):

    X_OFFSET = 18
    Y_OFFSET = 4

    def __init__(self, parent):
        Astronomical_Object.__init__(self, parent)
        self.name = self.generate_name()
        
        self.structures = [
            [None, None, None, None, None, None],
            [None, None, None, None, buildings.Building(self), None],
            [None, None, buildings.Building(self), buildings.Building(self), buildings.Building(self), None],
            [None, buildings.Building(self), buildings.CommandCentre(self), buildings.Building(self), None, None],
            [None, None, None, buildings.Building(self), None, None],
            [None, None, None, None, None, None]
        ]
        
    def init_starting_asteroid(self):
        self.structures = [
            [None, None, None, None, None, None],
            [None, None, None, None, buildings.Building(self), None],
            [None, None, buildings.Building(self), buildings.Hydroponics(self), buildings.Building(self), None],
            [None, buildings.Building(self), buildings.Accomodation(self), buildings.CommandCentre(self), None, None],
            [None, None, None, buildings.PowerPlant(self), None, None],
            [None, None, None, None, None, None]
        ]
        
        self.structures[3][3].mineral_storage = Minerals('starting_amount')
        
        
    def generate_name(self):
        return 'One';
        
        
    def draw(self, canvas):
        canvas.screen.addstr(2, 24, "Asteroid: %s" % self.name)
    
        row_index = 0
        col_index = 0
        for row in self.structures:
            for structure in row:
                y = self.Y_OFFSET+(row_index*3)
                x = self.X_OFFSET+(col_index*5)
                if structure:
                    structure.draw(canvas, y, x)
                else:
                    self.draw_random_rock(canvas.screen, y, x)
                col_index += 1
                    
            row_index += 1
            col_index = 0
            
        self.draw_mineral_totals(canvas, 6, self.X_OFFSET+ (len(self.structures[0])*5)+5)
        
    
    def draw_mineral_totals(self, canvas, y, x):
        canvas.screen.addstr(y-2, x, "Minerals: ")
        #print self.minerals.quantity
        minerals, total_storage = self.calculate_minerals()
        for index, mineral in enumerate(minerals.names):
            canvas.screen.addstr(y+index, x, "{:<11}: {:>12}".format(mineral, minerals.quantity[mineral]))
            
            
    def draw_random_rock(self, screen, y, x):
        screen.addstr(y, x, ".%.~.")
        screen.addstr(y+1, x, ".:.~=")
        screen.addstr(y+2, x, ";-%~.")
        
        
    def get_command_object(self, command):
        for row in self.structures:
            for structure in row:
                if structure and structure.command_key == command:
                    return structure
                    
        return None
                    
                    
            
        
