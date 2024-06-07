import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
import websocket
from environment import *
import threading
import time 
from matplotlib import pyplot as plt
from util import plot


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        # self.model = Linear_QNet(19, 256, 2)

        self.model = Linear_QNet(19, 256, 2)
        self.model.load_state_dict(torch.load('model/model-50.pth'))
        # model.eval()  # Set the model to evaluation mode

        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.is_connected = False
        self.server_address = "ws://192.168.137.8:81/"
        self.ws = websocket.WebSocketApp(self.server_address,on_open=self.on_open,on_message=self.on_message,on_error=self.on_error,on_close=self.on_close)
        threading.Thread(target=self.ws.run_forever).start()

    def on_message(self, ws, message):
        pass

    def on_error(self, ws, error):
        print("Error:", error)

    def on_close(self, ws):
        print("WebSocket connection closed")

    def on_open(self,ws):
        self.is_connected = True
        print("WebSocket connection established")

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def move(self, action, env):
        # return
        # if self.is_connected == False:
            # return
        if action[0] == 1:
            self.ws.send("spd -100 100")
            # env.rotate_car(-10)
        elif action[1] == 1:
            self.ws.send("spd 100 -100")
            # env.rotate_car(10)
        elif action[2] == 1:
            self.ws.send("spd 0 0")
            pass

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 100 - self.n_games
        final_move = [0,0]
        is_random = 0
        if random.randint(0, 100) < self.epsilon:
            move = random.randint(0,1)
            final_move[move] = 1
            # print("Random move", final_move)
            is_random = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            is_random = 0
            # print("Predicted move", final_move)
        return final_move, is_random

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    environment = Environment()
    # while True:
    #     state_old = environment.get_state()
    #     environment.get_reward()
    #     print(state_old)
    moves = 0
    while True:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        # keys = pygame.key.get_pressed()

        # if keys[pygame.K_a]:
        #     environment.rotate_car(10)
        # if keys[pygame.K_d]:
        #     environment.rotate_car(-10)
        # environment.draw()
        # continue
        # environment.get_state()
        state_old = environment.get_state()

        final_move, is_random = agent.get_action(state_old)
        agent.move(final_move, environment)
        moves += 1
        time.sleep(0.1)

        agent.move([0,0,1], environment)

        state_new = environment.get_state()

        reward, done, score = environment.get_reward(state_old, state_new)
        print('move: ',final_move, 'random:', is_random, 'reward: ', reward, 'done: ', done)# 'angle: ', environment.get_angle())


        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done or moves >= 50:
            # time.sleep(1)
            if done:
                move = random.randint(0,1)
                final_move = [0,0]
                final_move[move] = 1
                for i in range(random.randint(20,50)):
                    agent.move(final_move, environment)
            else:
                input("moves exceed! >> ")
            moves = 0
            agent.n_games += 1
            agent.train_long_memory()

            if agent.n_games == 50:
                print('\n\n\nSAVED\n\n\n')
                agent.model.save(file_name='model-50.pth')
                # break
            if agent.n_games == 100:
                print('\n\n\nSAVED\n\n\n')
                agent.model.save(file_name='model-100.pth')
                # break
            
            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            # print("Press enter to continue")
            # input()


if __name__ == '__main__':
    train()