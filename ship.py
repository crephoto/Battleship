import random

class Ship:

    def __init__(self, info):
        self.type = info[0]
        self.size = info[1]
        self.sunk = False
        self.pos = [] # FIXME: Remove magic number/Use len(shipArray) or something
        self.status = [info[0][0]]*int(info[1])
    
    def setPosition(self, x, y):
        self.pos.append((x, y))

    def isSunk(self):
        if self.sunk == False and self.status.count("X") == self.size:
            self.sunk = True
        
        return self.sunk
    
    def shoot(self, target):
        for i, pos in enumerate(self.pos):
            if pos == target:
                self.status[i] = "X"
                return(True)

        return(False)
