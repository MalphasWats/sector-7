import random

class Minerals:

    names = ('Tritanium', 'Pyerite', 'Mexallon', 'Isogen', 'Nocxium', 'Zydrine', 'Megacyte')
            
    def __init__(self, density=None):
        random.seed()
        #print "creating minerals at density: %s" % density
        if density == 'medium':
            self.quantity = {
             'Tritanium': random.randint(8000, 54500), 
             'Pyerite': random.randint(6500, 44500), 
             'Mexallon': random.randint(5000, 34500), 
             'Isogen': random.randint(4000, 24500), 
             'Nocxium': random.randint(2000, 14500), 
             'Zydrine': random.randint(500, 8500), 
             'Megacyte': random.randint(280, 5600)
            }
            
        elif density == 'starting_amount':
            self.quantity = {
             'Tritanium': 1500, 
             'Pyerite': 1200, 
             'Mexallon': 750, 
             'Isogen': 45, 
             'Nocxium': 35, 
             'Zydrine': 5, 
             'Megacyte': 2
            }
            
        else:
            self.quantity = {
             'Tritanium': 0, 
             'Pyerite': 0, 
             'Mexallon': 0, 
             'Isogen': 0, 
             'Nocxium': 0, 
             'Zydrine': 0, 
             'Megacyte': 0
            }