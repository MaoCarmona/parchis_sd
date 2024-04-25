import select
import socket
import threading
import pygame
import random
import os

Width = 650
Height = 650
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
RED = [255, 0, 0]
WHITE = [255, 255, 255]
YELLOW = [253, 232, 15]
COLORS = [GREEN, BLUE, YELLOW, RED, [150, 150, 250]]
COUNTERS = [1]
CENTERS = [[105, 105], [105, Height - 105], [Width - 105, 105],
           [Width - 105, Height - 105], [Width / 2, Height / 2]]


class Block(pygame.sprite.Sprite):
    def __init__(self, dimension, cont=0):
        super().__init__()
        self.image = pygame.Surface(dimension)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.obj_id = cont


class Piece(pygame.sprite.Sprite):
    def __init__(self, number=[0, 1], sky=[0, 0, 0]):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.color = [number[0][0] / 6 * 4, number[0]
                      [1] / 6 * 4, number[0][2] / 6 * 4]
        self.id = number
        self.rect = self.image.get_rect()
        self.number = number
        self.safe = True
        self.position = 0
        self.sky = sky


class PieceButton(pygame.sprite.Sprite):
    def __init__(self, piece_number):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill([220, 220, 220])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.pressed = False
        self.piece = piece_number
        self.text = 0
        self.in_jail = True
        self.in_sky = False
        self.selected = False
        self.value_to_move = 0

    def reset_selection(self):
        if self.selected:
            self.image.fill([220, 220, 220])
            self.selected = False

    def is_selected(self):
        if not self.selected:
            self.selected = True
            self.image.fill([30, 200, 30])
        else:
            self.selected = False
            self.image.fill([220, 220, 220])


class Dice(pygame.sprite.Sprite):
    def __init__(self, dice_number):
        super().__init__()
        self.image = pygame.Surface([150, 150])
        self.image.fill([220, 220, 220])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.value = 0
        self.in_jail = False
        self.turn_throw = 1
        self.dice_number = dice_number
        self.selected = False

    def update_value(self, val):
        self.value = val

    def is_selected(self):
        if not self.selected:
            self.selected = True
            self.image.fill([30, 200, 30])
        else:
            self.selected = False
            self.image.fill([220, 220, 220])


class LaunchButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([150, 50])
        self.image.fill([63, 122, 77])
        self.rect = self.image.get_rect()
        self.rect.x = 770
        self.rect.y = 200
        self.pressed = False
        self.text = "Launch"

    def press_button(self):
        if self.pressed:
            pass


class MoveButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([150, 50])
        self.image.fill([63, 122, 77])
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 350
        self.pressed = False
        self.text = "Move"

    def press_button(self):
        if self.pressed:
            pass


def throw_dice(start_game, remaining_pieces):
    throws = 1
    if start_game:
        throws = 3
    for _ in range(throws):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
    else:
        for _ in range(throws):
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
        if remaining_pieces == 1:
            dice2 = 0
    return dice1, dice2


def create_pieces():
    aux = [[1, 69, 75], [18, 76, 82], [52, 90, 96], [35, 83, 89]]
    complete = []
    for j in range(4):
        pieces_list = []
        for i in range(4):
            piece = Piece([COLORS[j], i + 1], aux[j])
            piece.rect.center = [j * 50 + 50, i * 50 + 50]
            pieces_list.append(piece)
        complete.append(pieces_list)
    print(len(pieces_list))
    return complete


def tower(orientation):  # Tower base creation
    if orientation == 0:
        block = Block([77, 25])
        block.image.fill(GREEN)
        block.rect.x = Width / 2 - 77 / 2
        block.rect.y = 0
    elif orientation == 2:
        block = Block([25, 77])
        block.image.fill(BLUE)
        block.rect.x = 0
        block.rect.y = Height / 2 - 77 / 2
    elif orientation == 4:
        block = Block([77, 25])
        block.image.fill(RED)
        block.rect.x = Width / 2 - 77 / 2
        block.rect.y = Height - 24
    elif orientation == 6:
        block = Block([25, 77])
        block.image.fill(YELLOW)
        block.rect.x = Width - 25
        block.rect.y = Height / 2 - 77 / 2
    return block


def create_squares():
    squares_list = []
    bases_list = []
    blanks_list = []

    for i in range(5):  # Create bases
        block = Block([210, 210], 200 * (i + 1))
        block.image.fill(COLORS[i])
        block.rect.center = CENTERS[i]
        if i == 4:
            block.image = pygame.image.load("statics\cielo.png")
        squares_list.append(block)
        bases_list.append(block)

    for j in range(8):  # Create squares
        if j in [0, 2, 4, 6]:
            aux = tower(j)
            blanks_list.append(aux)
            squares_list.append(aux)
        if j in [0, 3, 4, 7]:
            size = [77, 25]
        else:
            size = [25, 77]
        for i in range(8):
            k = 0
            block = Block(size)

            if j == 0:  # **top left
                k = 0
                block.rect.x = 210
                block.rect.y = i * 27

            elif j == 1:  # **left top
                k = 0
                block.rect.y = 210
                block.rect.x = 189 - i * 27

            elif j == 2:  # ?left bottom
                k = 1
                block.rect.y = Width - 287
                block.rect.x = i * 27

            elif j == 3:  # ?bottom left
                k = 1
                block.rect.x = 210
                block.rect.y = 436 + (i * 27)

            elif j == 4:  # !bottom right
                k = 3
                block.rect.x = Width - 287
                block.rect.y = Height - (i * 27 + 25)

            elif j == 5:  # !right bottom
                k = 3
                block.rect.y = Height - 287
                block.rect.x = 436 + (i * 27)

            elif j == 6:  # TODO: right top
                k = 2
                block.rect.y = 210
                block.rect.x = Height - (i * 27 + 25)

            else:  # TODO: top right
                k = 2
                block.rect.x = Width - 287
                block.rect.y = 189 - i * 27

            if j in [0, 2, 4, 6]:
                if i == 4:
                    block.image.fill(COLORS[k])
                else:
                    block.image.fill(WHITE)
            else:
                if i == 3:
                    block.image.fill(COLORS[k])
                else:
                    block.image.fill(WHITE)

            squares_list.append(block)
            blanks_list.append(block)

    for block in blanks_list:
        block.obj_id = COUNTERS[0]
        COUNTERS[0] += 1

    return squares_list, bases_list, blanks_list


def create_dice():
    result = []
    for i in range(2):
        die = Dice(i + 1)
        if i == 0:
            die.rect.x = 680
            die.rect.y = 20
        else:
            die.rect.x = 870
            die.rect.y = 20
        result.append(die)
    return result


def create_buttons():
    buttons_list = []
    for i in range(4):
        button = PieceButton(i + 1)
        if i == 0:
            button.piece = 1
            button.rect.x = 680
            button.rect.y = 400
        elif i == 1:
            button.piece = 2
            button.rect.x = 780
            button.rect.y = 400
        elif i == 2:
            button.piece = 3
            button.rect.x = 680
            button.rect.y = 500
        elif i == 3:
            button.piece = 4
            button.rect.x = 780
            button.rect.y = 500
        buttons_list.append(button)
    return buttons_list


def create_move_button():
    return []


def construct_move_play(play):
    message = + ":"
    for n in play:
        message += str(n) + " "
    return message[:-1]


def throw():
    global screen
    moves_left = 2
    global use
    while True:
        screen.fill([255, 255, 255])
        if not use:
            use = True
            play = [0, 0, 0, 0]
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                # Game events
                if event.type == pygame.QUIT:
                    end = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Click")
                    click_d = 1
                    click_m = True
                    for b in ALL_BUTTOMS:
                        if b.rect.collidepoint(pos):
                            if click_d == 1:
                                dice_toss = throw_dice(False, 3)
                                moves_left = 2
                                for f in BUTTOMS_PIECES:
                                    f.value_to_move = 0
                                    f.selected = False

                                print(dice_toss)
                                possible_throws = [
                                    sum(dice_toss), dice_toss[0], dice_toss[1]]
                                if dice_toss[0] == dice_toss[1]:
                                    pressed = True
                                else:
                                    pressed = False
                                for die in DICE:
                                    die.selected = False
                                    screen.blit(DICE_FONT.render(str(die.value), False, [220, 220, 220]),
                                                die.rect.center)
                                pygame.display.flip()

                            for die in DICE:
                                screen.blit(DICE_FONT.render(str(die.value), False, [220, 220, 220]),
                                            die.rect.center)
                                die.image.fill([220, 220, 220])
                                if die.dice_number == 1:
                                    die.value = dice_toss[0]
                                    die.update_value(dice_toss[0])
                                else:
                                    die.value = dice_toss[1]
                                    die.update_value(dice_toss[1])
                    for die in DICE:
                        if die.rect.collidepoint(pos):
                            die.is_selected()
                            if die.dice_number == 1:
                                if die.selected:
                                    DICE_LIST[0] = die.value
                                    DICE_LIST[2] = True
                                else:
                                    DICE_LIST[0] = 0
                                    DICE_LIST[2] = False

                            else:
                                if die.selected:
                                    DICE_LIST[1] = die.value
                                    DICE_LIST[3] = True
                                else:
                                    DICE_LIST[1] = 0
                                    DICE_LIST[3] = False

                    for b in BUTTOMS_PIECES:
                        if b.rect.collidepoint(pos):
                            b.is_selected()
                            if b.selected and moves_left > 0:
                                if DICE_LIST[2]:
                                    if b.piece == 1:
                                        b.value_to_move += DICE_LIST[0]
                                        moves_left -= 1
                                        b.selected = False
                                        b.image.fill([220, 220, 220])
                                        for die in DICE:
                                            die.image.fill([220, 220, 220])
                                        pygame.display.flip()
                                    if b.piece == 2:
                                        b.value_to_move += DICE_LIST[0]
                                        moves_left -= 1
                                        b.selected = False
                                        b.image.fill([220, 220, 220])
                                        for die in DICE:
                                            die.image.fill([220, 220, 220])
                                        pygame.display.flip()
                                    if b.piece == 3:
                                        b.value_to_move += DICE_LIST[0]
                                        moves_left -= 1
                                        b.selected = False
                                        b.image.fill([220, 220, 220])
                                        for die in DICE:
                                            die.image.fill([220, 220, 220])
                                        pygame.display.flip()

                                    if b.piece == 4:
                                        b.value_to_move = DICE_LIST[0]
                                        moves_left -= 1
                                        b.selected = False
                                        b.image.fill([220, 220, 220])
                                        for die in DICE:
                                            die.image.fill([220, 220, 220])
                                        pygame.display.flip()
                                    DICE_LIST[2] = False

                                elif DICE_LIST[3]:
                                    if b.piece == 1:
                                        b.value_to_move += DICE_LIST[1]
                                        moves_left -= 1
                                        b.selected = False
                                        b.image.fill


# Server connection socketpp
SERVER_CONNECTION = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_CONNECTION.connect(('localhost', 3005))

# Clear screen
os.system('cls' if os.name == 'nt' else 'clear')
NUMBER = "0"
GAME = False
USE = False
DICE_LIST = [0, 0, False, False]
# Screen dimensions
WIDTH = 650
HEIGTH = 650

if __name__ == '__main__':
    # Initialize pygame
    pygame.init()


    # Set up pygame display and fonts
    SCREEN = pygame.display.set_mode([WIDTH + 400, HEIGTH])
    FONT = pygame.font.Font(None, 20)
    DICE_FONT = pygame.font.Font(None, 50)

    # Sprite groups
    ALL_SPRITES = pygame.sprite.Group()
    BUTTOMS_SPRITES = pygame.sprite.Group()
    BUTTOMS_PIECES = pygame.sprite.Group()
    BUTTOMS_MOVES = pygame.sprite.Group()
    DICES = pygame.sprite.Group()
    GROUP = pygame.sprite.Group()

    # Create game elements
    squares_list, bases_list, blanks_list = create_squares()
    GROUP.add(squares_list)
    fichos = create_pieces()

    # Draw screen components
    pygame.draw.rect(SCREEN, [255, 255, 255], [[650, 0], [850, 650]])
    pygame.draw.line(SCREEN, [0, 0, 0], [650, 0], [650, 650], 2)

    DICE = create_dice()
    DICES.add(DICE)
    ALL_SPRITES.add(DICE)

    ALL_BUTTOMS = create_buttons()
    BUTTOMS_PIECES.add(ALL_BUTTOMS)
    ALL_SPRITES.add(ALL_BUTTOMS)

    BUTTOMS_PIECES.add(ALL_BUTTOMS)
    ALL_SPRITES.add(ALL_BUTTOMS)

    LAUNCH_BUTTOM = LaunchButton()
    BUTTOMS_SPRITES.add(LAUNCH_BUTTOM)
    ALL_SPRITES.add(LAUNCH_BUTTOM)

    MOVE_BUTTOM = MoveButton()
    BUTTOMS_MOVES.add(MOVE_BUTTOM)
    ALL_SPRITES.add(MOVE_BUTTOM)

    PAIRS = False
    END = False
    while not GAME:
        sockets = [SERVER_CONNECTION]
        try:
            read_sockets, write_sockets, error_sockets = select.select(sockets, [], [])
        except select.error as e:
            print("Error de select:", e)
            break
        
        for socks in read_sockets:
            if socks == SERVER_CONNECTION:
                mensaje = socks.recv(1024)
                os.system('cls' if os.name == 'nt' else 'clear')
                if mensaje.count(b"#") > 0:
                    print("My number is #: " + mensaje[-1])
                    NUMBER = mensaje[-1]
                    GAME = True
                    break
                print(mensaje)

    if GAME:
        threading.Thread(target=throw).start()
        while not END:
            SCREEN.fill([255, 255, 255])
            sockets = [SERVER_CONNECTION]
            try:
                read_sockets, write_sockets, error_sockets = select.select(sockets, [], [])
            except select.error as e:
                print("Error de select:", e)
                break
            
            for socks in read_sockets:
                if socks == SERVER_CONNECTION:
                    mensaje = socks.recv(1024)
                    print(mensaje)
                    mensaje = mensaje.split("#")
                    aux = mensaje[3]
                    mensaje[3] = mensaje[2]
                    mensaje[2] = aux
                    SCREEN.blit(DICE_FONT.render(str(mensaje[-1]), False, [0, 0, 0]), [700, 600])
                    for n in range(4):
                        mensaje[n] = mensaje[n].split(" ")
                    print(mensaje)
                    print(len(fichos))
                    for n in fichos:
                        print(len(n), "elemento")

                    for i in range(4):
                        for j in range(4):
                            fichos[i][j].pos = int(mensaje[i][j])

                    for i in range(4):
                        for j in range(4):
                            print(fichos[i][j].pos)
                    print("Updated")
                    if mensaje[0] == 'G':
                        GAME = False
                        END = True
                    break
    SERVER_CONNECTION.close()
