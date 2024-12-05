import gym
from gym import spaces
import numpy as np


class ConnectFourEnv(gym.Env):
    def __init__(self):
        self.board_size = 4
        self.board = np.zeros((self.board_size, self.board_size))
        self.action_space = spaces.Discrete(self.board_size)
        self.observation_space = spaces.Box(low=-1, high=1, shape=(self.board_size, self.board_size), dtype=np.float32)
        self.current_player = 1
        self.winner = None
        self.done = False

    def step(self, action):
        if self.done:
            return self.get_obs(), 0, True, {}

        row = self._get_next_row(action)
        if row is None:
            return self.get_obs(), -10, False, {'player': self.current_player}

        self.board[row, action] = self.current_player
        winner = self._check_for_winner()
        if winner is not None:
            reward = 10 if winner == 1 else -10
            self.done = True
            self.winner = winner
        else:
            reward = 0
            self.current_player = 1 if self.current_player == -1 else -1

        return self.get_obs(), reward, self.done, {'player': self.current_player}

    def reset(self):
        self.board = np.zeros((self.board_size, self.board_size))
        self.current_player = 1
        self.winner = None
        self.done = False
        return self.get_obs()

    def render(self, mode='human'):
        print(self.board)

    def get_obs(self):
        return self.board * self.current_player

    def _get_next_row(self, action):
        for row in range(self.board_size):
            if self.board[row, action] == 0:
                return row
        return None

    def _check_for_winner(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                player = self.board[row, col]
                if player == 0:
                    continue
                if col + 3 < self.board_size and np.all(self.board[row, col:col + 4] == player):
                    return player
                if row + 3 < self.board_size and np.all(self.board[row:row + 4, col] == player):
                    return player
                if col + 3 < self.board_size and row + 3 < self.board_size and np.all(
                        np.diagonal(self.board[row:row + 4, col:col + 4]) == player):
                    return player
                if col + 3 < self.board_size and row - 3 >= 0 and np.all(
                        np.diagonal(np.fliplr(self.board[row - 3:row + 1, col:col + 4])) == player):
                    return player
        if np.count_nonzero(self.board) == self.board_size ** 2:
            return 0
        return None

    def get_valid_actions(self):
        # returns a list of valid actions for the current game state
        valid_actions = []
        for j in range(4):
            if self.board[0][j] == 0:
                valid_actions.append(j)
        return valid_actions