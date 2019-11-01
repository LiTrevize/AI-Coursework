import math

global maxDepth
global N
INF = 100
moves = []


def childStates(r1, c1, r2, c2, turn1):
    validMove = []
    if turn1:
        if 1 <= r1+1 <= N and 1 <= c1 <= N:
            validMove.append((r1+1, c1, r2, c2))
        if 1 <= r1-1 <= N and 1 <= c1 <= N:
            validMove.append((r1-1, c1, r2, c2))
        if 1 <= r1 <= N and 1 <= c1+1 <= N:
            validMove.append((r1, c1+1, r2, c2))
        if 1 <= r1 <= N and 1 <= c1-1 <= N:
            validMove.append((r1, c1-1, r2, c2))
    else:
        if 1 <= r2+1 <= N and 1 <= c2 <= N:
            validMove.append((r1, c1, r2+1, c2))
        if 1 <= r2-1 <= N and 1 <= c2 <= N:
            validMove.append((r1, c1, r2-1, c2))
        if 1 <= r2 <= N and 1 <= c2+1 <= N:
            validMove.append((r1, c1, r2, c2+1))
        if 1 <= r2 <= N and 1 <= c2-1 <= N:
            validMove.append((r1, c1, r2, c2-1))
        if 1 <= r2+2 <= N and 1 <= c2 <= N:
            validMove.append((r1, c1, r2+2, c2))
        if 1 <= r2-2 <= N and 1 <= c2 <= N:
            validMove.append((r1, c1, r2-2, c2))
        if 1 <= r2 <= N and 1 <= c2+2 <= N:
            validMove.append((r1, c1, r2, c2+2))
        if 1 <= r2 <= N and 1 <= c2-2 <= N:
            validMove.append((r1, c1, r2, c2-2))
    return validMove


# reward: 100 for A win, -100 for B win, 0 for draw


def minimax(r1, c1, r2, c2, turn1=True, curDepth=1, alpha=-INF, beta=INF):
    # game over
    if r1 == r2 and c1 == c2:
        if turn1:
            return -100+curDepth
        else:
            return 100-curDepth
    # maxDepth reached
    if curDepth == maxDepth:
        if turn1:
            return -curDepth
        else:
            return curDepth
    # A's turn, maximize
    if turn1:
        for move in childStates(r1, c1, r2, c2, True):
            value = minimax(move[0], move[1], move[2],
                            move[3], False, curDepth+1, alpha, beta)
            # pruning
            if value > alpha:
                alpha = value
            if alpha >= beta:
                break
        return alpha
    # B's turn, minimize
    else:
        for move in childStates(r1, c1, r2, c2, False):
            value = minimax(move[0], move[1], move[2],
                            move[3], True, curDepth+1, alpha, beta)
            # pruning
            if value < beta:
                beta = value
            if alpha >= beta:
                break
        return beta


if __name__ == "__main__":
    user_in = input("Enter n r1 c1 r2 c2: ")
    N, r1, c1, r2, c2 = (int(i) for i in user_in.split())
    maxDepth = 4*N

    res = minimax(r1, c1, r2, c2)
    rounds = len(moves)

    if res < 0:
        print('BLACK', res+100-1)
    elif res > 0:
        print('WHITE', 100-res-1)
