import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
from matplotlib.pyplot import MultipleLocator


class Environment(object):
    def __init__(self, rows=5, cols=8, barrier_num=3, reward_num=5):
        self.rows = rows
        self.cols = cols
        self.barrier_num = barrier_num
        self.reward_num = reward_num
        self.reward = {0: 0, 1: 0, 2: 10, -1: -
                       100, 3: -1}  # reward of each node type
        self.create_env_default()

    def create_env_default(self):
        # the final matrix of environment in our problem
        # start node = 1, terminal node = 2, cliff = -1, barrier = -2, reward = 3
        # [[1. - 1. - 1. - 1. - 1. - 1. - 1.  2.]
        # [0.  0.  0.  0.  0.  0. - 2.  0.]
        # [0.  0.  0.  3. - 2.  0.  0.  0.]
        # [3.  0.  0.  0. - 2.  0.  0.  3.]
        # [0.  0.  3.  0.  0.  0.  0.  0.]]

        self.env = np.zeros([self.rows, self.cols])
        # start node = 1, terminal node = 2, cliff = -1
        self.env[0][0] = 1
        self.env[0][self.cols-1] = 2
        self.env[0][1:self.cols-1] = -1

        # set barrier pos
        barrier_pos = [[3, 4], [2, 4], [1, 6]]
        # set barrier = -2
        for pos in barrier_pos:
            self.env[pos[0]][pos[1]] = -2

        # set reward pos
        reward_pos = [[3, 0], [2, 3], [4, 2], [3, 7]]
        # set reward = 3
        for pos in reward_pos:
            self.env[pos[0]][pos[1]] = 3

    def create_env(self):
        self.env = np.zeros([self.rows, self.cols])
        # start node = 1, terminal node = 2, cliff = -1
        self.env[0][0] = 1
        self.env[0][self.cols-1] = 2
        self.env[0][1:self.cols-1] = -1

        # randomly set barrier pos
        barrier_pos = []
        while(len(barrier_pos) < self.barrier_num):
            i = random.randint(1, self.rows-1)
            j = random.randint(0, self.cols-1)
            if [i, j] not in barrier_pos and [i, j] not in [[1, 0], [1, self.cols-1]]:
                barrier_pos.append([i, j])

        # set barrier = -2
        for pos in barrier_pos:
            self.env[pos[0]][pos[1]] = -2

        # randomly set reward pos
        reward_pos = []
        while (len(reward_pos) < self.reward_num):
            i = random.randint(1, self.rows - 1)
            j = random.randint(0, self.cols - 1)
            if [i, j] not in reward_pos and [i, j] not in barrier_pos:
                reward_pos.append([i, j])

        # set reward = 3
        for pos in reward_pos:
            self.env[pos[0]][pos[1]] = 3

    def show_env(self):
        # fig = plt.figure()
        ax = plt.subplot()
        plt.xlim((0, self.cols))
        plt.ylim((0, self.rows))
        # name: start, terminal, cliff, barrier, reward, others
        # number: 1, 2, -1, -2, 3, 0
        # color: yellow, orange, gray, black, red, white
        color_dict = {-1: "gray", 1: "yellow",
                      2: "orange", -2: "black", 3: "red", 0: "white"}
        my_x_ticks = np.arange(0, self.cols, 1)
        my_y_ticks = np.arange(0, self.rows, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        x_major_locator = MultipleLocator(1)
        y_major_locator = MultipleLocator(1)
        ax.xaxis.set_major_locator(x_major_locator)
        ax.yaxis.set_major_locator(y_major_locator)
        ax.xaxis.set_ticks_position('top')
        ax.invert_yaxis()

        plt.grid()
        for i in range(self.rows):
            for j in range(self.cols):
                color = color_dict[int(self.env[i][j])]
                rect = mpathes.Rectangle([j, i], 1, 1, color=color)
                ax.add_patch(rect)
        # plt.savefig('./cliffwalk.jpg')
        plt.show()


class Sarsa():
    def __init__(self, env):
        self.env = env.env
        self.rows = env.rows
        self.cols = env.cols
        # qval: q-value table, 0: up, 1: right, 2: down, 3: left
        self.qval = np.zeros((self.rows, self.cols, 4))
        # action id -> direction
        self.action = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self.action = [np.array(a) for a in self.action]
        # reward of each state
        self.reward = env.reward
        # utility of start point
        self.util = []

    def policy(self, state, epsilon=0):
        '''choose maximal q-value with epsilon-greedy'''
        rand = random.random()
        # remove all infeasible actions (out of bound or go to barrier)
        # q(s,a)
        qsa = []
        for a_id, reward in enumerate(self.qval[state[0], state[1], :]):
            next_s = state+self.action[a_id]
            if next_s[0] < 0 or next_s[1] < 0 or next_s[0] >= self.rows or next_s[1] >= self.cols or self.env[tuple(next_s)] == -2:
                pass
            else:
                qsa.append((a_id, reward))
        # if all actions are equal
        if len(qsa) == 1:
            return qsa[0][0]
        elif len(qsa) == 2:
            if qsa[0][1] == qsa[1][1]:
                return qsa[int(rand*2)][0]
        elif len(qsa) == 3:
            if qsa[0][1] == qsa[1][1] and qsa[1][1] == qsa[2][1]:
                return qsa[int(rand*3)][0]
        elif len(qsa) == 4:
            if qsa[0][1] == qsa[1][1] and qsa[1][1] == qsa[2][1] and qsa[2][1] == qsa[3][1]:
                return qsa[int(rand*4)][0]

        # choose the max q-value
        maxx = max(qsa, key=lambda x: x[1])
        if rand > epsilon:
            return maxx[0]
        # exploration
        # choose random action with equal probability
        num = len(qsa)
        for k in range(num):
            if rand <= (k+1)*epsilon/num:
                return qsa[k][0]

    # sarsa learning

    def learning(self, max_episode_num, alpha, epsilon, gamma=0.9, show_info=False):
        # gamma: the discount factor
        # max_episode_num: total episode num
        # epsilon: exploration probability
        print("sarsa learning")
        qval = self.qval
        # curent state, current policy, next policy
        state = np.array([0, 0])
        cur_action = self.policy(state, epsilon)
        next_action = 0
        for _ in range(max_episode_num):
            if show_info:
                print("Iteration", _+1)
            # while not terminal
            while self.env[state[0], state[1]] != 2:
                if show_info:
                    print(cur_action, end=" ")
                next_s = state + self.action[cur_action]
                next_action = self.policy(next_s, epsilon)
                # update q value
                qval[state[0], state[1], cur_action] = (1-alpha) * qval[state[0], state[1], cur_action] + alpha * (
                    self.reward[self.env[next_s[0], next_s[1]]] + gamma * qval[next_s[0], next_s[1], next_action])
                # update state and action
                state = next_s
                cur_action = next_action

            # reset state and action
            state = np.array([0, 0])
            cur_action = self.policy(state, epsilon)
            u = self.qval[0, 0, 2]
            self.util.append(u)
            if show_info:
                print("\n", u)

    def utility_plot(self):
        plt.figure()
        plt.plot(range(len(self.util)), self.util)
        plt.xlabel('iteration')
        plt.ylabel('utility of starting state')
        # plt.title('Training Performance')
        plt.show()

    def qvalue_plot(self):
        # fig = plt.figure()
        ax = plt.subplot()
        # ax.axis('equal')
        plt.xlim((0, self.cols))
        plt.ylim((0, self.rows))
        # name: start, terminal, cliff, barrier, reward, others
        # number: 1, 2, -1, -2, 3, 0
        # color: yellow, orange, gray, black, red, white
        color_dict = {-1: "gray", 1: "yellow",
                      2: "orange", -2: "black", 3: "red", 0: "white"}
        my_x_ticks = np.arange(0, self.cols, 1)
        my_y_ticks = np.arange(0, self.rows, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        x_major_locator = MultipleLocator(1)
        y_major_locator = MultipleLocator(1)
        ax.xaxis.set_major_locator(x_major_locator)
        ax.yaxis.set_major_locator(y_major_locator)
        ax.xaxis.set_ticks_position('top')
        ax.invert_yaxis()

        plt.grid()
        for i in range(self.rows):
            for j in range(self.cols):
                color = color_dict[int(self.env[i][j])]
                rect = mpathes.Rectangle([j, i], 1, 1, color=color)
                ax.add_patch(rect)
                # policy arrow
                # for end point, barrier, skip
                if self.env[i, j] == 2 or self.env[i, j] == -2:
                    continue
                # draw lines to divide each block into four parts
                plt.plot([j,j+1],[i,i+1],c='k',lw=0.5)
                plt.plot([j+1,j],[i,i+1],c='k',lw=0.5)
                
                # plot q value
                plt.text(j+0.5,i+0.25,'{:.2f}'.format(self.qval[i,j,0]),fontsize=6,ha='center')
                plt.text(j+0.75,i+0.5,'{:.2f}'.format(self.qval[i,j,1]),fontsize=6,ha='center',va='center')
                plt.text(j+0.5,i+0.8,'{:.2f}'.format(self.qval[i,j,2]),fontsize=6,ha='center',va='center')
                plt.text(j,i+0.5,'{:.2f}'.format(self.qval[i,j,3]),fontsize=6,va='center')
        
        # plt.savefig('./cliffwalk.jpg')
        plt.show()

    def policy_plot(self):
        # fig = plt.figure()
        ax = plt.subplot()
        # ax.axis('equal')
        plt.xlim((0, self.cols))
        plt.ylim((0, self.rows))
        # name: start, terminal, cliff, barrier, reward, others
        # number: 1, 2, -1, -2, 3, 0
        # color: yellow, orange, gray, black, red, white
        color_dict = {-1: "gray", 1: "yellow",
                      2: "orange", -2: "black", 3: "red", 0: "white"}
        my_x_ticks = np.arange(0, self.cols, 1)
        my_y_ticks = np.arange(0, self.rows, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        x_major_locator = MultipleLocator(1)
        y_major_locator = MultipleLocator(1)
        ax.xaxis.set_major_locator(x_major_locator)
        ax.yaxis.set_major_locator(y_major_locator)
        ax.xaxis.set_ticks_position('top')
        ax.invert_yaxis()

        plt.grid()
        for i in range(self.rows):
            for j in range(self.cols):
                color = color_dict[int(self.env[i][j])]
                rect = mpathes.Rectangle([j, i], 1, 1, color=color)
                ax.add_patch(rect)
                # policy arrow
                # for end point, barrier, skip
                if self.env[i, j] == 2 or self.env[i, j] == -2:
                    continue
                arrow = None
                p = self.policy(np.array([i, j]))
                if p == 0:
                    arrow = mpathes.Arrow(j+0.5, i+1, 0, -1)
                    # ax.add_patch(arrow)
                elif p == 2:
                    arrow = mpathes.Arrow(j+0.5, i, 0, 1)
                elif p == 1:
                    arrow = mpathes.Arrow(j, i+0.5, 1, 0)
                elif p == 3:
                    arrow = mpathes.Arrow(j+1, i+0.5, -1, 0)
                ax.add_patch(arrow)
        # plt.savefig('./cliffwalk.jpg')
        plt.show()


if __name__ == "__main__":
    Env = Environment()
    print("the environment matrix:")
    print(Env.env)
    # Env.show_env()

    sarsa = Sarsa(Env)
    random.seed(529)
    # qval = np.zeros((2,2,4))
    # for _ in range(10):
    #     print(sarsa.policy(qval,np.array([0,0]),0.2))
    sarsa.learning(max_episode_num=350, alpha=0.1, epsilon=0.01)
    sarsa.utility_plot()
    sarsa.policy_plot()
    sarsa.qvalue_plot()
