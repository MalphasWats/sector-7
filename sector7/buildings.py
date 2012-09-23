from minerals import Minerals

class Building(object):

    parent = None
    build_time = 0

    name = ''
    command_key = ord(' ')
    
    def __init__(self, parent):
        
        if parent:
            self.parent = parent
            self.build_timer = self.build_time
        else:
            self.build_timer = 0
            
        self.build_cost = Minerals(None, 0, 0, 0, 0, 0, 0, 0)
        
        self.status = 'inactive'
        
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
        
        
    def advance_day(self):
        if self.build_timer > 0:
            self.build_timer -= 1
            
            if self.build_timer == 0:
                self.status = 'active'
                
                
    def calculate_mineral_storage_total(self):
        storage_total = 0
        for mineral in self.mineral_storage.names:  
            storage_total += self.mineral_storage.quantity[mineral]
                        
        return storage_total
        
        
    def draw(self, canvas, y, x):
        if (self.build_timer > 0 or self.status == 'inactive') and self.parent:
            color = canvas.colors[2]
        else:
            color = canvas.colors[1]
        canvas.screen.addstr(y, x, ".---.", color)
        canvas.screen.addstr(y+1, x, "|   |", color)
        canvas.screen.addstr(y+2, x, "`___'", color)
        
        
    def draw_command_details(self, canvas, y, x):
        canvas.screen.addstr(y, x, self.name)
        if self.build_timer > 0:
            canvas.screen.addstr(y+2, x+2, "Constructing : %s days" % self.build_timer, canvas.colors[2])
        else:
            if self.status == 'inactive':
                color = canvas.colors[2]
            else:
                color = canvas.colors[0]
            canvas.screen.addstr(y+2, x+2, "Status    : %s" % self.status, color)
        canvas.screen.addstr(y+3, x+2, "Power Draw:{:>5} MW".format(self.power_consumption))
        
        canvas.screen.addstr(y+17, x+1, "(c)onfigure")
        
        return y+4
        
        
    def configure(self, canvas, y, x):
        canvas.screen.addstr(y, x, "%s - Configuration" % self.name)
        
        canvas.screen.addstr(y+2, x+1, "Toggle (s)tatus: %s" % self.status)
        
        return y+3
        
        
    def handle_configuration_command(self, command):
        if command == ord('s'):
            if self.status == 'active':
                self.status = 'inactive'
            else:
                self.status = 'active'
        
        
    def draw_build_options(self, canvas, y, x, minerals):
        self.draw(canvas, y, x)
        canvas.screen.addstr(y+1, x+6, self.name)
        
        canvas.screen.addstr(y+4, x+2, "Power Draw:{:>5} MW".format(self.power_consumption))
        
        canvas.screen.addstr(y+6, x, "Build Cost: ")
        build_option_color = canvas.colors[0]
        for index, mineral in enumerate(self.build_cost.names):
            if self.build_cost.quantity[mineral] > minerals.quantity[mineral]:
                color = canvas.colors[2]
                build_option_color = canvas.colors[2]
            else:
                color = canvas.colors[0]
            canvas.screen.addstr(y+7+index, x+2, "{:<11}: {:>6}".format(mineral, self.build_cost.quantity[mineral]), color)
            
        canvas.screen.addstr(y+17, x+2, "(b)uild", build_option_color)
        
        
        
        
        
class CommandCentre(Building):
    
    name = 'Command Centre'
    description = """Commands ships"""
    
    command_key = ord('c')
    
    def __init__(self, parent):
        Building.__init__(self, parent)
    
        self.power_consumption = -1.0
        self.algae_output = 2.1
        self.oxygen_output = 1.3
    
        self.mineral_storage_max = 10000
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "C", canvas.colors[1])
        
        
    def draw_command_details(self, canvas, y, x):
        y = Building.draw_command_details(self, canvas, y, x)
        
        canvas.screen.addstr(y-1, x+2, "Power Output: {:>5} MW".format(abs(self.power_consumption)))
        canvas.screen.addstr(y, x+2, "Algae Output: {:>5} Kg/d".format(self.algae_output))
        canvas.screen.addstr(y+1, x+2, "Oxygen Output:{:>5} Kg/d".format(self.oxygen_output))
        
        canvas.screen.addstr(y+11, x, "   Mineral Storage (m^3)")
        
        mineral_total = 0
        for m in self.mineral_storage.names:
            mineral_total += self.mineral_storage.quantity[m]
            
        stor = "{:>13}/{:<13}".format(mineral_total, self.mineral_storage_max)
        canvas.screen.addstr(y+12, x, "{:^27}".format(stor))
        
        
    def configure(self, canvas, y, x):
        canvas.screen.addstr(y, x, "%s - Config." % self.name)
        
    def handle_configuration_command(self, command):
        pass
        
        
class PowerPlant(Building):
    
    name = 'Power Plant'
    description = """Generates power"""
    
    command_key = ord('p')
    
    build_time = 6
    
    def __init__(self, parent):
        Building.__init__(self, parent)
        
        self.build_cost = Minerals(None, 220, 40, 15, 4, 2, 2, 1)
    
        self.power_consumption = -5.0
        self.power_stored = 0.1
        self.power_storage_max = 10000.0
        
        
    def advance_day(self):
        if self.build_timer > 0:
            Building.advance_day(self)
        elif self.status == 'active':
            output, draw, stored = self.parent.calculate_power()
            daily_balance = (output - draw) * 24
            self.power_stored += daily_balance
            if self.power_stored > self.power_storage_max:
                self.power_stored = self.power_storage_max
            elif self.power_stored < 0.0:
                self.power_stored = 0.0
                    
    
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "P", canvas.colors[1])
        
        
    def draw_command_details(self, canvas, y, x):
        y = Building.draw_command_details(self, canvas, y, x)
        
        canvas.screen.addstr(y-1, x+2, "Power Output:{:>5} MW".format(abs(self.power_consumption)))

        canvas.screen.addstr(y+1, x+1, "Totals")
        total_power_output, total_power_draw, stored = self.parent.calculate_power()
        
        canvas.screen.addstr(y+2, x+2, "Power Output:{:>5} MW".format(total_power_output))
        canvas.screen.addstr(y+3, x+2, "Power Draw:  {:>5} MW".format(total_power_draw-(total_power_draw*2)))
        power_balance = total_power_output - total_power_draw
        if power_balance < 0.0:
            canvas.screen.addstr(y+4, x+2, "Balance:     {:>5} MW".format(power_balance), canvas.colors[0])
        else:
            canvas.screen.addstr(y+5, x+2, "Balance:     {:>5} MW".format(power_balance))
            
            
        canvas.screen.addstr(y+11, x, "      Storage (MWh)")
        stor = "{:>13}/{:<13}".format(self.power_stored, self.power_storage_max)
        canvas.screen.addstr(y+12, x, "{:^27}".format(stor))
        
        
        
class Hydroponics(Building):
    
    name = 'Hydroponics'
    description = """Generates food & oxygen"""
    
    command_key = ord('h')
    
    build_time = 5
    
    def __init__(self, parent):
        Building.__init__(self, parent)
        
        self.build_cost = Minerals(None, 310, 110, 5, 2, 0, 0, 0)
    
        self.power_consumption = 0.5
    
        self.algae_output = 10.3
        self.algae_storage_max = 500.0
    
        self.oxygen_output = 5.6 #0.6 per person per day
        self.oxygen_storage_max = 5000.0

    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "H", canvas.colors[1])
        
        
    def draw_command_details(self, canvas, y, x):
        y = Building.draw_command_details(self, canvas, y, x)
        
        canvas.screen.addstr(y, x+2, "Algae Output: {:>5} Kg/d".format(self.algae_output))
        canvas.screen.addstr(y+1, x+2, "Oxygen Output:{:>5} Kg/d".format(self.oxygen_output))
        
        canvas.screen.addstr(y+3, x+1, "Totals")
        total_algae_output, total_algae_consumption = self.parent.calculate_algae()
        total_oxygen_output, total_oxygen_consumption = self.parent.calculate_oxygen()
        
        canvas.screen.addstr(y+4, x+2, "Algae Output: {:>5} Kg/d".format(total_algae_output))
        canvas.screen.addstr(y+5, x+2, "Algae Used:   {:>5} Kg/d".format(total_algae_consumption))
        
        canvas.screen.addstr(y+6, x+2, "Oxygen Output:{:>5} Kg/d".format(total_oxygen_output))
        canvas.screen.addstr(y+7, x+2, "Oxygen Used:  {:>5} Kg/d".format(total_oxygen_consumption))
        
        
class Accomodation(Building):
    
    name = 'Accomodation'
    description = """People live here"""
    
    command_key = ord('a')
    
    build_time = 3
    
    def __init__(self, parent):
        Building.__init__(self, parent)
        
        self.build_cost = Minerals(None, 195, 185, 12, 4, 0, 0, 0)
    
        self.power_consumption = 1.2
        
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "A", canvas.colors[1])
        
        
class Refinery(Building):
    
    name = 'Refinery'
    description = """Extracts minerals from rock"""
    
    command_key = ord('r')
    
    build_time = 5
    
    def __init__(self, parent):
        Building.__init__(self, parent)
        
        self.build_cost = Minerals(None, 380, 80, 30, 12, 2, 0, 1)
    
        self.power_consumption = 3.9
        self.mineral_storage_max = 30000
        self.extraction_capacity = 12
        
        self.extraction_configuration = Minerals()
        
        
    def advance_day(self):
        if self.build_timer > 0:
            Building.advance_day(self)
        elif self.status == 'active':
            if self.calculate_mineral_storage_total() < self.mineral_storage_max:
                for mineral in self.mineral_storage.names:
                    extraction_amount = self.extraction_configuration.quantity[mineral]
                    if self.parent.minerals.quantity[mineral] >= extraction_amount:
                        self.parent.minerals.quantity[mineral] -= extraction_amount
                        self.mineral_storage.quantity[mineral] += extraction_amount
                    else:
                        self.mineral_storage.quantity[mineral] += self.parent.minerals.quantity[mineral]
                        self.parent.minerals.quantity[mineral] = 0
            #else #find another place to store it.
        
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "R", canvas.colors[1])
        
        
    def draw_command_details(self, canvas, y, x):
        y = Building.draw_command_details(self, canvas, y, x)
        
        if self.build_timer > 0:
            canvas.screen.addstr(y+13, x+1, "-----------")
        else:
            canvas.screen.addstr(y, x+2, "Extraction Cap.: %s m^3" % self.extraction_capacity)
        
            canvas.screen.addstr(y+2, x, "Geology:")
        
            for index, mineral in enumerate(self.parent.minerals.names):
                canvas.screen.addstr(y+3+index, x+2, "{:<10}: {:>6}  [{}]".format(mineral, self.parent.minerals.quantity[mineral], self.extraction_configuration.quantity[mineral]))
        
            mineral_total = 0
            for m in self.mineral_storage.names:
                mineral_total += self.mineral_storage.quantity[m]
            
            stor = "{:>13}/{:<13}".format(mineral_total, self.mineral_storage_max)
            canvas.screen.addstr(y+12, x, "{:^27}".format(stor))
        
    
    def configure(self, canvas, y, x):
        y = Building.configure(self, canvas, y, x)
        
        canvas.screen.addstr(y+1, x, "Extraction Config: %s/%s" % (self.calculate_extraction_capacity_used(), self.extraction_capacity))
        for index, mineral in enumerate(self.extraction_configuration.names):
            canvas.screen.addstr(y+2+index, x+2, "({}) {:<10}: {}".format(index+1, mineral, self.extraction_configuration.quantity[mineral]))
            
    
    def calculate_extraction_capacity_used(self):
        extraction_capacity_used = 0
        
        for m in self.extraction_configuration.quantity:
            extraction_capacity_used += self.extraction_configuration.quantity[m]
            
        return extraction_capacity_used
        
        
    def handle_configuration_command(self, command):
        Building.handle_configuration_command(self, command)
        
        extraction_capacity_used = self.calculate_extraction_capacity_used()
            
        if extraction_capacity_used < self.extraction_capacity:
            if command == ord('1'):
                self.extraction_configuration.quantity[self.extraction_configuration.names[0]] += 1
            if command == ord('2'):
                self.extraction_configuration.quantity[self.extraction_configuration.names[1]] += 1
            if command == ord('3'):
                self.extraction_configuration.quantity[self.extraction_configuration.names[2]] += 1
            if command == ord('4'):
                self.extraction_configuration.quantity[self.extraction_configuration.names[3]] += 1
            if command == ord('5'):
                self.extraction_configuration.quantity[self.extraction_configuration.names[4]] += 1
            if command == ord('6'):
                self.extraction_configuration.quantity[self.extraction_configuration.names[5]] += 1
            if command == ord('7'):
                self.extraction_configuration.quantity[self.extraction_configuration.names[6]] += 1
                
        if command == 33 and self.extraction_configuration.quantity[self.extraction_configuration.names[0]] > 0:
            self.extraction_configuration.quantity[self.extraction_configuration.names[0]] -= 1
        elif command == 64 and self.extraction_configuration.quantity[self.extraction_configuration.names[1]] > 0:
            self.extraction_configuration.quantity[self.extraction_configuration.names[1]] -= 1
        elif command == 194 and self.extraction_configuration.quantity[self.extraction_configuration.names[2]] > 0:
            self.extraction_configuration.quantity[self.extraction_configuration.names[2]] -= 1
        elif command == 36 and self.extraction_configuration.quantity[self.extraction_configuration.names[3]] > 0:
            self.extraction_configuration.quantity[self.extraction_configuration.names[3]] -= 1
        elif command == 37 and self.extraction_configuration.quantity[self.extraction_configuration.names[4]] > 0:
            self.extraction_configuration.quantity[self.extraction_configuration.names[4]] -= 1
        elif command == 94 and self.extraction_configuration.quantity[self.extraction_configuration.names[5]] > 0:
            self.extraction_configuration.quantity[self.extraction_configuration.names[5]] -= 1
        elif command == 38 and self.extraction_configuration.quantity[self.extraction_configuration.names[6]] > 0:
            self.extraction_configuration.quantity[self.extraction_configuration.names[6]] -= 1

        
class StorageSilo(Building):
    
    name = 'Storage Silo'
    description = """Stores minerals"""
    
    command_key = ord('s')
    
    build_time = 4
    
    def __init__(self, parent):
        Building.__init__(self, parent)
        
        self.build_cost = Minerals(None, 390, 315, 20, 9, 6, 0, 0)
    
        self.power_consumption = 1.0 #0.3
    
        self.mineral_storage_max = 50000
        
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "S", canvas.colors[1])
        
        
class Factory(Building):
    
    name = 'Factory'
    description = """Builds things"""
    
    command_key = ord('f')
    
    build_time = 7
    
    def __init__(self, parent):
        Building.__init__(self, parent)
        
        self.build_cost = Minerals(None, 480, 350, 40, 12, 22, 0, 1)
    
        self.power_consumption = 4.6
        
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "F", canvas.colors[1])
        
        
class Laboratory(Building):
    
    name = 'Laboratory'
    description = """Researches new technology"""
    
    command_key = ord('l')
    
    build_time = 11
    
    def __init__(self, parent):
        Building.__init__(self, parent)
        
        self.build_cost = Minerals(None, 280, 480, 68, 17, 45, 12, 1)
    
        self.power_consumption = 6.6
        
    
    def draw(self, canvas, y, x):
        Building.draw(self, canvas, y, x)
        canvas.screen.addstr(y+1, x+2, "L", canvas.colors[1])