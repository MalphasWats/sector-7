from minerals import Minerals

class Building:

    parent = None

    name = ''
    command_key = ord(' ')
    
    
    def __init__(self, parent):
        self.parent = parent
        
        self.power_consumption = 0.0
        self.power_stored = 0.0
        self.power_storage_max = 0.0
    
        self.algae_output = 0.0
        self.algae_stored = 0.0
        self.algae_storage_max = 0.0
    
        self.oxygen_output = 0.0
        self.oxygen_stored = 0.0
        self.oxygen_storage_max = 0.0
    
        self.mineral_storage = Minerals()
        self.mineral_storage_max = 0
        
        
    def draw(self, canvas, y, x):
        canvas.screen.addstr(y, x, ".---.", canvas.colors[1])
        canvas.screen.addstr(y+1, x, "|   |", canvas.colors[1])
        canvas.screen.addstr(y+2, x, "`___'", canvas.colors[1])
        
        
    def draw_command_details(self, canvas, y, x):
        canvas.screen.addstr(y, x, self.name)
        canvas.screen.addstr(y+2, x+2, "Power Draw:{:>5} MW".format(self.power_consumption))
        
        
        
class CommandCentre(Building):
    
    name = 'Command Centre'
    description = """ ...command centre desc... """
    
    command_key = ord('c')
    
    def __init__(self, parent):
        Building.__init__(self, parent)
    
        self.power_consumption = -1.0
        self.algae_output = 2.1
        self.oxygen_output = 1.3
    
        self.mineral_storage_max = 10000
    
        self.power_storage_max = 500.0
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "C", canvas.colors[1])
        
        
    def draw_command_details(self, canvas, y, x):
        Building.draw_command_details(self, canvas, y, x)
        
        canvas.screen.addstr(y+2, x+2, "Power Output: {:>5} MW".format(abs(self.power_consumption)))
        canvas.screen.addstr(y+3, x+2, "Algae Output: {:>5} Kg/d".format(self.algae_output))
        canvas.screen.addstr(y+4, x+2, "Oxygen Output:{:>5} Kg/d".format(self.oxygen_output))
        
        
class PowerPlant(Building):
    
    name = 'Power Plant'
    description = """ ...power plant desc... """
    
    command_key = ord('p')
    
    def __init__(self, parent):
        Building.__init__(self, parent)
    
        self.power_consumption = -6.0
        self.power_storage_max = 10000.0
    
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "P", canvas.colors[1])
        
        
    def draw_command_details(self, canvas, y, x):
        Building.draw_command_details(self, canvas, y, x)
        
        canvas.screen.addstr(y+2, x+2, "Power Output:{:>5} MW".format(abs(self.power_consumption)))

        canvas.screen.addstr(y+4, x+1, "Totals")
        total_power_output, total_power_draw = self.parent.calculate_power()
        
        canvas.screen.addstr(y+5, x+2, "Power Output:{:>5} MW".format(total_power_output))
        canvas.screen.addstr(y+6, x+2, "Power Draw:  {:>5} MW".format(total_power_draw-(total_power_draw*2)))
        power_balance = total_power_output - total_power_draw
        if power_balance < 0.0:
            canvas.screen.addstr(y+8, x+2, "Balance:     {:>5} MW".format(power_balance), canvas.colors[0])
        else:
            canvas.screen.addstr(y+8, x+2, "Balance:     {:>5} MW".format(power_balance))
        
        
        
class Hydroponics(Building):
    
    name = 'Hydroponics'
    description = """ ...hydroponics desc... """
    
    command_key = ord('h')
    
    def __init__(self, parent):
        Building.__init__(self, parent)
    
        self.power_consumption = 0.5
    
        self.algae_output = 10.3
        self.algae_storage_max = 500.0
    
        self.oxygen_output = 5.6 #0.6 per person per day
        self.oxygen_storage_max = 5000.0

    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "H", canvas.colors[1])
        
        
    def draw_command_details(self, canvas, y, x):
        Building.draw_command_details(self, canvas, y, x)
        
        canvas.screen.addstr(y+4, x+2, "Algae Output: {:>5} Kg/d".format(self.algae_output))
        canvas.screen.addstr(y+5, x+2, "Oxygen Output:{:>5} Kg/d".format(self.oxygen_output))
        
        canvas.screen.addstr(y+7, x+1, "Totals")
        total_algae_output, total_algae_consumption = self.parent.calculate_algae()
        total_oxygen_output, total_oxygen_consumption = self.parent.calculate_oxygen()
        
        canvas.screen.addstr(y+8, x+2, "Algae Output: {:>5} Kg/d".format(total_algae_output))
        canvas.screen.addstr(y+9, x+2, "Algae Used:   {:>5} Kg/d".format(total_algae_consumption))
        
        canvas.screen.addstr(y+10, x+2, "Oxygen Output:{:>5} Kg/d".format(total_oxygen_output))
        canvas.screen.addstr(y+11, x+2, "Oxygen Used:  {:>5} Kg/d".format(total_oxygen_consumption))
        
        
        
        
        
class Accomodation(Building):
    
    name = 'Accomodation'
    description = """ ...accomodation desc... """
    
    command_key = ord('a')
    
    def __init__(self, parent):
        Building.__init__(self, parent)
    
        self.power_consumption = 1.2
        
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "A", canvas.colors[1])
        
        
class Refinery(Building):
    
    name = 'Refinery'
    description = """ ...refinery desc... """
    
    command_key = ord('r')
    
    def __init__(self, parent):
        Building.__init__(self, parent)
    
        self.power_consumption = 3.9
    
        self.mineral_storage_max = 30000
        
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "R", canvas.colors[1])
        
        
class StorageSilo(Building):
    
    name = 'Storage Silo'
    description = """ ...storage silo desc... """
    
    command_key = ord('s')
    
    def __init__(self, parent):
        Building.__init__(self, parent)
    
        self.power_consumption = 0.3
    
        self.mineral_storage_max = 50000
        
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "S", canvas.colors[1])
        
        
class Factory(Building):
    
    name = 'Factory'
    description = """ ...factory desc... """
    
    command_key = ord('f')
    
    def __init__(self, parent):
        Building.__init__(self, parent)
    
        self.power_consumption = 5.8
        
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "F", canvas.colors[1])
        
        
class Laboratory(Building):
    
    name = 'Laboratory'
    description = """ ...laboratory desc... """
    
    command_key = ord('l')
    
    def __init__(self, parent):
        Building.__init__(self, parent)
    
        self.power_consumption = 4.6
        
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "L", canvas.colors[1])