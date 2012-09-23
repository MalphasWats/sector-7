import random

class Minerals(object):

    names = ('Tritanium', 'Pyerite', 'Hexallon', 'Isogen', 'Nocxium', 'Zydrine', 'Megacyte')
            
    def __init__(self, density=None, Tritanium=0, Pyerite=0, Hexallon=0, Isogen=0, Nocxium=0, Zydrine=0, Megacyte=0):
        if density == 'medium':
            self.quantity = {
             'Tritanium': random.randint(8000, 54500), 
             'Pyerite': random.randint(6500, 44500), 
             'Hexallon': random.randint(5000, 34500), 
             'Isogen': random.randint(4000, 24500), 
             'Nocxium': random.randint(2000, 14500), 
             'Zydrine': random.randint(500, 8500), 
             'Megacyte': random.randint(280, 5600)
            }
            
        elif density == 'starting_amount':
            self.quantity = {
             'Tritanium': 800, 
             'Pyerite': 350, 
             'Hexallon': 110, 
             'Isogen': 20, 
             'Nocxium': 15, 
             'Zydrine': 5, 
             'Megacyte': 2
            }
            
        else:
            self.quantity = {
             'Tritanium': Tritanium, 
             'Pyerite': Pyerite, 
             'Hexallon': Hexallon, 
             'Isogen': Isogen, 
             'Nocxium': Nocxium, 
             'Zydrine': Zydrine, 
             'Megacyte': Megacyte
            }
            
            
    def __lt__(self, other):
        result = True
        for mineral in self.names:
            result = result and (self.quantity[mineral] < other.quantity[mineral])
        return result
    
    def __le__(self, other):
        result = True
        for mineral in self.names:
            result = result and (self.quantity[mineral] <= other.quantity[mineral])
        return result
    
    def __eq__(self, other):
        result = True
        for mineral in self.names:
            result = result and (self.quantity[mineral] == other.quantity[mineral])
        return result
    
    def __ne__(self, other):
        result = False
        for mineral in self.names:
            result = result or (self.quantity[mineral] != other.quantity[mineral])
        return result
    
    def __gt__(self, other):
        result = True
        for mineral in self.names:
            result = result and (self.quantity[mineral] > other.quantity[mineral])
        return result
    
    def __ge__(self, other):
        result = True
        for mineral in self.names:
            result = result and (self.quantity[mineral] >= other.quantity[mineral])
        return result