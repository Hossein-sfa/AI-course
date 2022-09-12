from time import time
from random import randint


def has_interfere(x, y, board):
    for i in range(8):
        if board[x][i] == 'Q' or board[i][y] == 'Q':
            return True
    x_copy = x + 1
    y_copy = y + 1
    while x_copy < 8 and y_copy < 8:
        if board[x_copy][y_copy] == 'Q':
            return True
        x_copy += 1
        y_copy += 1

    x_copy = x - 1
    y_copy = y - 1
    while x_copy >= 0 and y_copy >= 0:
        if board[x_copy][y_copy] == 'Q':
            return True
        x_copy -= 1
        y_copy -= 1

    x_copy = x + 1
    y_copy = y - 1
    while x_copy < 8 and y_copy >= 0:
        if board[x_copy][y_copy] == 'Q':
            return True
        x_copy += 1
        y_copy -= 1

    x_copy = x - 1
    y_copy = y + 1
    while x_copy >= 0 and y_copy < 8:
        if board[x_copy][y_copy] == 'Q':
            return True
        x_copy -= 1
        y_copy += 1

    return False


def queen_placer(board, queens):
    start = time()
    while queens != 8:
        x = randint(0, 7)
        y = randint(0, 7)
        if board[x][y] != 'Q' and not has_interfere(x, y, board):
            board[x][y] = 'Q'
            queens += 1
        if time() - start > 0.3:
            return queens
    return queens


while True:
    queens_num = 0
    chess_board = [[None for i in range(8)] for j in range(8)]
    queens_num = queen_placer(chess_board, queens_num)
    if queens_num == 8:
        for i in range(8):
            for j in range(8):
                if chess_board[i][j] == 'Q':
                    print(f'{i + 1}, {j + 1}')
        break
