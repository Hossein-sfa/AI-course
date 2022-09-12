from random import choice


def has_interfere(x, y, board):
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


def queen_placer(board):
    x_coordinates = [i for i in range(8)]
    y_coordinates = [i for i in range(8)]
    for i in range(8):
        x = choice(x_coordinates)
        y = choice(y_coordinates)
        x_coordinates.remove(x)
        y_coordinates.remove(y)
        board[x][y] = 'Q'


def evaluate_board(board):
    result = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'Q':
                if has_interfere(i, j, board):
                    result += 1
    return result


while True:
    chess_board = [[None for i in range(8)] for j in range(8)]
    queen_placer(chess_board)
    score = evaluate_board(chess_board)
    if score == 0:
        for i in range(8):
            for j in range(8):
                if chess_board[i][j] == 'Q':
                    print(f'{i + 1}, {j + 1}')
        break

