import torch
import random
import numpy as np
from collections import deque
from Model import Linear_QNet, QTrainer
from CarRacing import CarRacingGameAI  # Import your car game environment here

# Hyperparameters
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # Exploration rate
        self.gamma = 0.9  # Discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # Memory for experience replay
        self.model = Linear_QNet(10, 256, 3)  # Input, hidden, output sizes
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        car_position = game.car_rect.center
        velocity = game.velocity
        obstacles = game.obstacles

        state = [
            # Car position and velocity
            car_position[0], car_position[1],
            velocity[0], velocity[1],
            
            # Obstacle positions (simplified for example)
            obstacles[0][0], obstacles[0][1],  # First obstacle
            obstacles[1][0], obstacles[1][1],  # Second obstacle

            # Direction towards the goal
            game.roads[0][0] - car_position[0],
            game.roads[0][1] - car_position[1],
        ]
        return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # Random sampling
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games  # Decrease exploration over time
        final_move = [0, 0, 0]  # [straight, left, right]

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
    agent = Agent()
    game = CarRacingGameAI()  # Replace with your car game environment
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

            print('Game', agent.n_games, 'Score', score)

if __name__ == "__main__":
    train()
