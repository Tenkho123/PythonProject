import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
from CarRacing import CarRacing
import pygame

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(16, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        state = game.get_state()
        return np.array(state, dtype=float)
            # 16 values 
            # [car_x,car_y,
            # self.car_speed,
            # *raycast_distances,
            # finish_x - car_x,
            # finish_y - car_y]
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        states = torch.tensor(states, dtype=torch.float)
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float)
        next_states = torch.tensor(next_states, dtype=torch.float)
        dones = torch.tensor(dones, dtype=torch.bool)
        
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float).unsqueeze(0)
        action = torch.tensor(action, dtype=torch.long).unsqueeze(0)
        reward = torch.tensor(reward, dtype=torch.float).unsqueeze(0)
        next_state = torch.tensor(next_state, dtype=torch.float).unsqueeze(0)
        done = torch.tensor(done, dtype=torch.bool).unsqueeze(0)
        
        self.trainer.train_step(state, action, reward, next_state, done)
        
    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move
    
def train():
    pygame.init()
    pygame.display.set_caption("Car Racing")
    game = CarRacing()
    agent = Agent()
    while True:
        state_old = agent.get_state(game)
        
        final_move = agent.get_action(state_old)
        
        reward, done, score = game.play_step(final_move)
        
        state_new = agent.get_state(game)
        
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        
        agent.remember(state_old, final_move, reward, state_new, done)
        
        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            if agent.n_games % 10 == 0:
                agent.model.save()  

if __name__ == '__main__':
    train()