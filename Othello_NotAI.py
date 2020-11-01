from bangtal import *
from enum import Enum

setGameOption(GameOption.ROOM_TITLE, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)

scene = Scene("Otello", "./Images/background.png")
board = []

bscore1 = Object("./Images/L0.png")
bscore1.locate(scene, 750, 220)
bscore1.show()
bscore2 = Object("./Images/L2.png")
bscore2.locate(scene, 830, 220)
bscore2.show()

wscore1 = Object("./Images/L0.png")
wscore1.locate(scene, 1070, 220)
wscore1.show()
wscore2 = Object("./Images/L2.png")
wscore2.locate(scene, 1150, 220)
wscore2.show()

class State(Enum):
    BLANK = 0
    POSSIBLE = 1
    BLACK = 2
    WHITE = 3

class Turn(Enum):
    BLACK = 1
    WHITE = 2

turn = Turn.BLACK

def setState(x, y, s):
    ob = board[y][x]
    ob.state = s
    if s == State.BLANK:
        ob.setImage("./Images/blank.png")
    elif s == State.BLACK:
        ob.setImage("./Images/black.png")
    elif s == State.WHITE:
        ob.setImage("./Images/white.png")
    elif turn == Turn.BLACK:
        ob.setImage("./Images/black possible.png")
    else :
        ob.setImage("./Images/white possible.png")

def setPossible_xy_dir(x, y, dx, dy):

    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK

    possible = False
    while True:
        x, y = x + dx, y + dy
        if x < 0 or x > 7 :
            return False
        if y < 0 or y > 7 :
            return False

        ob = board[y][x]
        if ob.state == other:
            possible = True
        elif ob.state == mine:
            return possible
        else:
            return False

def setPossible_xy(x, y):
    ob = board[y][x]
    if ob.state == State.BLACK:
        return False
    if ob.state == State.WHITE:
        return False
    setState(x, y, State.BLANK)

    if setPossible_xy_dir(x, y, 0, 1):
        return True
    if setPossible_xy_dir(x, y, 1, 1):
        return True
    if setPossible_xy_dir(x, y, 1, 0):
        return True
    if setPossible_xy_dir(x, y, 1, -1):
        return True
    if setPossible_xy_dir(x, y, -1, 1):
        return True
    if setPossible_xy_dir(x, y, -1, 0):
        return True
    if setPossible_xy_dir(x, y, -1, -1):
        return True
    if setPossible_xy_dir(x, y, 0, -1):
        return True
    return False

def setPossible():
    pos = False
    for y in range(8):
        for x in range(8):
            if setPossible_xy(x, y):
                setState(x, y, State.POSSIBLE)
                pos = True
    return pos

def reverse_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    else:
        mine = State.WHITE
        other = State.BLACK

    possible = False
    while True:
        x, y = x + dx, y + dy
        if x < 0 or x > 7 :
            return False
        if y < 0 or y > 7 :
            return False

        ob = board[y][x]
        if ob.state == other:
            possible = True
        elif ob.state == mine:
            if possible:
                while True:
                    x, y = x - dx, y - dy
                    ob = board[y][x]
                    if ob.state == other:
                        setState(x, y, mine)
                    else:
                        return
        else:
            return False

def reverse_xy(x, y):
    reverse_xy_dir(x, y, 0, 1)
    reverse_xy_dir(x, y, 1, 1)
    reverse_xy_dir(x, y, 1, 0)
    reverse_xy_dir(x, y, 1, -1)
    reverse_xy_dir(x, y, -1, 1)
    reverse_xy_dir(x, y, -1, 0)
    reverse_xy_dir(x, y, -1, -1)
    reverse_xy_dir(x, y, 0, -1)


def stone_onMouseACtion(x, y):
    global turn

    ob = board[y][x]
    if ob.state == State.POSSIBLE:
        if turn == Turn.BLACK:
            setState(x, y, State.BLACK)
            reverse_xy(x, y)
            turn = Turn.WHITE
        else:
            setState(x, y, State.WHITE)
            reverse_xy(x, y)
            turn = Turn.BLACK

        if not setPossible():
            if turn == Turn.BLACK:
                turn = Turn.WHITE
            else:
                turn = Turn.BLACK
            if not setPossible():
                showMessage("게임이 종료되었습니다")

        setPossible()
        setScore()

def count_black():
    count = 0
    for y in range(8):
        for x in range(8):
            if board[y][x].state == State.BLACK:
                count += 1
    return count

def count_white():
    count = 0
    for y in range(8):
        for x in range(8):
            if board[y][x].state == State.WHITE:
                count += 1
    return count

def setScore():
    bc = str(count_black())
    wc = str(count_white())

    black_path1 = "./Images/L0.png"
    black_path2 = "./Images/L"+bc[0]+".png"
    if count_black() > 9:
        black_path1 = "./Images/L" + bc[0] + ".png"
        black_path2 = "./Images/L" + bc[1] + ".png"

    white_path1 = "./Images/L0.png"
    white_path2 = "./Images/L" + wc[0]+".png"
    if count_white() > 9:
        white_path1 = "./Images/L" + wc[0] + ".png"
        white_path2 = "./Images/L" + wc[1] + ".png"

    bscore1.setImage(black_path1)
    bscore2.setImage(black_path2)
    wscore1.setImage(white_path1)
    wscore2.setImage(white_path2)

for y in range(8):
    board.append([])
    for x in range(8):
        obje = Object("./Images/blank.png")
        obje.locate(scene, 40 + x * 80, 40 + y * 80)
        obje.show()
        obje.onMouseAction = lambda x, y, action, ix = x, iy = y: stone_onMouseACtion(ix, iy)
        obje.state = State.BLANK

        board[y].append(obje)

setState(3, 3, State.BLACK)
setState(4, 4, State.BLACK)
setState(3, 4, State.WHITE)
setState(4, 3, State.WHITE)

setPossible()

startGame(scene)