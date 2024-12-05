import pygame
from pygame.locals import *
from tensorflow.keras.models import load_model
import numpy as np
from connect_four import ConnectFourEnv
import time

model1 = load_model('connect4_model1.h5')
model2 = load_model('connect4_model2.h5')

env = ConnectFourEnv()

# Set up Pygame window
pygame.init()
FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 80
BOARD_WIDTH = env.observation_space.shape[1]
BOARD_HEIGHT = env.observation_space.shape[0]
BOARD_OFFSET_X = int((WINDOW_WIDTH - BOARD_WIDTH * CELL_SIZE) / 2)
BOARD_OFFSET_Y = int((WINDOW_HEIGHT - BOARD_HEIGHT * CELL_SIZE) / 2)
WINDOW_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Connect Four')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Define font
FONT_SIZE = 32
FONT = pygame.font.Font(None, FONT_SIZE)

# Set up game variables
state = env.reset()
done = False
player_turn = 1
winner = None


def draw_board(board):
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            pygame.draw.rect(WINDOW_SURF, WHITE, (BOARD_OFFSET_X + x * CELL_SIZE, BOARD_OFFSET_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if board[y][x] == 1:
                pygame.draw.circle(WINDOW_SURF, YELLOW, (int(BOARD_OFFSET_X + (x + 0.5) * CELL_SIZE), int(BOARD_OFFSET_Y + (y + 0.5) * CELL_SIZE)), int(CELL_SIZE / 2.5))
            elif board[y][x] == -1:
                pygame.draw.circle(WINDOW_SURF, RED, (int(BOARD_OFFSET_X + (x + 0.5) * CELL_SIZE), int(BOARD_OFFSET_Y + (y + 0.5) * CELL_SIZE)), int(CELL_SIZE / 2.5))


def draw_text(text, x, y, color):
    text_surf = FONT.render(text, True, color)
    text_rect = text_surf.get_rect()
    text_rect.center = (x, y)
    WINDOW_SURF.blit(text_surf, text_rect)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while not done:

        # AI player 1's turn
        q_values = model2.predict(state.reshape(1, -1))[0]
        env.state = state
        valid_actions = env.get_valid_actions()
        masked_q_values = np.ma.array(q_values,
                                      mask=[not env.action_space.contains(i) for i in range(env.action_space.n)])
        action = np.argmax(masked_q_values)
        state, reward, done, info = env.step(action)
        if done:
            winner = env.winner

        WINDOW_SURF.fill(BLACK)
        draw_board(state)
        if winner:
            draw_text("Agent {} wins!".format(winner), int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2),
                      RED if winner == 1 else YELLOW)
        else:
            draw_text("Agent 1 turn", int(WINDOW_WIDTH / 2), int(CELL_SIZE / 2), YELLOW)
        pygame.display.update()
        time.sleep(5)

        # AI player 2's turn
        q_values = model1.predict(state.reshape(1, -1))[0]
        env.state = state
        valid_actions = env.get_valid_actions()
        masked_q_values = np.ma.array(q_values,
                                      mask=[not env.action_space.contains(i) for i in range(env.action_space.n)])
        action = np.argmax(masked_q_values)
        state, reward, done, info = env.step(action)
        if done:
            winner = env.winner

        WINDOW_SURF.fill(BLACK)
        draw_board(state)
        if winner:
            draw_text("Agent {} wins!".format(winner), int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2),
                      RED if winner == 1 else YELLOW)
        else:
            draw_text("Agent 2 turn", int(WINDOW_WIDTH / 2), int(CELL_SIZE / 2), RED)
        pygame.display.update()
        time.sleep(5)

    time.sleep(1)
    pygame.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
