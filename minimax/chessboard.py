import time

# max depth = 4 * N
global maxDepth
# board size
global N
# value for infinity
INF = 100
# memorization
cache = {}


# find all the valid child state of the input state
def childStates(r1, c1, r2, c2, turn1):
    validMove = []
    if turn1:
        if 1 <= r1 + 1 <= N and 1 <= c1 <= N:
            validMove.append((r1 + 1, c1, r2, c2))
        if 1 <= r1 - 1 <= N and 1 <= c1 <= N:
            validMove.append((r1 - 1, c1, r2, c2))
        if 1 <= r1 <= N and 1 <= c1 + 1 <= N:
            validMove.append((r1, c1 + 1, r2, c2))
        if 1 <= r1 <= N and 1 <= c1 - 1 <= N:
            validMove.append((r1, c1 - 1, r2, c2))
    else:
        if 1 <= r2 + 2 <= N and 1 <= c2 <= N:
            validMove.append((r1, c1, r2 + 2, c2))
        if 1 <= r2 - 2 <= N and 1 <= c2 <= N:
            validMove.append((r1, c1, r2 - 2, c2))
        if 1 <= r2 <= N and 1 <= c2 + 2 <= N:
            validMove.append((r1, c1, r2, c2 + 2))
        if 1 <= r2 <= N and 1 <= c2 - 2 <= N:
            validMove.append((r1, c1, r2, c2 - 2))
        if 1 <= r2 + 1 <= N and 1 <= c2 <= N:
            validMove.append((r1, c1, r2 + 1, c2))
        if 1 <= r2 - 1 <= N and 1 <= c2 <= N:
            validMove.append((r1, c1, r2 - 1, c2))
        if 1 <= r2 <= N and 1 <= c2 + 1 <= N:
            validMove.append((r1, c1, r2, c2 + 1))
        if 1 <= r2 <= N and 1 <= c2 - 1 <= N:
            validMove.append((r1, c1, r2, c2 - 1))
    return validMove


# reward: 100 for A win, -100 for B win, 0 for draw
def minimax(r1, c1, r2, c2, turn1=True, curDepth=1):
    # if cached, retrieve directly
    if (r1, c1, r2, c2, turn1, curDepth) in cache:
        return cache[(r1, c1, r2, c2, turn1, curDepth)]

    # game over test
    if r1 == r2 and abs(c1 - c2) == 1 or c1 == c2 and abs(r1 - r2) == 1:
        if turn1:
            cache[(r1, c1, r2, c2, turn1, curDepth)] = 100 + curDepth
            return 100 + curDepth
        else:
            cache[(r1, c1, r2, c2, turn1, curDepth)] = -100 + curDepth
            return -100 + curDepth
    if r1 == r2 and abs(c1 - c2) == 2 or c1 == c2 and abs(r1 - r2) == 2:
        if not turn1:
            cache[(r1, c1, r2, c2, turn1, curDepth)] = -100 + curDepth
            return -100 + curDepth

    # maxDepth reached
    if curDepth == maxDepth:
        cache[(r1, c1, r2, c2, turn1, curDepth)] = curDepth
        return curDepth

    # A's turn, maximize
    if turn1:
        bestValue = -INF
        for move in childStates(r1, c1, r2, c2, True):
            value = minimax(move[0], move[1], move[2],
                            move[3], False, curDepth + 1)
            if value > bestValue:
                bestValue = value
        # store to cache
        cache[(r1, c1, r2, c2, turn1, curDepth)] = bestValue
        # print(alpha, curDepth)
        return bestValue
    # B's turn, minimize
    else:
        bestValue = INF
        for move in childStates(r1, c1, r2, c2, False):
            value = minimax(move[0], move[1], move[2],
                            move[3], True, curDepth + 1)
            if value < bestValue:
                bestValue = value
        # store to cache
        cache[(r1, c1, r2, c2, turn1, curDepth)] = bestValue
        # print(beta, curDepth)
        return bestValue


if __name__ == "__main__":
    user_in = input("Enter n r1 c1 r2 c2: ")
    N, r, c, rr, cc = (int(i) for i in user_in.split())
    maxDepth = 4 * N

    # do minimax and record processing time
    t0 = time.process_time()
    res = minimax(r, c, rr, cc)
    t1 = time.process_time()

    # show results
    print('Utility:', res)
    if res < 0:
        print('BLACK', res + 100)
    elif res > 0:
        print('WHITE', 100 - res)
    print('Process Time:', t1 - t0)

