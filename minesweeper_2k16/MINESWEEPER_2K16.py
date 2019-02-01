"""Command line minesweeper clone for python 3.5. Only for windows and utf-8 encoding"""
import msvcrt
import os
import random
import time
import math
# en ole ihan varma että mitä kurssillä oikeastaan pidettiin oikeana ratkaisuna jos moduulista tarvitaan vain yhtä asiaa.
# esimerkiksi msvcrt moduulista olisi voinut kutsua vain getch funktion esimerkiksi

def clear_screen():
    """Clears the command-line"""
    os.system("cls")

def getch():
    """Waits for keypress and returns the character without the need for enter-key"""
    while True:
        try:
            return msvcrt.getch().decode()
        except UnicodeDecodeError:
            continue

def get_dimensions():
    """Asks the user for board dimensions and returns them"""
    flag = 0
    while True:
        clear_screen()
        print ("o-----------------------------o")
        print ("|                             |")
        print ("| GIVE BOARD WIDTH AND HEIGHT |")
        print ("|  AND PRESS ENTER WHEN DONE  |")
        print ("|   OR JUST LEAVE EMPTY FOR   |")
        print ("|    DEFAULT SIZE (7 by 5)    |")
        print ("|                             |")
        print ("|         E.G.: 10 10         |")
        print ("|                             |")
        if flag == 0:   print ("|                             |\n"
                               "|                             |")
        elif flag == 1: print ("|    VALUEERROR: ENTER TWO    |\n"
                               "|   INTEGERS OR LEAVE EMPTY   |")
        elif flag == 2: print ("|   SIZEERROR: INVALID SIZE   |\n"
                               "|       TOO SMALL BOARD       |")
        else:           print ("|   SIZEERROR: INVALID SIZE   |\n"
                               "| MAXIMUM BOARD SIZE IS 99*99 |")
        print ("|                             |")
        print ("o-----------------------------o")
        userinput = input("WIDTH AND HEIGHT: ")
        if userinput == (""):
            clear_screen()
            return 7, 5
        else:
            try:
                width, height = userinput.split(" ")
                width = int(width)
                height = int(height)
            except ValueError:
                flag = 1
                continue
            else:
                if width <= 0 or height <= 0 :
                    flag = 2
                    continue
                elif width > 99 or height > 99:
                    flag = 3
                    continue
                else:
                    clear_screen()
                    return width, height

def get_mines():
    """Asks the user for mine amount and returns it in int"""
    flag = 0
    while True:
        clear_screen()
        print ("o-----------------------------o")
        print ("|                             |")
        print ("|  ENTER THE NUMBER OF MINES  |")
        print ("|  AND PRESS ENTER WHEN DONE  |")
        print ("|   OR JUST LEAVE EMPTY FOR   |")
        print ("|     DEFAULT AMOUNT (15)     |")
        print ("|                             |")
        print ("|          E.G.: 100          |")
        print ("|                             |")
        if flag == 0:   print ("|                             |\n"
                               "|                             |")
        elif flag == 1: print ("|    VALUEERROR: ENTER ONE    |\n"
                               "| INTEGER OR JUST LEAVE EMPTY |")
        else:           print ("| NOTENOUGHMINESERROR: AMOUNT |\n"
                               "|     MUST BE ONE OR MORE     |")
        print ("|                             |")
        print ("o-----------------------------o")
        userinput = input("AMOUNT OF MINES: ")
        if userinput == (""):
            clear_screen()
            return (15)
        else:
            try:
                mines = int(userinput)
            except ValueError:
                flag = 1
                continue
            else:
                if mines < 1:
                    flag = 2
                    continue
                else:
                    clear_screen()
                    return mines

def make_board(width, height, mines):
    """
    Generates the empty board and returns it in 2D-list or false if mine amount is too high
    Example board:
    [[" "], [" "], [" "],
     [" "], [" "], [" "],
     [" "], [" "], [" "]]
    """
    if width*height <= mines:
        clear_screen()
        print ("o-----------------------------o")
        print ("|                             |")
        print ("|   SIZEERROR: INVALID SIZE   |")
        print ("|                             |")
        print ("|     TOO SMALL BOARD FOR     |")
        print ("|     THE AMOUNT OF MINES     |")
        print ("|    PRESS ENTER TO CHANGE    |")
        print ("|    ( MAX AMOUNT = {} )    |".format("{0:04d}".format(width*height-1)))
        print ("|                             |")
        print ("|                             |")
        print ("|                             |")
        print ("|                             |")
        print ("o-----------------------------o")
        input ()
        return False
    else:
        return [["·" for i in range(width)] for i in range(height)]
    
def plant_mines_and_placeholders(board, mines):
    """Plants the given number of mines (marked as M) randomly onto the board and surrounds them with placeholder symbols for numbers (markes as P)"""
    # this part plants the mines
    i = 0
    while mines != i:
        width = (random.randint(0,len(board[0])-1))
        height = (random.randint(0,len(board)-1))
        if board[height][width] == "·":
            board[height][width] = "M"
            i += 1
        else:
            continue
    # this part surrounds the mines with placeholer symbols
    for x in range(len(board[0])):
        for y in range(len(board)):
            if board[y][x] == "M":
                for i in ((x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)):
                    x_i = i[0]
                    y_i = i[1]
                    if x_i < 0 or y_i < 0 or x_i > len(board[0])-1 or y_i > len(board)-1:
                        continue
                    else:
                        if board[y_i][x_i] == "·":
                           board[y_i][x_i] = "P"

def _print_board(board):
    """Prints the board in it's current state showing numbers but hiding mines and placeholders. Also prints coordinate guides"""
    
    clear_screen()
    
    width = len(board[0])
    height = len(board)
    
    # this part prints coordinate guides at top
    if width <= 10:
        print ("      " + ("0 ")*width)
        print ("      " + "{}".format("".join(["{} ".format(i) for i in range(width)]))) # generates list ["0 ", "1 ", "2 "...] and joins it into string. then formats it into print function
    else:
        help_list = []
        lazy_solution = "00010203040506070809"
        for i in range(10, width):
            help_list.append(str(i))
        help_list = "".join(help_list)
        help_list = list(lazy_solution + help_list) # yields always the same result if width is 10 or less. that case is handlend in the previous part
        row1 = []
        row2 = []
        for i in range(len(help_list)):
            if i % 2 == 0:
                row1.append(help_list[i])
            else:
                row2.append(help_list[i])
        print ("      " + " ".join(row1))
        print ("      " + " ".join(row2))
    
    # this part prints the top arrows
    print ("      " + ("v ")*width)
    
    # this part prints the rows with the board itself. also hides mines "M" and placeholder "P" with the "·" symbol
    for i in range(height):
        print((" ".join(list(("{0:02d}".format(i)))) + " > " + (" ".join(board[i])) + " < " + " ".join(list(("{0:02d}".format(i))))).replace("M", "·").replace("P", "·"))
    
    # this part prints the bottom arrows
    print ("      " + ("^ ")*width)
    
    # this part prints the coordinate guides at bottom
    if width <= 10:
        print ("      " + ("0 ")*width)
        print ("      " + "{}".format("".join(["{} ".format(i) for i in range(width)]))) # generates list ["0 ", "1 ", "2 "...] and joins it into string. then formats it into print function
    else:
        help_list = []
        lazy_solution = "00010203040506070809"
        for i in range(10, width):
            help_list.append(str(i))
        help_list = "".join(help_list)
        help_list = list(lazy_solution + help_list) # yields always the same result if width is 10 or less. that case is handlend in the previous part
        row1 = []
        row2 = []
        for i in range(len(help_list)):
            if i % 2 == 0:
                row1.append(help_list[i])
            else:
                row2.append(help_list[i])
        print ("      " + " ".join(row1))
        print ("      " + " ".join(row2))

def _print_board_cheat(board):
    """Prints the board in it's current state showing numbers, mines and placeholders. Also prints coordinate guides"""
    
    clear_screen()
    
    width = len(board[0])
    height = len(board)
    
    # this part prints coordinate guides at top
    if width <= 10:
        print ("      " + ("0 ")*width)
        print ("      " + "{}".format("".join(["{} ".format(i) for i in range(width)]))) # generates list ["0 ", "1 ", "2 "...] and joins it into string. then formats it into print function
    else:
        help_list = []
        lazy_solution = "00010203040506070809"
        for i in range(10, width):
            help_list.append(str(i))
        help_list = "".join(help_list)
        help_list = list(lazy_solution + help_list) # yields always the same result if width is 10 or less. that case is handlend in the previous part
        row1 = []
        row2 = []
        for i in range(len(help_list)):
            if i % 2 == 0:
                row1.append(help_list[i])
            else:
                row2.append(help_list[i])
        print ("      " + " ".join(row1))
        print ("      " + " ".join(row2))
    
    # this part prints the top arrows
    print ("      " + ("v ")*width)
    
    # this part prints the rows with the board itself. also hides mines "M" and placeholder "P" with the "·" symbol
    for i in range(height):
        print(" ".join(list(("{0:02d}".format(i)))) + " > " + (" ".join(board[i])) + " < " + " ".join(list(("{0:02d}".format(i)))))
    
    # this part prints the bottom arrows
    print ("      " + ("^ ")*width)
    
    # this part prints the coordinate guides at bottom
    if width <= 10:
        print ("      " + ("0 ")*width)
        print ("      " + "{}".format("".join(["{} ".format(i) for i in range(width)]))) # generates list ["0 ", "1 ", "2 "...] and joins it into string. then formats it into print function
    else:
        help_list = []
        lazy_solution = "00010203040506070809"
        for i in range(10, width):
            help_list.append(str(i))
        help_list = "".join(help_list)
        help_list = list(lazy_solution + help_list) # yields always the same result if width is 10 or less. that case is handlend in the previous part
        row1 = []
        row2 = []
        for i in range(len(help_list)):
            if i % 2 == 0:
                row1.append(help_list[i])
            else:
                row2.append(help_list[i])
        print ("      " + " ".join(row1))
        print ("      " + " ".join(row2))

def get_coordinates_print_board(board):
    """Asks the user for coordinates of panel to open and returns them or "QUIT" "QUIT" if user wants to quit. Also prints board"""
    flag = 0
    while True:
        clear_screen()
        _print_board(board)
        print ("o----------------------------------------------------------------------------o")
        print ("| ENTER COORDINATES OF THE PANEL YOU WANT TO OPEN WITH HORIZONTAL AXIS FIRST |")
        print ("|               E.G: 10 8      OR ENTER Q TO EXIT TO MAIN MENU               |")
        print ("|                                                                            |")
        if flag == 0:   print ("|                                                                            |")
        elif flag == 1: print ("|                       VALUEERROR: ENTER TWO INTEGERS                       |")
        else:           print ("|             COORDINATESERROR: COORDINATES MUST BE ON THE BOARD             |")
        print ("|                                                                            |")
        print ("o----------------------------------------------------------------------------o")
        userinput = input("X-COORDINATE AND Y-COORDINATE: ")
        if userinput == "q" or userinput == "Q":
            return "QUIT", "QUIT" # cant use false here. it would equal to zero
        elif userinput == "aasisvengaa":
            clear_screen()
            _print_board_cheat(board)
            print ("o----------------------------------------------------------------------------o")
            print ("|                                                                            |")
            print ("|                     CHEAT VIEW ON. CONTINUE WITH ENTER                     |")
            print ("|                                                                            |")
            print ("|  \"M\" MINE    \"P\" NUMBER PLACEHOLDER    \"·\" CLOSED PANEL    \" \" OPEN PANEL  |")
            print ("|                                                                            |")
            print ("o----------------------------------------------------------------------------o")
            input ()
            continue
        else:
            try:
                x, y = userinput.split(" ")
                x = int(x)
                y = int(y)
            except ValueError:
                flag = 1
                continue
            else:
                if x < 0 or y < 0 or x > len(board[0])-1 or y > len(board)-1:
                    flag = 2
                    continue
                else:
                    return x, y
                    clear_screen()
    
def open_panel(board, x, y):
    """
    Opens one panel and returns value depending on the result
        If panel is in the middle of empty area do floodfill and return   "TURNDONE"
        If panel is number placeholder calculate the number and return    "TURNDONE"
        If panel is mine display "gameover" screen until enter and return "GAMELOST"
        If none of the above panel has already been opened and return     "TURNPASS"
    """
    if board[y][x] == "·": # floodfill with empty space until border or number placeholder P is hit. Calculate the P and place it in
        seed = [(x, y)] # seed for the floodfill
        while seed: # while seed is not empty it is true
            x, y = seed.pop() # remove item from seed and use it to create the 8-directional check-list
            board[y][x] = " " # fill the seed
            for i in ((x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)): # do followring for 8 directions around the seed
                x_i = i[0] # secondary X and Y generated from the list above to use for checking
                y_i = i[1] # secondary X and Y generated from the list above to use for checking
                if x_i < 0 or y_i < 0 or x_i > len(board[0])-1 or y_i > len(board)-1: # check if the current item from the 8-direction-list is in the field
                    continue # skip to next item if it is not
                else: # otherwise
                    if board[y_i][x_i] == "·": # if there is empty panel
                       seed.append((x_i, y_i)) # add it to seed list
                    if board[y_i][x_i] == "P": # ---- HERE STARTS THE PLACEHOLER CALCULATION PART ---- if panel is placeholder
                        x = x_i # take the location of P use it to create the 8-directional check-list
                        y = y_i # take the location of P use it to create the 8-directional check-list
                        mine_counter = 0 # generate mine counter to keep track of the surround mines
                        for i in ((x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)): # do followring for 8 directions around the seed
                            x_i = i[0] # tertiary X and Y generated from the list above to use for checking
                            y_i = i[1] # tertiary X and Y generated from the list above to use for checking
                            if x_i < 0 or y_i < 0 or x_i > len(board[0])-1 or y_i > len(board)-1: # check if the current item from the 8-direction-list is in the field
                                continue # skip to next item if it is not
                            else: # otherwise
                                if board[y_i][x_i] == "M": # if it is a mine
                                    mine_counter += 1 # increase mine counter
                        if mine_counter != 0: # if mine counter is not zero
                            board[y][x] = str(mine_counter) # write the counted amount to the panel
                        mine_counter = 0 # and reset counter for the next iteration
        return "TURNDONE"              
    
    elif board[y][x] == "P": # count mines surrounding the placeholder
        mine_counter = 0 # generate mine counter to keep track of the surround mines
        for i in ((x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)): # do followring for 8 directions around the seed
            x_i = i[0] # tertiary X and Y generated from the list above to use for checking
            y_i = i[1] # tertiary X and Y generated from the list above to use for checking
            if x_i < 0 or y_i < 0 or x_i > len(board[0])-1 or y_i > len(board)-1: # check if the current item from the 8-direction-list is in the field
                continue # skip to next item if it is not
            else: # otherwise
                if board[y_i][x_i] == "M": # if it is a mine
                    mine_counter += 1 # increase mine counter
        if mine_counter != 0: # if mine counter is not zero
            board[y][x] = str(mine_counter) # write the counted amount to the panel
        mine_counter = 0 # and reset counter for the next iteration
        return "TURNDONE"
    
    elif board[y][x] == "M": # game over
        board[y][x] = "X" # mark the mine with X so the user can view the board before the game ends because M are hidden in normal print board and cheat one views placeholders that are not wanted here
        clear_screen()
        _print_board(board)
        print ("o----------------------------------------------------------------------------o")
        print ("|                                                                            |")
        print ("|                             G A M E    O V E R                             |")
        print ("|                                                                            |")
        print ("|                      PRESS ENTER TO EXIT TO MAIN MENU                      |")
        print ("|                                                                            |")
        print ("o----------------------------------------------------------------------------o")
        input()
        return "GAMELOST"
    
    else: # panel has already been opened
        return "TURNPASS"

def game_won(board):
    """If win conditions are met return True otherwise False"""
    checkstring = ""
    for row in board:
        checkstring = checkstring+"".join(row)
    if "·" not in checkstring and "P" not in checkstring:
        clear_screen()
        _print_board_cheat(board)
        print ("o----------------------------------------------------------------------------o")
        print ("|                                                                            |")
        print ("|                               Y O U    W I N                               |")
        print ("|                                                                            |")
        print ("|                      PRESS ENTER TO EXIT TO MAIN MENU                      |")
        print ("|                                                                            |")
        print ("o----------------------------------------------------------------------------o")
        input ()
        return True
    else:
        return False

def save_scores(W_or_L, game_duration, start_time, start_date, width, lenght, mines, turns):
    """
    Saves scores into a MINESWEEPER_2K16_SCORES.txt with one game per row
    
    arguments: True or False, lenght in seconds, start time, start date, width, lenght, mines, turns
    note: start time and start date can use whatever format. string type assumed

    Example save data:
    Lost in 09 minutes and 01 seconds at 20:15:56 16/10/2016 on 09*11 board with 10 mines over 10 turns
    """
    if W_or_L == True:
        result = "Won "
    else:
        result = "Lost"
        
    # this formatting part could be in the write part but that would look too complicated
    minutes, seconds = divmod(game_duration, 60)
    seconds = "{0:02d}".format(int(round(seconds+0.1)))
    minutes = "{0:02d}".format(int(round(minutes+0.1)))
    width = "{0:02d}".format(width)
    lenght = "{0:02d}".format(lenght)
    mines = "{0:04d}".format(mines)
    
    
    try:
        with open("MINESWEEPER_2K16_SCORES.txt", "a") as target:
            target.write("{} in {} minutes and {} seconds at {} {} on {}*{} board with {} mines over {} turns\n".format(result, minutes, seconds, start_time, start_date, width, height, mines, turns))
    except: # no idea what errors to except
        print ("Couldn't write to scoreboard file. Sorry. Enter to continue")
        input ()

def print_scores():
    """Prints scores from savefile"""
    clear_screen()
    print ("o----------------------------------------------------------------------------o")
    print ("|                                                                            |")
    print ("|                        SCORES LISTED BY TIME PLAYED                        |")
    print ("|                                                                            |")
    print ("|                      PRESS ENTER TO EXIT TO MAIN MENU                      |")
    print ("|                                                                            |")
    print ("o----------------------------------------------------------------------------o")
    try:
        with open("MINESWEEPER_2K16_SCORES.txt") as target:
            for row in target.readlines():
                print (row)
    except: # no idea what errors to except
        print ("Couldn't read the scoreboard file. Sorry. Enter to continue")
        input ()

def make_validator():
    """Makes file to use for validating score file"""
    validator = []
    try:
        with open("MINESWEEPER_2K16_SCORES.txt") as target:
            for row in target.readlines():
                validator.append(row)
    except: # no idea what errors to except
        print ("Couldn't create savefile validator. Sorry")
        input ()
    validator = "".join(validator).replace("\n", "").replace(" ", "").replace("0", "")
    hash = str(int(math.sqrt(len(validator)*(math.pi))*98567966583454987545644598456498456))
    hash = hash.replace("3", "a").replace("2", "y").replace("5", "k").replace("6", "e").replace("9", "h")
    try:
        with open("MINESWEEPER_2K16_SCORES.validator", "w") as target:
            target.write(hash)
    except: # no idea what errors to except
        print ("Couldn't create savefile validator. Sorry")
        input ()

def check_validator():
    """Checks the valitor file to see if scoreboard has been edited"""
    validator = []
    try:
        with open("MINESWEEPER_2K16_SCORES.txt") as target:
            for row in target.readlines():
                validator.append(row)
    except: # no idea what errors to except
        print ("Couldn't create savefile validator. Sorry")
        input ()
    validator = "".join(validator).replace("\n", "").replace(" ", "").replace("0", "")
    hash = str(int(math.sqrt(len(validator)*(math.pi))*98567966583454987545644598456498456))
    hash = hash.replace("3", "a").replace("2", "y").replace("5", "k").replace("6", "e").replace("9", "h")
    
    try:
        with open("MINESWEEPER_2K16_SCORES.validator") as target:
            if hash != target.read():
                    with open("MINESWEEPER_2K16_SCORES.txt", "w") as target:
                        target.write("")
                    print ("!!! SCOREBOARD FILE HAS BEEN EDITED. RESETTING !!!")
                    input ()
    except: # no idea what errors to except
        print ("Couldn't create savefile. Sorry")
        input ()

check_validator()
while True:
    clear_screen()
    print ("o-----------------------------o")
    print ("|                             |")
    print ("|    M I N E S W E E P E R    |")
    print ("|           2 K 1 6           |")
    print ("|                             |")
    print ("|          p - PLAY           |")
    print ("|          s - SCORES         |")
    print ("|          q - QUIT           |")
    print ("|                             |")
    print ("|   CONTINUE WITH p, s OR q   |")
    print ("|                             |")
    print ("|                             |")
    print ("o-----------------------------o")
    choise = getch().lower() # Don't try to allow CAPS in choise because numlock+pageup and various others can produce P, S or Q in getch() !!!
    
    if choise == "p":
        width, height = get_dimensions()
        while True:
            mines = get_mines()
            board = make_board(width, height, mines)
            if board == False:
                continue
            else:
                break
        plant_mines_and_placeholders(board, mines)
        
        # get values to write in scores
        start_time = time.strftime("%H:%M:%S")
        start_date = time.strftime("%d/%m/%Y")
        game_length_start = time.time()
        turn_counter = 1
        
        while True: # the actual game-loop
            if game_won(board) == True:
                game_length = time.time() - game_length_start
                save_scores(True, game_length, start_time, start_date, width, height, mines, turn_counter)
                make_validator()
                break
            else:
                x, y = get_coordinates_print_board(board)
                if x == "QUIT" and y == "QUIT": # cant use false here. it would equal to zero
                    break
                else: 
                    turn_result = open_panel(board, x, y)
                    if turn_result == "TURNDONE":
                        turn_counter += 1
                    elif turn_result == "GAMELOST":
                        game_length = time.time() - game_length_start
                        save_scores(False, game_length, start_time, start_date, width, height, mines, turn_counter)
                        make_validator()
                        break
                    elif turn_result == "TURNPASS":
                        pass
                    else:
                        print ("This clause exists for debugging and it shouldn't get printed during gameplay")
    elif choise == "s":
        print_scores()
        input ()
        continue
    
    elif choise == "q":
        clear_screen()
        break
    else:
        continue