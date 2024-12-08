import pygame
import sys
import random
import math
import numpy as np

class CarRacingGameAI:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1000
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Trường đua")
        self.FPS = pygame.time.Clock()

        # Colors
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (128, 128, 128)
        self.GRAY_LIGHT = (192, 192, 192)

        # Load resources
        self.BG = pygame.image.load("Textures/bg.jpg")
        self.BG = pygame.transform.scale(self.BG, (self.WIDTH, self.HEIGHT))
        self.car = pygame.image.load("Textures/car.png")
        self.car = pygame.transform.scale(self.car, (30, 30))
        self.car_rect = self.car.get_rect(topleft=(85, 320))

        # Roads, walls, obstacles
        self.init_track_and_walls()
        self.init_obstacles()
        self.previous_position = self.car_rect.topleft
        self.velocity = (0, 0)

        # State and rewards
        self.car_speed = 3
        self.score = 0
        self.finished = False

    def init_track_and_walls(self):
        self.roads = [
            pygame.Rect(50, 50, self.WIDTH - 350, 100),
            pygame.Rect(550, 150, 300, 100),
            pygame.Rect(750, 250, 100, 200),
            pygame.Rect(850, 350, 100, 400),
            pygame.Rect(550, 650, 400, 100),
            pygame.Rect(550, 350, 100, 300),
            pygame.Rect(250, 350, 300, 100),
            pygame.Rect(250, 450, 100, 300),
            pygame.Rect(150, 650, 100, 100),
            pygame.Rect(50, 150, 100, 600),
        ]
        self.walls = [
            pygame.Rect(50, 30, 670, 20), pygame.Rect(150, 150, 400, 20),
            pygame.Rect(700, 50, 20, 100), pygame.Rect(550, 250, 180, 20),
            pygame.Rect(530, 170, 20, 100), pygame.Rect(720, 130, 150, 20),
            pygame.Rect(730, 250, 20, 200), pygame.Rect(730, 450, 100, 20),
            pygame.Rect(850, 150, 20, 200), pygame.Rect(830, 450, 20, 180),
            pygame.Rect(950, 350, 20, 420), pygame.Rect(870, 330, 100, 20),
            pygame.Rect(550, 750, 400, 20), pygame.Rect(670, 630, 180, 20),
            pygame.Rect(650, 330, 20, 320), pygame.Rect(530, 470, 20, 300),
            pygame.Rect(230, 330, 420, 20), pygame.Rect(350, 450, 200, 20),
            pygame.Rect(350, 470, 20, 300), pygame.Rect(230, 350, 20, 280),
            pygame.Rect(30, 750, 320, 20), pygame.Rect(150, 630, 100, 20),
            pygame.Rect(30, 30, 20, 720), pygame.Rect(150, 170, 20, 460),
        ]

    def init_obstacles(self):
        self.obstacles = [
            pygame.Rect(120, 50, 30, 30),
            pygame.Rect(250, 120, 30, 30),
            pygame.Rect(350, 50, 30, 30),
            pygame.Rect(450, 120, 30, 30),
            pygame.Rect(500, 50, 30, 30),
            pygame.Rect(600, 70, 30, 30),
            pygame.Rect(250, 50, 30, 30),
            pygame.Rect(170, 120, 30, 30),
            
            pygame.Rect(850, 450, 30, 100),
            pygame.Rect(860, 450, 30, 100),
            pygame.Rect(870, 450, 30, 100),
            pygame.Rect(880, 450, 30, 100),
            pygame.Rect(890, 450, 30, 100),
            pygame.Rect(900, 450, 30, 100),
            pygame.Rect(910, 450, 30, 100),
            pygame.Rect(920, 450, 30, 100),
            
            pygame.Rect(300, 370, 30, 30),
            pygame.Rect(400, 400, 30, 30),
            pygame.Rect(540, 400, 30, 30),
            pygame.Rect(620, 400, 30, 30),
        ]
        self.moving_obstacle = pygame.Rect(700, 650, 40, 40)
        self.moving_obstacle_speed = 1

    def reset(self):
        self.car_rect.topleft = (85, 320)
        self.score = 0
        self.finished = False
        self.velocity = (0, 0)
        # Return the initial observation
        return self.get_observation()

    def play_step(self, action):
        self.handle_action(action)
        self.update_environment()
        observation = self.get_observation()
        reward = self.calculate_reward()
        done = self.check_done()
        return observation, reward, done

    def handle_action(self, action):
        if action == 0:  # Up
            self.car_rect.y -= self.car_speed
        elif action == 1:  # Down
            self.car_rect.y += self.car_speed
        elif action == 2:  # Left
            self.car_rect.x -= self.car_speed
        elif action == 3:  # Right
            self.car_rect.x += self.car_speed

    def update_environment(self):
        # Update moving obstacles
        self.moving_obstacle.y += self.moving_obstacle_speed
        if self.moving_obstacle.bottom >= 750 or self.moving_obstacle.top <= 650:
            self.moving_obstacle_speed = -self.moving_obstacle_speed
            
        # Calculate velocity
        delta_time = self.FPS.get_time() / 1000.0  # Time in seconds since the last frame
        current_position = self.car_rect.topleft
        displacement = (current_position[0] - self.previous_position[0],
                        current_position[1] - self.previous_position[1])
        self.velocity = (displacement[0] / delta_time, displacement[1] / delta_time) if delta_time > 0 else (0, 0)
    
        # Update the previous position
        self.previous_position = current_position
        
    def get_observation(self):
        walls_and_obstacles = self.walls + [self.moving_obstacle] + self.obstacles
        ray_distances = self.ray_casting(self.car_rect, walls_and_obstacles)
        return np.array(ray_distances, dtype=np.float32)

    def ray_casting(self, car_rect, obstacles, num_rays=11, max_distance=300):
        origin = car_rect.midright
        angles = np.linspace(-math.pi / 2, math.pi / 2, num_rays)
        distances = []

        for angle in angles:
            for dist in range(max_distance):
                x = origin[0] + dist * math.cos(angle)
                y = origin[1] + dist * math.sin(angle)
                if any(obs.collidepoint(x, y) for obs in obstacles):
                    distances.append(dist)
                    break
            else:
                distances.append(max_distance)
        return distances

    def calculate_reward(self):
        if self.car_rect.colliderect(self.moving_obstacle):
            return -10  # Penalty for hitting a moving obstacle
        if self.car_rect.colliderect(self.roads[0]):  # Replace with the finish line
            return 10  # Reward for reaching the finish line
        return -1  # Small penalty for each step

    def check_done(self):
        return self.car_rect.colliderect(self.roads[0])  # Replace with the finish line

    def render(self):
        self.screen.blit(self.BG, (0, 0))
        pygame.draw.rect(self.screen, self.GRAY_LIGHT, self.car_rect)
        for wall in self.walls:
            pygame.draw.rect(self.screen, self.WHITE, wall)
        pygame.draw.rect(self.screen, self.GRAY_LIGHT, self.moving_obstacle)
        
        # Display velocity on the screen
        font = pygame.font.SysFont(None, 24)
        velocity_text = font.render(f"Velocity: {self.velocity}", True, self.WHITE)
        self.screen.blit(velocity_text, (10, 10))
    
        pygame.display.flip()
