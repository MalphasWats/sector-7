import random

import buildings
from minerals import Minerals

class Universe(object):

    def __init__(self):
        random.seed()
    
        self.day = 1
        
        self.sectors = []
        self.sectors.append(Sector(self))
        
        self.current_view = self.sectors[0].systems[0].astronomical_objects[0]
        self.current_view.init_starting_asteroid()
        
        self.building_tech_tree = [
            buildings.PowerPlant(None),
            buildings.Hydroponics(None),
            buildings.Accomodation(None),
            buildings.Refinery(None),
            buildings.StorageSilo(None),
            buildings.Factory(None),
            buildings.Laboratory(None),
        ]
        
        
    def draw(self, canvas):
        self.current_view.draw(canvas)
        
        
    def advance_day(self):
        self.day += 1
        for s in self.sectors:
            s.advance_day()
        
        
        
class Sector(object):

    def __init__(self, parent):
        self.parent = parent
        
        self.systems = []
        self.systems.append(System(self))
        
        self.name = 'Sector 7'
        
        
    def advance_day(self):
        for s in self.systems:
            s.advance_day()
        
        
    
class System(object):
    
    def __init__(self, parent):
        self.parent = parent
        self.name = self.generate_system_name()
        
        self.astronomical_objects = []
        self.astronomical_objects.append(Asteroid(self))
        
        
    def generate_system_name(self):
        return 'Solar System'
        
        
    def advance_day(self):
        for o in self.astronomical_objects:
            o.advance_day()
        
        
class Astronomical_Object(object):
    
    def __init__(self, parent):
        self.parent = parent
        
        self.name = self.generate_name()
        
        self.structures = []
        self.ships = []
        self.population = []
        self.minerals = Minerals('medium')
        
    
    def generate_name(self):
        return 'Unknown Object'
        
        
    def advance_day(self):
        output, draw, stored = self.calculate_power()
        if stored <= 0.0 and output < draw:
            for row in self.structures:
                for structure in row:
                    if (output < draw and
                        structure and 
                        structure.name != '' and 
                        structure.name != 'Power Plant' and 
                        structure.name != 'Command Centre'):
                            structure.status = 'inactive'
                    output, draw, stored = self.calculate_power()
                    
        for row in self.structures:
            for s in row:
                if s:
                    s.advance_day()
        
    
    def build_options(self, canvas, y, x):
        canvas.screen.addstr(y, x, "Select a building: ")
        
        universe = self.parent.parent.parent
        building_tech_tree = universe.building_tech_tree
        i = 0
        y += 2
        for b in building_tech_tree:
            b.draw(canvas, y, (x+1)+(i*5))
            i += 1
            if i > 4:
                i = 0
                y += 3
            
            
    def get_structure_to_build(self, structureChar):
        universe = self.parent.parent.parent
        building_tech_tree = universe.building_tech_tree
        for structure in building_tech_tree:
            if structure.command_key == structureChar:
                return structure.__class__(None)
                
        return None
        
        
    def build_structure(self, structure_to_build):
        minerals, total_storage = self.calculate_minerals()
        building_plot = None
        if minerals >= structure_to_build.build_cost:
            for row_index, row in enumerate(self.structures):
                for structure_index, structure in enumerate(row):
                    if structure and structure.name == '':
                        building_plot = (row_index, structure_index)
                        
            if building_plot:            
                self.structures[building_plot[0]][building_plot[1]] = structure_to_build.__class__(self)
                self.spend_minerals(structure_to_build.build_cost)
        
        
    def calculate_power(self):
        output = 0.0
        draw = 0.0
        stored = 0.0
        for row in self.structures:
            for structure in row:
                if structure:
                    if structure.power_consumption > 0.0 and structure.status == 'active':
                        draw += structure.power_consumption
                    elif structure.power_consumption < 0.0 and structure.status == 'active':
                        output += abs(structure.power_consumption)
                        stored += structure.power_stored
                
        return output, draw, stored
        
        
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
        
        
    def spend_minerals(self, minerals):
        for row in self.structures:
            for structure in row:
                if structure:
                    for mineral in structure.mineral_storage.quantity.keys():
                        if structure.mineral_storage.quantity[mineral] >= minerals.quantity[mineral]:
                            structure.mineral_storage.quantity[mineral] -= minerals.quantity[mineral]
                            minerals.quantity[mineral] = 0
                        else:
                            minerals.quantity[mineral] -= structure.mineral_storage.quantity[mineral]
                            structure.mineral_storage.quantity[mineral] = 0  
                        
        
        
        
    def get_command_object(self, command):
        for row in self.structures:
            for structure in row:
                if structure and structure.command_key == command:
                    return structure
                    
        return None
    
    
class Asteroid(Astronomical_Object):

    X_OFFSET = 25
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
        
        for row in self.structures:
            for structure in row:
                if structure:
                    structure.build_timer = 0
                    structure.status = 'active'
        
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
            
        self.draw_mineral_totals(canvas, 6, 1)#self.X_OFFSET+ (len(self.structures[0])*5)+5)
        
    
    def draw_mineral_totals(self, canvas, y, x):
        canvas.screen.addstr(y-2, x, "Minerals: ")
        minerals, total_storage = self.calculate_minerals()
        for index, mineral in enumerate(minerals.names):
            canvas.screen.addstr(y+index, x, "{:<10}: {:>8}".format(mineral, minerals.quantity[mineral]))
            
            
    def draw_random_rock(self, screen, y, x):
        screen.addstr(y, x, ".%.~.")
        screen.addstr(y+1, x, ".:.~=")
        screen.addstr(y+2, x, ";-%~.")
                    
                    
            
        
