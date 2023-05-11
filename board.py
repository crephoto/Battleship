from enum import Enum
import random, tkinter as tk
import ship

# class v2002(Enum):
#     CARRIER = 5
#     BATTLESHIP = 4
#     CRUISER = 3
#     SUBMARINE = 3
#     DESTROYER = 2

v1990 = {"CARRIER": 5, "BATTLESHIP": 4, "CRUISER": 3, "SUBMARINE": 3, "DESTROYER": 2}
v2002 = {"Carrier": 5, "Battleship": 4, "Destroyer": 3, "Submarine": 3, "PT Boat": 2}

# Grid States: "w": water, "s": ship, "h": hit, "m", miss

markers = {"Hit": 'X', "Miss": 'm', "Water": 'w', "Ships": 'BCDPS'}


class Grid:
    height = 10
    width = 10
    hitsRemaining = 0
    forfeit = False
    
    def __init__(self, frame):
        self.board = [[markers['Water']]*self.width for i in range(self.height)]
        self.ships = []
        for item in v2002.items():
            self.ships.append(ship.Ship(item))
            self.hitsRemaining += item[1]

        self.gridScale = 50 # Pixels per grid
        self.frame = frame
        self.frame.pack()
        # Canvas to display game board
        print(f"Canvas width: {frame.winfo_reqwidth()}, height: {frame.winfo_reqheight()}")
        self.grid = tk.Canvas(self.frame, width = frame.winfo_reqwidth(), height = frame.winfo_reqheight(), )
        self.grid.grid(column=0, row=0, )
        # print(f"Instantiated {len(self.ships)} ships")
        
    def showBoard(self, showShips = False):
        if showShips:
            print("\t\t\t", end='')
        print("   1  2  3  4  5  6  7  8  9  10")
        for y in range(self.height):
            if showShips:
                print("\t\t\t", end='')
            print(f"{chr(y+65)} ", end='')
            for x in range(self.width):
                # Don't show water & ships (unless we're cheating or looking at our own board)
                if self.board[x][y] in (markers['Hit'] + markers['Miss']) or self.board[x][y] in markers['Ships'] and showShips:
                    print(f"[{self.board[x][y]}]", end="")
                    if self.board[x][y] == markers['Hit']:
                        self.grid.create_rectangle(x*self.gridScale, y*self.gridScale, (x+1)*self.gridScale, (y+1)*self.gridScale, fill="red", outline = 'gray')
                    elif self.board[x][y] == markers['Miss']:
                        self.grid.create_rectangle(x*self.gridScale, y*self.gridScale, (x+1)*self.gridScale, (y+1)*self.gridScale, fill="white", outline = 'gray')
                    else:
                        self.grid.create_rectangle(x*self.gridScale, y*self.gridScale, (x+1)*self.gridScale, (y+1)*self.gridScale, fill="black", outline = 'gray')
                else: # show hits & misses (and possibly ships)
                    print(f"[ ]", end="")
                    # Maybe just set the canvas background to blue?
                    self.grid.create_rectangle(x*self.gridScale, y*self.gridScale, (x+1)*self.gridScale, (y+1)*self.gridScale, fill="blue", outline = 'gray')
            print("")
        self.grid.update()
        print("---------------------------------")

    def listShips(self):
        for ship in self.ships:
            print(f"Ship type: {ship.type} Size: {ship.size}")

    def placeShips(self):
        for ship in self.ships:
            PositioningShip = True
            while PositioningShip:
                # print(f"Positioning Ship: {ship.type}")
                # Horizontal or Vertical?
                orientation = random.choice('HV')
                # Choose random location within grid
                if orientation == 'H':
                    # Valid rows are 0 through height
                    yPos = random.randint(0, self.height-1)
                    # Valid columns are 0 through width - ship.size + 1
                    xPos = random.randint(0, self.width - ship.size)
                    # Check for "collisions" with other ships
                    collision = False
                    for x in range(xPos, xPos+ship.size):
                        if self.board[x][yPos] != markers['Water']:
                            collision = True
                            break
                    # Place Ship
                    if not collision:
                        for x in range(xPos, xPos+ship.size):
                            self.board[x][yPos] = ship.type[0]
                            ship.pos.append((x, yPos))
                        PositioningShip = False
                elif orientation == 'V':
                    # Valid columns are 0 through width
                    xPos = random.randint(0, self.width-1)
                    # Valid rows are 0 through height - ship.size + 1
                    yPos = random.randint(0, self.height - ship.size)
                    # Check for "collisions" with other ships
                    collision = False
                    for y in range(yPos, yPos + ship.size):
                        if self.board[xPos][y] != markers['Water']:
                            collision = True
                            break
                    # Place Ship
                    if not collision:
                        for y in range(yPos, yPos + ship.size):
                            self.board[xPos][y] = ship.type[0]
                            ship.pos.append((xPos, y))
                        PositioningShip = False
                else:
                    # Logic Error
                    print("Logic error selecting H/V orientation")
                    exit()
                    
    def targetCell(self, col, row):
        status = self.board[col][row]
        if status == markers['Miss'] or status == markers['Hit']:
            print("Duplicate! Try again")
        elif status == markers['Water']:
            self.board[col][row] = markers['Miss']
            print("Miss")
        elif status in markers['Ships']:
            for boat in self.ships:
                if boat.type[0] == self.board[col][row]:
                    if boat.shoot((col, row)):
                        print("Hit!")
                        self.board[col][row] = markers['Hit']
                        if boat.isSunk():
                            print(f"You sunk my {boat.type}!")
                        break
                    else:
                        print("Error: should be a hit but boat reporting miss")
            self.hitsRemaining -= 1
        #print(f"Hits remaining: {self.hitsRemaining}")

    def getHitCount(self):
        return self.hitsRemaining

    def quit(self):
        self.forfeit = True

    def gameOver(self):
        return (self.forfeit or self.hitsRemaining == 0) 

