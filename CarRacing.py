import pygame
import sys
import random
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH = 1000
HEIGHT = 800
FPS = 60
CAR_SPEED = 3

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Create the Environment Class
class CarRacingEnv:
    def __init__(self):
        # Screen setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("RL Car Racing")
        
        # Load assets
        self.bg = pygame.image.load("Textures/bg.jpg")
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        self.car = pygame.image.load("Textures/car.png")
        self.car = pygame.transform.scale(self.car, (30, 30))
        self.car_rect = self.car.get_rect(topleft=(85, 320))
        self.car_speed = CAR_SPEED
        
        # Tracks, obstacles, etc.
        self.init_game_elements()
        self.clock = pygame.time.Clock()
        
        # RL setup
        self.state = None
        self.done = False
        self.score = 0
        self.num_rays = 11
        self.max_distance = 300

    def init_game_elements(self):
        # Define roads, walls, obstacles, etc.
        self.roads = [
            pygame.Rect(50, 50, WIDTH - 350, 100),
            pygame.Rect(550, 150, 300, 100),
            pygame.Rect(750, 250, 100, 200),
            pygame.Rect(850, 350, 100, 400),
            pygame.Rect(550, 650, 400, 100),
            pygame.Rect(550, 350, 100, 300),
            pygame.Rect(250, 350, 300, 100),
            pygame.Rect(250, 450, 100, 300),
            pygame.Rect(150, 650, 100, 100),
            pygame.Rect(50, 150, 100, 600)
        ] 
        
        self.walls = [
            pygame.Rect(50, 30, 670, 20),
            pygame.Rect(150, 150, 400, 20),
            pygame.Rect(700, 50, 20, 100),
            pygame.Rect(550, 250, 180, 20),
            pygame.Rect(530, 170, 20, 100),
            pygame.Rect(720, 130, 150, 20),
            pygame.Rect(730, 250, 20, 200),
            pygame.Rect(730, 450, 100, 20),
            pygame.Rect(850, 150, 20, 200),
            pygame.Rect(830, 450, 20, 180),
            pygame.Rect(950, 350, 20, 420),
            pygame.Rect(870, 330, 100, 20),
            pygame.Rect(550, 750, 400, 20),
            pygame.Rect(670, 630, 180, 20),
            pygame.Rect(650, 330, 20, 320),
            pygame.Rect(530, 470, 20, 300),
            pygame.Rect(230, 330, 420, 20),
            pygame.Rect(350, 450, 200, 20),
            pygame.Rect(350, 470, 20, 300),
            pygame.Rect(230, 350, 20, 280),
            pygame.Rect(30, 750, 320, 20),
            pygame.Rect(150, 630, 100, 20),
            pygame.Rect(30, 30, 20, 720),
            pygame.Rect(150, 170, 20, 460)
        ]
        
        
        self.finish_line = pygame.Rect(50, 350, 100, 10)
        self.selected_obstacles = [
            pygame.Rect(random.randint(200, 800), random.randint(200, 600), 30, 30)
            for _ in range(10)
        ]

    def reset(self):
        """Reset the environment for a new episode."""
        self.car_rect.topleft = (85, 320)
        self.done = False
        self.score = 0
        self.state = self.get_state()
        return self.state

    def get_state(self):
        """Compute the state representation using ray casting."""
        distances = self.ray_casting()
        car_position = np.array([self.car_rect.centerx / WIDTH, self.car_rect.centery / HEIGHT])
        return np.concatenate([car_position, distances])

    def ray_casting(self):
        """Perform ray casting for state representation."""
        directions = np.linspace(-60, 60, self.num_rays)  # Spread rays over an angle
        distances = []
        origin = self.car_rect.center
        
        for angle in directions:
            rad_angle = math.radians(angle)
            for d in range(1, self.max_distance):
                end_x = origin[0] + d * math.cos(rad_angle)
                end_y = origin[1] + d * math.sin(rad_angle)
                if self.check_collision((end_x, end_y)):
                    distances.append(d / self.max_distance)  # Normalize
                    break
            else:
                distances.append(1.0)  # Max distance normalized
        
        return np.array(distances)

    def check_collision(self, point):
        """Check if a point collides with walls or obstacles."""
        for wall in [*self.selected_obstacles, *self.walls]:
            if wall.collidepoint(point):
                return True
        return False

    def step(self, action):
        """Perform an action in the environment."""
        if action == 0:  # Move up
            self.car_rect.y -= CAR_SPEED
        elif action == 1:  # Move down
            self.car_rect.y += CAR_SPEED
        elif action == 2:  # Move left
            self.car_rect.x -= CAR_SPEED
        elif action == 3:  # Move right
            self.car_rect.x += CAR_SPEED

        # Compute reward
        reward = self.compute_reward()
        
        # Check if episode ends
        #if self.car_rect.colliderect(self.finish_line):
            #self.done = True
            #reward += 100  # Bonus for reaching the goal
        if self.check_collision(self.car_rect.center):
            self.done = True
            reward -= 50  # Penalty for collision
        
        self.state = self.get_state()
        return self.state, reward, self.done
    
    def is_on_road(self):
        """Check if the car is on the road."""
        car_rect = self.car_rect  # Get the car's rect
        
        # Check if the car's rectangle collides with any road area
        for road in self.roads:
            if car_rect.colliderect(road):
                return 1  # The car is on the road
        
        return 0  # The car is not on the road

    def compute_reward(self):
        """Define a reward function."""
        return -0.1  # Penalize time spent, encourage progress

    def render(self):
        """Render the environment."""
        self.screen.blit(self.bg, (0, 0))
        for i in self.roads:
            pygame.draw.rect(self.screen, GRAY, i)
        
        for i in self.walls:
            pygame.draw.rect(self.screen, WHITE, i)
        
        pygame.draw.rect(self.screen, YELLOW, self.finish_line)
        self.screen.blit(self.car, self.car_rect)
        pygame.display.flip()
        self.clock.tick(FPS)

    def close(self):
        """Close the environment."""
        pygame.quit()
        sys.exit()

# Example interaction with the environment
if __name__ == "__main__":
    env = CarRacingEnv()
    state = env.reset()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If close button is pressed
                done = True
            if event.type == pygame.KEYDOWN:  # If a key is pressed
                if event.key == pygame.K_ESCAPE:  # If Escape is pressed
                    done = True
                    
        # Random action (replace with agent action)
        action = random.choice([0, 1, 2, 3])
        state, reward, done_step = env.step(action)
        done = done or done_step  # Combine manual quit with environment's done
        env.render()
        
    env.close()
    pygame.quit()
