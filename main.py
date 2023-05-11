import random, tkinter as tk
import board, ship

winMain = tk.Tk()

# Set window width/height
winMain.wm_geometry("500x500")

# The following two lines allow the frame to fill the window
# We use a single row and column, but this makes them "stretchable"
winMain.columnconfigure(0, weight=1)
winMain.rowconfigure(0, weight=1)

myFrame = tk.Frame(winMain)
oppFrame = tk.Frame(winMain)

for i in range(10):
    myFrame.columnconfigure(i, weight=1)
    myFrame.rowconfigure(i, weight=1)
    oppFrame.columnconfigure(i, weight=1)
    oppFrame.rowconfigure(i, weight=1)


myFrame.grid(row=0, column=0, sticky="news")
#oppFrame.grid(row=0, column=0, sticky="news")

myBoard = board.Grid(myFrame)
oppBoard = board.Grid(oppFrame)

#urBoard.listShips()
print("Welcome to Battleship!")
print("Randomly placing ships for you on your board.")

myBoard.placeShips()
myBoard.showBoard(True)

print("Randomly placing my ships (Don't peek!)")
oppBoard.placeShips()
#oppBoard.showBoard(False) # TESTING: Set to True for testing (or cheating!)

message = "Game Over"
cheat = False
gameOver = False
bestGuess = ()

def showMyBoard():
    myFrame.tkraise()
    return

def showOppBoard():
    #oppFrame.tkraise()
    return

def parseUserInput(target):
    global cheat
    if target.upper() == "IDDQD":
        cheat = not cheat
        myBoard.showBoard(True)
        oppBoard.showBoard(cheat) # TESTING: Set to True for testing (or cheating!)
        print("Toggling cheeat mode!")
        return(False)

    if target.upper() == 'Q': # Quit
        userChoice = input("Do you really want to quit the game (Y/N)? ")
        if userChoice.upper() == 'Y':
            myBoard.quit()
            return(True)
        else:
            return(False)
    
    # Other "Cheat" codes:
    # - Sink all their ships & end game?
    # - Singk all our ships & forfeit?        
    if not target[0].isalpha or not target[1:].isnumeric() or int(target[1:]) > 10:
        print("Invalid selection.")
        return(False)

    return(True)

while not gameOver:
    # Columns are A-J, rows are 1-10
    # Take your turn by targeting a square, 
    # eg., 
    showMyBoard()
    validInput = False
    while not validInput:
        target = input("Target a grid squre (eg., 'E5'): ")
        validInput = parseUserInput(target)

    if myBoard.gameOver(): # Did user quit?
        message += " - You forfeit!"
        try:
            # User may have already clicked "X"
            winMain.destroy()
        except:
            print("Notice: Application has already been destroyed")
        break

    row = ord(target[0].upper()) - 65
    col = int(target[1:])-1

    # Target/Shoot
    oppBoard.targetCell(col, row)

    # FIXME: Logically this is awkward and should probably 
    if oppBoard.gameOver():
        message += " - You win!"
        gameOver = True

    # Their turn
    else:
        showOppBoard()
        if bestGuess:
            # Computer's turn: (Dumb algorithm = random guess)
            col = random.randint(0, 9)
            row = random.randint(0, 9)
            print(f"My turn: {col}{chr(row+65)}... ", end='')
        myBoard.targetCell(col, row)

        if myBoard.gameOver():
            message += " - You lose!"
            gameOver = True
    
    myBoard.showBoard(True)
    oppBoard.showBoard(cheat) # TESTING: Set to True for testing (or cheating!)

print(message)

winMain.mainloop()
