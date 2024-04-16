from random import choice


class Ai:
    def __init__(self, shape):
        self.shape = shape
        self.X = shape[0]
        self.Y = shape[1]
        # available moves
        self.lines = [((i, j), (i + 1, j)) for i in range(self.X - 1) for j in range(self.Y)] + \
                     [((i, j), (i, j + 1)) for i in range(self.X) for j in range(self.Y - 1)]
        # calculate the best depth for board size
        if self.X * self.Y > 70:
            self.depth = 1
        elif 28 <= self.X * self.Y <= 70:
            self.depth = 2
        else:
            self.depth = 3

    # check if this move leads to a box
    @staticmethod
    def makes_square(current_state, line):
        sum_squares = 0
        if line[0][0] == line[1][0]:
            if ((line[0][0] + 1, line[0][1]), (line[1][0] + 1, line[1][1])) in current_state and \
                    ((line[0][0], line[0][1]), (line[0][0] + 1, line[0][1])) in current_state and \
                    ((line[1][0], line[1][1]), (line[1][0] + 1, line[1][1])) in current_state:
                sum_squares += 1
            if ((line[0][0] - 1, line[0][1]), (line[1][0] - 1, line[1][1])) in current_state and \
                    ((line[0][0] - 1, line[0][1]), (line[0][0], line[0][1])) in current_state and \
                    ((line[1][0] - 1, line[1][1]), (line[1][0], line[1][1])) in current_state:
                sum_squares += 1
        else:
            if ((line[0][0], line[0][1] + 1), (line[1][0], line[1][1] + 1)) in current_state and \
                    ((line[0][0], line[0][1]), (line[0][0], line[0][1] + 1)) in current_state and \
                    ((line[1][0], line[1][1]), (line[1][0], line[1][1] + 1)) in current_state:
                sum_squares += 1
            if ((line[0][0], line[0][1] - 1), (line[0][0], line[0][1])) in current_state and \
                    ((line[0][0], line[0][1] - 1), (line[1][0], line[1][1] - 1)) in current_state and \
                    ((line[1][0], line[1][1] - 1), (line[1][0], line[1][1])) in current_state:
                sum_squares += 1
        return sum_squares

    # deciding best move
    def decide(self, state):
        max_score = -100
        options = []
        if len(self.lines) < 10:
            self.depth += 1
        for line in self.lines:
            if line not in state:
                new_state = state + [line]
                opponent_score = self.minimum(new_state, self.depth - 1)
                square_score = self.makes_square(state, line)
                # if move makes a box it's your turn again
                if square_score > 0:
                    my_turn = self.maximum(new_state, self.depth - 1)
                    if my_turn + square_score > max_score:
                        max_score = my_turn + square_score
                        options = [line]
                    elif my_turn + square_score == max_score:
                        options.append(line)
                elif opponent_score > max_score:
                    max_score = opponent_score
                    options = [line]
                elif opponent_score == max_score:
                    options.append(line)
        return choice(options)

    # min node for opponent
    def minimum(self, current_state, d):
        min_score = 100
        for line in self.lines:
            square_score = self.makes_square(current_state, line)
            if line not in current_state:
                if d != 0:
                    new_state = current_state + [line]
                    opponent_score = self.maximum(new_state, d - 1)
                    if square_score > 0:
                        my_turn = self.minimum(new_state, d - 1)
                        if my_turn - square_score < min_score:
                            min_score = my_turn - square_score
                    elif opponent_score < min_score:
                        min_score = opponent_score
                else:
                    min_score = -square_score if -square_score < min_score else min_score
        return min_score

    # max node for player
    def maximum(self, current_state, d):
        max_score = -100
        for line in self.lines:
            if line not in current_state:
                square_score = self.makes_square(current_state, line)
                if d != 0:
                    new_state = current_state + [line]
                    opponent_score = self.minimum(new_state, d - 1)
                    if square_score > 0:
                        my_turn = self.maximum(new_state, d - 1)
                        if my_turn + square_score > max_score:
                            max_score = my_turn + square_score
                    elif opponent_score > max_score:
                        max_score = opponent_score
                else:
                    max_score = square_score if square_score > max_score else max_score
        return max_score


# test
ai_instance = Ai([3, 3])
print(ai_instance.decide([((0, 0), (0, 1)), ((0, 0), (1, 0))]))
