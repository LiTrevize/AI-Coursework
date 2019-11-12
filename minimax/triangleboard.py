import copy
import time

INF = 1000


# board size: 4
class TriangleBoard:
    # all possible combinations of small triangles it may form
    triangles = ((1, 2, 3), (2, 4, 5), (2, 3, 5),
                 (3, 5, 6), (4, 7, 8), (4, 5, 8),
                 (5, 8, 9), (5, 6, 9), (6, 9, 10))

    def __init__(self):
        self.board = TriangleBoard.initAllLines()
        self.turnA = 1
        self.score = [0, 0]

    # all lines in a dictionary form
    # i.e. a adjacent list
    # directed: small node to large node
    # -1: unoccupied
    # 1: A's
    # 0: B's
    def initAllLines():
        return {1: {2: -1, 3: -1},
                2: {3: -1, 4: -1, 5: -1},
                3: {5: -1, 6: -1},
                4: {5: -1, 7: -1, 8: -1},
                5: {6: -1, 8: -1, 9: -1},
                6: {9: -1, 10: -1},
                7: {8: -1},
                8: {9: -1},
                9: {10: -1}}

    # when player (specified by self.turnA) take a new move, adding line (x,y)
    def setLine(self, x, y):
        # x should be smaller than y as dictionary specifies
        if x > y:
            x, y = y, x
        # check invalid move
        if x not in self.board.keys() or y not in self.board[x].keys():
            print("Invalid move:", x, "and", y, "cannot be connected")
            return
        # set on the board
        if self.turnA:
            self.board[x][y] = 1
        else:
            self.board[x][y] = 0
        # check if form a triangle and add scores
        oneMoreTurn = False
        for tri in TriangleBoard.triangles:
            if x in tri and y in tri:
                if self.board[tri[0]][tri[1]] != -1 and self.board[tri[0]][tri[2]] != -1 and \
                        self.board[tri[1]][tri[2]] != -1:
                    self.score[self.turnA] += 1
                    oneMoreTurn = True
        # set next turn
        if not oneMoreTurn:
            self.turnA = not self.turnA

    # find all the lines that are empty, i.e. available as the next move
    def getEmptyLines(self):
        lines = []
        for x in self.board.keys():
            for y in self.board[x].keys():
                if self.board[x][y] == -1:
                    lines.append((x, y))
        return lines

    # the next state (whole game state) if player takes step with 'line'
    def next(self, line):
        next_tb = TriangleBoard()
        next_tb.turnA = self.turnA
        # list needs to copy
        next_tb.score = self.score.copy()
        # dict needs to deep copy!
        next_tb.board = copy.deepcopy(self.board)
        # set line
        next_tb.setLine(line[0], line[1])

        return next_tb


def minimax(state, alpha=-INF, beta=INF):
    lines = state.getEmptyLines()
    # all lines are occupied
    # get reward: scoreA - scoreB
    if not len(lines):
        return state.score[1] - state.score[0]
    # early stop:
    # if one player gets more than 5 points
    # he/she must win. This case is preferred.
    # So get reward of 5/-5
    if state.score[1] >= 5:
        return 10
    if state.score[0] >= 5:
        return -10
    # A's turn, maximize
    if state.turnA:
        # line = None
        # value = None
        for line in lines:
            value = minimax(state.next(line), alpha, beta)
            # pruning
            if value > alpha:
                alpha = value
            if alpha >= beta:
                break
        # if 18 - len(lines) + 1 < 9:
        #     print('Move', 18 - len(lines) + 1, ":", line, value, alpha, beta)
        return alpha
    # B's turn, minimize
    else:
        # line = None
        # value = None
        for line in lines:
            value = minimax(state.next(line), alpha, beta)
            # pruning
            if value < beta:
                beta = value
            if alpha >= beta:
                break
        # if 18 - len(lines) + 1 < 9:
        #     print('Move', 18 - len(lines) + 1, ":", line, value, alpha, beta)
        return beta


def main():
    tb = TriangleBoard()
    user_in = input("Enter previous steps (x1 y1 x2 y2 ...):")
    steps = user_in.split()
    for i in range(len(steps) // 2):
        tb.setLine(int(steps[2 * i]), int(steps[2 * i + 1]))

    t0 = time.process_time()
    value = minimax(tb)
    t1 = time.process_time()

    print(value)
    if value > 0:
        print('A wins')
    elif value < 0:
        print('B wins')
    else:
        print('DRAW')
    print("Process Time:", t1 - t0)


if __name__ == '__main__':
    main()
