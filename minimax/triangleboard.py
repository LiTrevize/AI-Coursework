import math

INF = 1000


# board size: 4

class TriangleBoard:
    triangles = ((1, 2, 3), (2, 4, 5), (2, 3, 5),
                 (3, 5, 6), (4, 7, 8), (4, 5, 8),
                 (5, 8, 9), (5, 6, 9), (6, 9, 10))

    def __init__(self):
        self.board = TriangleBoard.initAllLines()
        self.turnA = 1

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

    def setLine(self, x, y):
        if x > y:
            x, y = y, x
        if self.turnA == 1:
            self.board[x][y] = 1
            self.turnA = 0
        else:
            self.board[x][y] = 0
            self.turnA = 1

    def getEmptyLines(self):
        lines = []
        for x in self.board.keys():
            for y in self.board[x].keys():
                if self.board[x][y] == -1:
                    lines.append((x, y))
        return lines

    # reward: 100 for A win, -100 for B win, 0 for draw
    def getReward(self):
        a = 0
        b = 0
        for tri in TriangleBoard.triangles:
            x = self.board[tri[0]][tri[1]]
            y = self.board[tri[0]][tri[2]]
            z = self.board[tri[1]][tri[2]]
            if x == y and y == z:
                if x == 1:
                    a += 1
                else:
                    b += 1
        if a > b:
            return 100
        elif a < b:
            return -100
        else:
            return 0

    def next(self, line, turnA):
        next_tb = TriangleBoard()
        next_tb.board = self.board.copy()
        next_tb.board[line[0]][line[1]] = turnA
        return next_tb


def minimax(state, turnA=True, alpha=-INF, beta=INF):
    lines = state.getEmptyLines()
    # all lines are occupied
    if not len(lines):
        return state.getReward()
        # A's turn, maximize
    if turnA:
        for line in lines:
            value = minimax(state.next(line, True), False, alpha, beta)
            # pruning
            if value > alpha:
                alpha = value
            if alpha >= beta:
                break
        return alpha
    # B's turn, minimize
    else:
        for line in lines:
            value = minimax(state.next(line, False), True, alpha, beta)
            # pruning
            if value < beta:
                beta = value
            if alpha >= beta:
                break
    return beta


def main():
    tb = TriangleBoard()
    user_in = input("Enter previous steps (x1 y1 x2 y2 ...):")
    steps = user_in.split()
    for i in range(len(steps) // 2):
        tb.setLine(int(steps[2 * i]), int(steps[2 * i + 1]))
    value = minimax(tb, tb.turnA)
    print(value)
    if value > 0:
        print('A wins')
    elif value < 0:
        print('B wins')
    else:
        print('DRAW')


if __name__ == '__main__':
    main()