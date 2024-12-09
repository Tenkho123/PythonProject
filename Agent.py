import torch
import random
import numpy as np
from collections import deque
from CarRacing import CarRacingEnv
from Model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(15, 256, 4)  # assuming the state has 5 features and 4 possible actions
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        # Assuming `game` gives us the car's position, speed, and distances to obstacles
        car_x, car_y = game.car_rect.center  # get the car's x, y position
        car_speed = game.car_speed  # get the car's speed
        #distance_to_obstacle = game.get_distance_to_obstacle()  # assuming a distance measure
        
        distances = game.ray_casting()  # Call the ray_casting method to get the distances to obstacles
        # car_position = np.array([game.car_rect.centerx / 1000, game.car_rect.centery / 800])  # Normalize car position
        # distance_to_obstacle = np.concatenate([car_position, distances])  # Combine the normalized car position with the obstacle distances
        # print("A ", len(game.ray_casting()))
        # state representation could be a vector with car position, speed, and obstacle distances
        state = [
            car_x,
            car_y,
            car_speed,
            *distances,
            game.is_on_road()  # whether the car is on the road (1) or off the road (0)
        ]
        
        return np.array(state, dtype=int)
        '''
        distances = game.ray_casting()  # Ray distances
        car_position = np.array([game.car_rect.centerx / 1000, game.car_rect.centery / 800])  # Normalized car position
        
        # Concatenate the car's position with the ray distances (a 13-element array)
        state = np.concatenate([car_position, distances])
        
        
        # Return the state as a numpy array with float data type (to prevent truncation)
        #return np.array(state, dtype=float)
        '''

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        
        final_move = [0, 0, 0, 0]  # 4 possible actions (move forward, move backward, turn left, turn right)
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = CarRacingEnv()  # assuming this is your new game environment

    game.render()
    
    while True:
        for event in game.pygame.event.get():
            if event.type == game.pygame.QUIT:  # If close button is pressed
                game.pygame.quit()
            if event.type == game.pygame.KEYDOWN:  # If a key is pressed
                if event.key == game.pygame.K_ESCAPE:  # If Escape is pressed
                    game.pygame.quit()
                    
        # get old state 
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.step(final_move)  # assuming step method in the new game
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()  # assuming reset method in the new game
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

if __name__ == '__main__':
    train()
