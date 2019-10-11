import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
from queue import PriorityQueue as PQ


class MazeProblem:
    def __init__(self, maze_file=''):
        # read file and turn into numpy array
        self.map = np.array(self.loadMap(maze_file))

    def loadMap(self, file):
        # Load map txt as matrix.
        # 0: path, 1: obstacle, 2: start point, 3: end point
        f = open(file)
        lines = f.readlines()
        numOfLines = len(lines)
        returnMap = np.zeros((numOfLines, 40))
        A_row = 0
        for line in lines:
            list = line.strip().split(' ')
            returnMap[A_row:] = list[0:40]
            A_row += 1
        print(np.shape(returnMap))
        return returnMap

    def drawMap(self, searchmap=None, show=False):
        # Visualize the maze map.
        # Draw obstacles(1) as red rectangles. Draw path(0) as white rectangles. Draw starting point(2) and ending point(3) as circles.
        rowNum = len(self.map)
        print(rowNum)
        colNum = len(self.map[0])
        print(colNum)
        ax = plt.subplot()
        param = 1
        for col in range(colNum):
            for row in range(rowNum):
                if self.map[row, col] == 2:
                    circle = mpathes.Circle(
                        [param * col + param/2.0, param * row + param/2.0], param/2.0, color='g')
                    ax.add_patch(circle)
                elif self.map[row, col] == 3:
                    circle = mpathes.Circle(
                        [param * col + param/2.0, param * row + param/2.0], param/2.0, color='y')
                    ax.add_patch(circle)
                elif self.map[row, col] == 1:
                    rect = mpathes.Rectangle(
                        [param * col, param * row], param, param, color='r')
                    ax.add_patch(rect)
                else:
                    rect = mpathes.Rectangle(
                        [param * col, param * row], param, param, color='w')
                    ax.add_patch(rect)
                # draw path and searched nodes
                # if searchmap == None:
                #     continue
                if searchmap[row, col] == 1:
                    rect = mpathes.Rectangle(
                        [param * col, param * row], param, param, color='darkgrey')
                    ax.add_patch(rect)
                elif searchmap[row, col] == 2:
                    rect = mpathes.Rectangle(
                        [param * col, param * row], param, param, color='darkblue')
                    ax.add_patch(rect)

        # Improve visualization
        plt.xlim((0, colNum))
        plt.ylim((0, rowNum))
        my_x_ticks = np.arange(0, colNum+1, 1)
        my_y_ticks = np.arange(0, rowNum+1, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        # change the tick size
        ax.tick_params(labelsize=7)
        axx = plt.gca()
        axx.xaxis.set_ticks_position('top')
        axx.invert_yaxis()
        plt.grid()
        # Save maze image.
        plt.savefig('./maze.png')
        # Show the figure in a new window
        if show:
            plt.show()

    def Astar(self):
        # set the limit of coordinates
        xlim = self.map.shape[0]
        ylim = self.map.shape[1]
        # default cost for every node
        cmax = 10000
        # find start point and end point
        index = np.where(self.map == 2)
        start = np.array([index[0][0], index[1][0]])
        index = np.where(self.map == 3)
        end = np.array([index[0][0], index[1][0]])
        # store the true cost (step) of nodes
        cost = np.zeros_like(self.map)
        for i in range(xlim):
            for j in range(ylim):
                cost[i, j] = cmax
        # matrix to store the direction of movement to the previous node in a path
        # +1/-1: down/up +2/-2: right/left
        prev = np.zeros_like(self.map)
        # set of all actions (moving direction)
        directions = [np.array(i) for i in [[1, 0], [0, 1], [-1, 0], [0, -1]]]

        def heuristic(p):
            '''use Manhattan distance to end point as heuristic'''
            return abs(p[0]-end[0])+abs(p[1]-end[1])
        pq = PQ()
        index = 0
        pq.put((0, index, start))
        cost[0, 0] = 0
        while not pq.empty():
            _, _, curp = pq.get()
            # check if end
            if np.array_equal(curp, end):
                break
            for dirr in directions:
                nextp = curp + dirr
                # check if out of index
                if nextp[0] < 0 or nextp[0] >= xlim or nextp[1] < 0 or nextp[1] >= ylim:
                    continue
                # check if wall
                if self.map[tuple(nextp)] == 1:
                    continue
                # check if searched
                if cost[tuple(nextp)] != cmax:
                    continue
                # calculate priority
                # print(nextp)
                priority = cost[tuple(curp)] + heuristic(nextp)
                # set real cost and previous direction
                cost[tuple(nextp)] = cost[tuple(curp)] + 1
                prev[tuple(nextp)] = np.dot(np.array([1, 2]), curp-nextp)
                # put into priority queue
                index = index + 1
                pq.put((priority, index, nextp))
        # search map
        # use 1 to denote searched nodes
        # use 2 to denote the nodes in the path found
        searchmap = np.zeros_like(cost)
        # mark searched nodes
        for i in range(xlim):
            for j in range(ylim):
                if cost[i, j] < 10000:
                    searchmap[i, j] = 1
        # inverse search the path found
        curp = end.copy()
        while True:
            pre = prev[tuple(curp)]
            if pre == 0:
                break
            elif pre == 1:
                curp[0] += 1
            elif pre == -1:
                curp[0] -= 1
            elif pre == 2:
                curp[1] += 1
            elif pre == -2:
                curp[1] -= 1
            searchmap[tuple(curp)] = 2
        # reset start and end
        searchmap[0, 0] = 0
        searchmap[xlim-1, ylim-1] = 0
        return searchmap


if __name__ == "__main__":
    Solution = MazeProblem(maze_file='maze.txt')
    searchmap = Solution.Astar()
    Solution.drawMap(searchmap, show=True)
    # a = np.array([[1,2],[3,4]])
    # print(a[(0,1)])
