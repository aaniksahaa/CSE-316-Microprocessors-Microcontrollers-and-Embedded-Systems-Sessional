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
from helper import plot


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(7, 256, 2)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.is_connected = False
        self.server_address = "ws://192.168.137.53:81/"
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

    def move(self, action):
        # return
        if self.is_connected == False:
            return
        if action[0] == 1:
            self.ws.send("spd -100 100")
        elif action[1] == 1:
            self.ws.send("spd 100 -100")
        elif action[2] == 1:
            self.ws.send("spd 0 0")

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 200 - self.n_games
        final_move = [0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0,1)
            final_move[move] = 1
            print("Random move", final_move)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            print("Predicted move", final_move)
        return final_move

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

    while True:
        state_old = environment.get_state()

        final_move = agent.get_action(state_old)
        agent.move(final_move)
        # time.sleep(0.1)
        
        reward, done, score = environment.get_reward()
        
        state_new = environment.get_state()

        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            for i in range(random.randint(20,50)):
                move = random.randint(0,1)
                final_move = [0,0]
                final_move[move] = 1
                agent.move(final_move)
            
            agent.move([0,0,1])
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

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