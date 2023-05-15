import random, tkinter as tk
from tkinter import font
import board, ship

winMain = tk.Tk()

# Set window width/height
winMain.wm_geometry("1050x570")
winMain.title("Battleship")

name = input("What is your name? ")

# The following two lines allow the frame to fill the window
# We use a single row and column, but this makes them "stretchable"
winMain.columnconfigure(0, weight=1)
winMain.rowconfigure(0, weight=1)
winMain.update()

boardFrame = tk.Frame(winMain, height = winMain.winfo_height(), width = winMain.winfo_width())
boardFrame.columnconfigure(0, weight=10)
boardFrame.columnconfigure(1, weight=10)
boardFrame.columnconfigure(2, weight=1)
boardFrame.rowconfigure(0, weight=2)
boardFrame.rowconfigure(1, weight=5)
boardFrame.rowconfigure(2, weight=50)
boardFrame.pack()
boardFrame.tkraise()
boardFrame.update()

myLabel = tk.Label(boardFrame, text=name, font="Ariel, 14")
myLabel.grid(column=1, row=0)
oppLabel = tk.Label(boardFrame, text="Computer", font="Ariel, 14")
oppLabel.grid(column=2, row=0)

font = font.nametofont("TkDefaultFont")
font.configure(family="Ariel", size=28, weight="bold")

rowsFrame = tk.Frame(boardFrame)
rowsFrame.grid(column=2, row=2, sticky="nesw")
rowsFrame.columnconfigure(0, weight=1)
rowsFrame.columnconfigure(1, weight=1)
rowsFrame.columnconfigure(2, weight=1)
rowsFrame.columnconfigure(3, weight=1)
rowsFrame.columnconfigure(4, weight=1)
rowsFrame.columnconfigure(5, weight=1)
rowsFrame.columnconfigure(6, weight=1)
rowsFrame.columnconfigure(7, weight=1)
rowsFrame.columnconfigure(8, weight=1)
rowsFrame.columnconfigure(9, weight=1)

bdA = tk.Label(rowsFrame, text="A")
bdB = tk.Label(rowsFrame, text="B")
bdC = tk.Label(rowsFrame, text="C")
bdD = tk.Label(rowsFrame, text="D")
bdE = tk.Label(rowsFrame, text="E")
bdF = tk.Label(rowsFrame, text="F")
bdG = tk.Label(rowsFrame, text="G")
bdH = tk.Label(rowsFrame, text="H")
bdI = tk.Label(rowsFrame, text="I")
bdJ = tk.Label(rowsFrame, text="J")

bdA.grid(column=2, row=0)
bdB.grid(column=2, row=1)
bdC.grid(column=2, row=2)
bdD.grid(column=2, row=3)
bdE.grid(column=2, row=4)
bdF.grid(column=2, row=5)
bdG.grid(column=2, row=6)
bdH.grid(column=2, row=7)
bdI.grid(column=2, row=8)
bdJ.grid(column=2, row=9)

columnsFrame = tk.Frame(boardFrame)
columnsFrame.grid(column=1, row=1, sticky="nesw")
columnsFrame.columnconfigure(0, weight=1)
columnsFrame.columnconfigure(1, weight=1)
columnsFrame.columnconfigure(2, weight=1)
columnsFrame.columnconfigure(3, weight=1)
columnsFrame.columnconfigure(4, weight=1)
columnsFrame.columnconfigure(5, weight=1)
columnsFrame.columnconfigure(6, weight=1)
columnsFrame.columnconfigure(7, weight=1)
columnsFrame.columnconfigure(8, weight=1)
columnsFrame.columnconfigure(9, weight=1)

bd1 = tk.Label(columnsFrame, text="1")
bd2 = tk.Label(columnsFrame, text="2")
bd3 = tk.Label(columnsFrame, text="3")
bd4 = tk.Label(columnsFrame, text="4")
bd5 = tk.Label(columnsFrame, text="5")
bd6 = tk.Label(columnsFrame, text="6")
bd7 = tk.Label(columnsFrame, text="7")
bd8 = tk.Label(columnsFrame, text="8")
bd9 = tk.Label(columnsFrame, text="9")
bd10 = tk.Label(columnsFrame, text="10")

bd1.grid(column=0, row=1)
bd2.grid(column=1, row=1)
bd3.grid(column=2, row=1)
bd4.grid(column=3, row=1)
bd5.grid(column=4, row=1)
bd6.grid(column=5, row=1)
bd7.grid(column=6, row=1)
bd8.grid(column=7, row=1)
bd9.grid(column=8, row=1)
bd10.grid(column=9, row=1)

myCanvas = tk.Canvas(boardFrame, height = winMain.winfo_height(), width = winMain.winfo_width()/2)
myCanvas.grid(column=0, row=2, sticky="nws")
myCanvas.update()

oppCanvas = tk.Canvas(boardFrame, height = winMain.winfo_height(), width = winMain.winfo_width()/2)
oppCanvas.grid(column=1, row=2, sticky="nes")
oppCanvas.update()

myBoard = board.Grid(myCanvas)
oppBoard = board.Grid(oppCanvas)

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
bestGuess = ()

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
    if len(target) < 2 or not target[0].isalpha or not target[1:].isnumeric() or int(target[1:]) > 10:
        print("Invalid selection.")
        return(False)

    return(True)

while not gameOver:
    # Rows are A-J, columns are 1-10
    # Take your turn by targeting a square, 
    # eg., 
    # Player's Turn ==================================================
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
        # Computer's Turn ==================================================
        if bestGuess:
            pass
        else:
            # Computer's turn: (Dumb algorithm = random guess)
            col = random.randint(0, 9)
            row = random.randint(0, 9)
            print(f"My turn: {col}{chr(row+65)}... ", end='')

        myBoard.targetCell(col, row)

        if myBoard.gameOver():
            message += " - You lose!"
            gameOver = True
    
        # Uncomment the following line to allow player to see stdout() messages for CLI/Text based version
        #input("Press Enter to continue...")

    myBoard.showBoard(True)
    oppBoard.showBoard(cheat) # TESTING: Set to True for testing (or cheating!)

print(message)

winMain.mainloop()
