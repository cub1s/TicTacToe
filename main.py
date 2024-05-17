from settings import *
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("Tic Cat Toe!")
        self.clock = pygame.time.Clock()
        self.running = True
        global board
        board = Board()
        global lastMove
        lastMove = None
        self.board_surf = pygame.Surface((250,250))
        self.board_surf.fill('#3698e3')
        self.board_rect = self.board_surf.get_rect(center = (150,150))
        self.overlay_surf = pygame.Surface((300,300))
        self.overlay_rect = self.overlay_surf.get_rect(center = (150,150))
        self.overlay_surf = self.overlay_surf.convert_alpha()
        self.overlay_surf.fill((0,0,0,0))
        self.slots = pygame.sprite.Group()
        slot_coords = [(25,25),(113,25),(201,25),(25,113),(113,113),(201,113),(25,201),(113,201),(201,201)]
        valid_coords = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
        for idx, coords in enumerate(slot_coords):
            self.slots.add(Slot(coords[0],coords[1],valid_coords[idx]))
        self.slot_list = self.slots.sprites()

    
    def comp_read(self):
        vert = board.verticals()
        horiz = board.horizontals()
        diag = board.diagonals()
        valid = board.open_slots()
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
        
    def comp_move(self):
        valid = board.open_slots()
        move = self.comp_read()
        if move is not None and move in valid:
            coords = move
        else:
            coords = random.choice(valid)
        board.current[coords[0]][coords[1]] = 'o'
        for sprite in self.slot_list:
            if sprite.board_slot == coords:
                selected_slot = sprite
        tiki = pygame.image.load('graphics/tiki.png').convert_alpha()
        selected_slot.image.blit(tiki,(0,0))
        self.lastMove = 'o'
        print('Computer move: ')
        board.draw_board()

    def check_win(self):
        vert = [[(0,0),(1,0),(2,0)],
                [(0,1),(1,1),(2,1)],
                [(0,2),(1,2),(2,2)]]
        horiz = [[(0,0),(0,1),(0,2)],
                [(1,0),(1,1),(1,2)],
                [(2,0),(2,1),(2,2)]]
        diag = [[(0,0),(1,1),(2,2)],
                [(0,2),(1,1),(2,0)]]
        for row in vert:
            # grab first slot value
            compare = board.current[row[0][0]][row[0][1]]
            # grab first slot coordinates
            first = row[0]
            # initialize stack
            stack = ''
            for slot in row:
                stack += board.current[slot[0]][slot[1]]
                # check win (if stack == compare * 3)
                if compare != ' ' and stack == compare * 3:
                    # grab ending slot values for tuple of tuples return
                    final = (slot[0],slot[1])
                    return (first,final)
        for row in horiz:
            compare = board.current[row[0][0]][row[0][1]]
            first = row[0]
            stack = ''
            for slot in row:
                stack += board.current[slot[0]][slot[1]]
                if compare != ' ' and stack == compare * 3:
                    final = (slot[0],slot[1])
                    return (first,final)
        for row in diag:
            compare = board.current[row[0][0]][row[0][1]]
            first = row[0]
            stack = ''
            for slot in row:
                stack += board.current[slot[0]][slot[1]]
                if compare != ' ' and stack == compare * 3:
                    final = (slot[0],slot[1])
                    return (first,final)
        return None

    def run(self):
        # initialize game
        print('Beginning board:')
        board.clear_board()
        board.draw_board()
        global lastMove
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.screen.blit(self.board_surf,self.board_rect)
            self.slots.draw(self.screen)
            self.screen.blit(self.overlay_surf,self.overlay_rect)

            if board.open_slots() and not self.check_win():
                if board.lastWin == 'o' or board.lastWin == None:
                    if not self.check_win() and board.open_slots():
                        if lastMove == 'o' or lastMove == None:
                            self.slots.update()
                        else:
                            self.comp_move()
                            lastMove = 'o'
            winner = self.check_win()
            first_slot = None
            last_slot = None
            if winner or not board.open_slots():
                if winner:
                    for sprite in self.slot_list:
                        if sprite.board_slot == winner[0]:
                            first_slot = sprite
                        if sprite.board_slot == winner[1]:
                            last_slot = sprite
                    pygame.draw.line(self.overlay_surf,'#fcad03',first_slot.rect.center,last_slot.rect.center,width=10)
            
            # pygame.draw.line(self.board_surf,'Blue',self.board_rect.topleft,self.board_rect.bottomright,width=10)
            pygame.display.update()
            self.clock.tick(60)

class Board():
    def __init__(self):
        self.current = [[' ',' ',' '],
                        [' ',' ',' '],
                        [' ',' ',' ']]
        self.lastWin = None

    def clear_board(self):
        self.current = [[' ',' ',' '],
                        [' ',' ',' '],
                        [' ',' ',' ']]
    
    # vars to distinguish vertical, horizontal, and diagonal win conditions
    def verticals(self):
        vert = [[self.current[0][0],self.current[1][0],self.current[2][0]],
                [self.current[0][1],self.current[1][1],self.current[2][1]],
                [self.current[0][2],self.current[1][2],self.current[2][2]]]
        return vert
    def horizontals(self):
        horiz = [[self.current[0][0],self.current[0][1],self.current[0][2]],
                [self.current[1][0],self.current[1][1],self.current[1][2]],
                [self.current[2][0],self.current[2][1],self.current[2][2]]]
        return horiz
    def diagonals(self):
        diag = [[self.current[0][0],self.current[1][1],self.current[2][2]],
                [self.current[0][2],self.current[1][1],self.current[2][0]]]
        return diag
    # draw current game board
    def draw_board(self):
        print('\n')
        for idx, row in enumerate(self.current):
            print('|'.join(row))
            if idx != 2:
                print('-' * 5)
        print('\n')
    # get an array of valid coordinates for the current board state
    def open_slots(self):
        slots = []
        for i in range(len(self.current)):
            for j in range(len(self.current[i])):
                if self.current[i][j] == ' ':
                    slots.append(tuple([i,j]))
        return slots

class Slot(pygame.sprite.Sprite):
    def __init__(self,x,y,board_slot):
        super().__init__()
        self.board_slot = board_slot
        self.image = pygame.Surface((74,74))
        self.image.fill('Black')
        self.rect = self.image.get_rect(topleft = (x,y))
        self.pressed = False
        self.benny = pygame.image.load('graphics/benny.png').convert_alpha()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        valid = board.open_slots()
        global lastMove
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed and self.board_slot in valid:
                    print('open slot!')
                    self.image.blit(self.benny,(0,0))
                    self.image = pygame.transform.scale(self.image,(74,74))
                    board.current[self.board_slot[0]][self.board_slot[1]] = 'x'
                    self.pressed = False
                    lastMove = 'x'
                    board.draw_board()
        else:
            self.pressed = False

    def update(self):    
        self.check_click()
        
if __name__ == '__main__':
    game = Game()
    game.run()