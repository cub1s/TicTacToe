import sys
import random
import time

# current board state
board = [[' ',' ',' '],
        [' ',' ',' '],
        [' ',' ',' ']]

def clear_board():
    global board
    board = [[' ',' ',' '],
            [' ',' ',' '],
            [' ',' ',' ']]

lastWin = None

# vars to distinguish vertical, horizontal, and diagonal win conditions
def verticals():
    vert = [[board[0][0],board[1][0],board[2][0]],
            [board[0][1],board[1][1],board[2][1]],
            [board[0][2],board[1][2],board[2][2]]]
    return vert
def horizontals():
    horiz = [[board[0][0],board[0][1],board[0][2]],
            [board[1][0],board[1][1],board[1][2]],
            [board[2][0],board[2][1],board[2][2]]]
    return horiz
def diagonals():
    diag = [[board[0][0],board[1][1],board[2][2]],
            [board[0][2],board[1][1],board[2][0]]]
    return diag

# draw current game board
def draw_board():
    print('\n')
    for idx, row in enumerate(board):
        print('|'.join(row))
        if idx != 2:
            print('-' * 5)
    print('\n')

# get an array of valid coordinates for the current board state
def open_slots():
    slots = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                slots.append(tuple([i,j]))
    return slots


# get input from user (coordinates in x,y format) and update game board
def user_move():
    global board
    errorMessage = 'Please enter numeric integers 0-2 in the format \"x,y".'
    valid = open_slots()
    s = input('Type valid coorindates for your move: ')
    try:
        coords = tuple(int(x) for x in s.split(","))
        if coords in valid:
            board[coords[0]][coords[1]] = 'x'
            draw_board()
        else:
            print(errorMessage)
            user_move()
    except ValueError:
        print(errorMessage)
        user_move()

# comp *currently* reads for vertical, horizontal, and diagonal (in that order) wins and blocks and will make them if available
# comp will choose a win over a block
# if no win or block open, it chooses a random available slot
def comp_read():
    vert = verticals()
    horiz = horizontals()
    diag = diagonals()
    valid = open_slots()
    choice = (-1,-1)
    win = (-1,-1)
    block = (-1,-1)
    diagMatch = {(1,0):(0,2), (1,1):(1,1), (1,2): (2,0)}
    for i in range(len(vert)):
        countX = 0
        countO = 0
        choice = (-1,-1)
        for j in range(len(vert[i])):
            if vert[i][j] == 'o':
                countO += 1
            elif vert[i][j] == 'x':
                countX += 1
            else:
                choice = (j,i)
        if countO > 1 and choice in valid:
            win = choice
        elif countX > 1 and choice in valid:
            block = choice
    for i in range(len(horiz)):
        countX = 0
        countO = 0
        choice = (-1,-1)
        for j in range(len(horiz[i])):
            if horiz[i][j] == 'o':
                countO += 1
            elif horiz[i][j] == 'x':
                countX += 1
            else:
                choice = (i,j)
        if countO > 1 and choice in valid:
            win = choice
        elif countX > 1 and choice in valid:
            block = choice
    for i in range(len(diag)):
        countX = 0
        countO = 0
        choice = (-1,-1)
        for j in range(len(diag[i])):
            if i == 0:
                if diag[i][j] == 'o':
                    countO += 1
                elif diag[i][j] == 'x':
                    countX += 1
                else:
                    choice = (j,j)
            else:
                if diag[i][j] == 'o':
                    countO += 1
                elif diag[i][j] == 'x':
                    countX += 1
                else:
                    choice = (diagMatch[i,j])
        if countO > 1 and choice in valid:
            win = choice
        elif countX > 1 and choice in valid:
            block = choice
    if win in valid:
        return win
    elif block in valid:
        return block
    else:
        return None

def comp_move():
    global board
    valid = open_slots()
    move = comp_read()
    if move is not None and move in valid:
        coords = move
    else:
        coords = random.choice(valid)
    board[coords[0]][coords[1]] = 'o'
    print('Computer move: ')
    draw_board()

# check for vertical, horizontal, or diagonal wins
def check_win():
    vert = verticals()
    horiz = horizontals()
    diag = diagonals()
    for i in range(len(vert)):
        if vert[i][0] != ' ' and vert[i].count(vert[i][0]) == len(vert[i]):
            return vert[i][0]
    for i in range(len(horiz)):
        if horiz[i][0] != ' ' and horiz[i].count(horiz[i][0]) == len(horiz[i]):
            return horiz[i][0]
    for i in range(len(diag)):
        if diag[i][0] != ' ' and diag[i].count(diag[i][0]) == len(diag[i]):
            return diag[i][0]
    return None

# run the game while there are open slots to play and win has not been found
# prompts to play again
def play_game():
    global lastWin
    # initialize game
    print('Beginning board:')
    clear_board()
    draw_board()
    while open_slots() and not check_win():
        if lastWin == 'o' or lastWin == None:
            if not check_win() and open_slots():
                user_move()
            if not check_win() and open_slots():
                time.sleep(2)
                comp_move()
        else:
            if not check_win() and open_slots():
                time.sleep(2)
                comp_move()
            if not check_win() and open_slots():
                user_move()
    winner = check_win()
    if winner or not open_slots():
        if winner:
            print('{} wins!'.format(winner))
        else:
            print('It\'s a draw!')
        s = ''
        while s != 'y' or s != 'n':
            s = input('Play again? (Y/N): ')
            if s.lower() == 'y':
                lastWin = winner
                play_game()
            elif s.lower() == 'n':
                quit()

play_game()

# program computer to be more aggressive in pursuing win/picking strategic spaces?
# option to pick x or o for user. Must change computer logic to reflexively pick x or o based on user's choice
# convert this to a class - create GUI with pygame in seperate file