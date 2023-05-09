import random
import board, ship

myBoard = board.Grid()
oppBoard = board.Grid()

#urBoard.listShips()
print("Welcome to Battleship!")
print("Randomly placing ships for you on your board.")
myBoard.placeShips()
myBoard.showBoard(True)

print("Randomly placing my ships (Don't peek!)")
oppBoard.placeShips()
oppBoard.showBoard(False) # TESTING: Set to True for testing (or cheating!)

message = "Game Over"
cheat = False
gameOver = False
while not gameOver:
    # Columns are A-J, rows are 1-10
    # Take your turn by targeting a square, 
    # eg., 
    validInput = False
    while not validInput:
        target = input("Target a grid squre (eg., 'E5'): ")
        if target.upper() == "IDDQD":
            cheat = not cheat
            myBoard.showBoard(True)
            oppBoard.showBoard(cheat) # TESTING: Set to True for testing (or cheating!)
            print("Toggling cheeat mode!")
            continue

        if not target[0].isalpha or not target[1:].isnumeric() or int(target[1:]) > 10:
            print("Invalid selection.")
        else:
            validInput = True

    col = ord(target[0].upper()) - 65
    row = int(target[1:])-1

    # Target/Shoot
    oppBoard.targetCell(col, row)

    if oppBoard.gameOver():
        message += " - You win!"
        gameOver = True

    else:
        # Computer's turn: (Dumb algorithm = random guess)
        col = random.randint(0, 9)
        row = random.randint(0, 9)
        print(f"My turn: {chr(col+65)}{row}... ", end='')
        myBoard.targetCell(col, row)

        if myBoard.gameOver():
            message += " - You lose!"
            gameOver = True
    
    myBoard.showBoard(True)
    oppBoard.showBoard(cheat) # TESTING: Set to True for testing (or cheating!)

print(message)