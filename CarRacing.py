import pygame
import sys
import random
import math

class CarRacing:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1000
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Trường đua")
        self.BG = pygame.image.load("Textures/bg.jpg")
        self.BG = pygame.transform.scale(self.BG, (self.WIDTH, self.HEIGHT))
        self.FPS = pygame.time.Clock()
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.GRAY_LIGHT = (192, 192, 192)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.init_track()
        self.init_obstacles()
        self.init_car()
        self.score = -1
        self.passed_finish_line = False

    def init_track(self):
        self.road_1 = pygame.Rect(50, 50, self.WIDTH - 350, 100)
        self.road_2 = pygame.Rect(550, 150, 300, 100)
        self.road_3 = pygame.Rect(750, 250, 100, 200)
        self.road_4 = pygame.Rect(850, 350, 100, 400)
        self.road_5 = pygame.Rect(550, 650, 400, 100)
        self.road_6 = pygame.Rect(550, 350, 100, 300)
        self.road_7 = pygame.Rect(250, 350, 300, 100)
        self.road_8 = pygame.Rect(250, 450, 100, 300)
        self.road_9 = pygame.Rect(150, 650, 100, 100)
        self.road_10 = pygame.Rect(50, 150, 100, 600)
        self.moving_obstacle = pygame.Rect(700, 650, 40, 40)
        self.moving_obstacle_speed = 1
        self.move1 = pygame.image.load("Textures/move1.png")
        self.move1 = pygame.transform.scale(self.move1, (40, 40))
        self.move2 = pygame.image.load("Textures/move2.png")
        self.move2 = pygame.transform.scale(self.move2, (40, 40))
        self.moving_obstacle_8 = pygame.Rect(280, 450, 30, 30)
        self.moving_obstacle_8_speed = 1
        self.move8 = pygame.image.load("Textures/move8.png")
        self.move8 = pygame.transform.scale(self.move8, (30, 30))
        self.current_image = self.move1
        self.finish_line = pygame.Rect(50, 350, 100, 10)
        self.init_walls()

    def init_walls(self):
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

    def init_obstacles(self):
        self.obstacles_1 = [
            pygame.Rect(120, 50, 30, 30),
            pygame.Rect(250, 120, 30, 30),
            pygame.Rect(350, 50, 30, 30),
            pygame.Rect(450, 120, 30, 30),
            pygame.Rect(500, 50, 30, 30),
            pygame.Rect(600, 70, 30, 30),
            pygame.Rect(250, 50, 30, 30),
            pygame.Rect(170, 120, 30, 30)
        ]
        self.obstacles_4 = [
            pygame.Rect(850, 450, 30, 100),
            pygame.Rect(860, 450, 30, 100),
            pygame.Rect(870, 450, 30, 100),
            pygame.Rect(880, 450, 30, 100),
            pygame.Rect(890, 450, 30, 100),
            pygame.Rect(900, 450, 30, 100),
            pygame.Rect(910, 450, 30, 100),
            pygame.Rect(920, 450, 30, 100)
        ]
        self.obstacles_7 = [
            pygame.Rect(300, 370, 30, 30),
            pygame.Rect(400, 400, 30, 30),
            pygame.Rect(540, 400, 30, 30),
            pygame.Rect(620, 400, 30, 30)
        ]
        self.reset_game()

    def init_car(self):
        self.car = pygame.image.load('Textures/car.png')
        self.car = pygame.transform.scale(self.car, (30, 30))
        self.car_rect = self.car.get_rect(topleft=(85, 320))
        self.car_speed = 3
        self.car1 = pygame.image.load('Textures/car1.png')
        self.car1 = pygame.transform.scale(self.car1, (30, 30))
        self.car2 = pygame.image.load('Textures/car2.png')
        self.car2 = pygame.transform.scale(self.car2, (30, 30))
        self.car3 = pygame.image.load('Textures/car3.png')
        self.car3 = pygame.transform.scale(self.car3, (30, 30))
        self.tmp = self.car

    def reset_game(self):
        self.selected_obstacle1 = random.sample(self.obstacles_1, 4)
        self.selected_obstacle4 = random.sample(self.obstacles_4, 1)
        self.selected_obstacle7 = random.sample(self.obstacles_7, 3)

    def draw_track(self):
        self.screen.blit(self.BG, (0, 0))
        pygame.draw.rect(self.screen, self.GRAY, self.road_1, 0)
        pygame.draw.rect(self.screen, self.GRAY, self.road_2, 0)
        pygame.draw.rect(self.screen, self.GRAY, self.road_3, 0)
        pygame.draw.rect(self.screen, self.GRAY, self.road_4, 0)
        pygame.draw.rect(self.screen, self.GRAY, self.road_5, 0)
        pygame.draw.rect(self.screen, self.GRAY, self.road_6, 0)
        pygame.draw.rect(self.screen, self.GRAY, self.road_7, 0)
        pygame.draw.rect(self.screen, self.GRAY, self.road_8, 0)
        pygame.draw.rect(self.screen, self.GRAY, self.road_9, 0)
        pygame.draw.rect(self.screen, self.GRAY, self.road_10, 0)
        for wall in self.walls:
            pygame.draw.rect(self.screen, self.WHITE, wall)
        pygame.draw.rect(self.screen, self.GRAY_LIGHT, self.finish_line)
        for obstacle in self.selected_obstacle1:
            pygame.draw.rect(self.screen, self.WHITE, obstacle)
        for obstacle in self.selected_obstacle7:
            pygame.draw.rect(self.screen, self.WHITE, obstacle)
        pygame.draw.rect(self.screen, self.WHITE, self.selected_obstacle4[0])
        self.screen.blit(self.current_image, self.moving_obstacle)
        self.screen.blit(self.move8, self.moving_obstacle_8)
        self.screen.blit(self.tmp, self.car_rect)

    def check_collision(self, rect):
        for obstacle in self.selected_obstacle1 + self.selected_obstacle4 + self.selected_obstacle7:
            if rect.colliderect(obstacle):
                return True
        return False

    def check_collision_slime(self, rect):
        return rect.colliderect(self.moving_obstacle_8)

    def check_collision_moving_obstacle(self, rect):
        return rect.colliderect(self.moving_obstacle)

    def check_collision_wall(self, rect):
        for wall in self.walls:
            if rect.colliderect(wall):
                return True
        return False

    def ray_casting(self, car_rect, state, walls, num_rays=11, max_distance=300):
        ray_distances = []
        if state == 'down':
            origin = car_rect.midbottom
            base_angle = 90
        elif state == 'up':
            origin = car_rect.midtop
            base_angle = -90
        elif state == 'left':
            origin = car_rect.midleft
            base_angle = 180
        elif state == 'right':
            origin = car_rect.midright
            base_angle = 0
        else:
            return []
        angles = [math.radians(base_angle - 60 + i * 120 / (num_rays - 1)) for i in range(num_rays)]
        for angle in angles:
            for dist in range(1, max_distance):
                ray_x = origin[0] + dist * math.cos(angle)
                ray_y = origin[1] + dist * math.sin(angle)
                ray_end = (ray_x, ray_y)
                ray_hit = any(wall.collidepoint(ray_end) for wall in walls)
                if ray_hit:
                    ray_distances.append(dist)
                    break
            else:
                ray_distances.append(max_distance)
            pygame.draw.line(self.screen, self.YELLOW, origin, ray_end, 1)
            pygame.draw.circle(self.screen, self.RED, (int(ray_end[0]), int(ray_end[1])), 3)
        return ray_distances

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.moving_obstacle.y += self.moving_obstacle_speed
            if self.moving_obstacle.bottom >= self.road_5.bottom or self.moving_obstacle.top <= self.road_5.top:
                self.moving_obstacle_speed = -self.moving_obstacle_speed
            self.moving_obstacle_8.y += self.moving_obstacle_8_speed
            if self.moving_obstacle_8.bottom >= self.road_8.bottom or self.moving_obstacle_8.top <= self.road_8.top:
                self.moving_obstacle_8_speed = -self.moving_obstacle_8_speed
            if self.check_collision_slime(self.car_rect):
                self.car_speed = 1
            else:
                self.car_speed = 3
            if self.check_collision_moving_obstacle(self.car_rect):
                pygame.time.delay(500)
                self.car_rect.topleft = (85, 310)
            if self.check_collision(self.car_rect):
                pygame.time.delay(500)
                self.car_rect.topleft = (85, 310)
            if self.check_collision_wall(self.car_rect):
                pygame.time.delay(500)
                self.car_rect.topleft = (85, 310)
            if self.car_rect.colliderect(self.finish_line):
                if not self.passed_finish_line:
                    self.score += 1
                    self.reset_game()
                    self.passed_finish_line = True
            else:
                self.passed_finish_line = False
            keys = pygame.key.get_pressed()
            state = ''
            if keys[pygame.K_w]:
                self.car_rect.y -= self.car_speed
                state = 'up'
            if keys[pygame.K_s]:
                self.car_rect.y += self.car_speed
                state = 'down'
            if keys[pygame.K_a]:
                self.car_rect.x -= self.car_speed
                state = 'left'
            if keys[pygame.K_d]:
                self.car_rect.x += self.car_speed
                state = 'right'
            if state == 'down':
                self.tmp = self.car
            elif state == 'right':
                self.tmp = self.car1
            elif state == 'up':
                self.tmp = self.car2
            elif state == 'left':
                self.tmp = self.car3
            self.draw_track()
            walls = self.walls + [self.moving_obstacle, self.moving_obstacle_8] + self.selected_obstacle1 + [self.selected_obstacle4[0]] + self.selected_obstacle7
            distances = self.ray_casting(self.car_rect, state, walls)
            print("Ray distances:", distances)
            pygame.display.flip()
            self.FPS.tick(60)
    def reset(self):
        """Reset the game and return the initial state."""
        self.car_rect.topleft = (85, 320)
        self.score = 0
        self.passed_finish_line = False
        self.reset_game()
        state = self.get_state()
        return state

    def step(self, action):
        """Perform an action and return the new state, reward, and done flag."""
        state = ''
        if action == 0:  # Move up
            self.car_rect.y -= self.car_speed
            state = 'up'
        elif action == 1:  # Move down
            self.car_rect.y += self.car_speed
            state = 'down'
        elif action == 2:  # Move left
            self.car_rect.x -= self.car_speed
            state = 'left'
        elif action == 3:  # Move right
            self.car_rect.x += self.car_speed
            state = 'right'

        # Update car orientation
        if state == 'down':
            self.tmp = self.car
        elif state == 'right':
            self.tmp = self.car1
        elif state == 'up':
            self.tmp = self.car2
        elif state == 'left':
            self.tmp = self.car3

        # Check collisions and compute reward
        reward = -1  # Default step cost
        done = False
        if self.check_collision(self.car_rect) or self.check_collision_wall(self.car_rect):
            reward = -10
            done = True
        elif self.car_rect.colliderect(self.finish_line):
            reward = 100
            done = True

        next_state = self.get_state()
        return next_state, reward, done

    def get_state(self):
        raycast_distances = self.ray_casting(self.car_rect, 'up', self.walls)
        finish_x, finish_y = self.finish_line.center
        car_x, car_y = self.car_rect.center
        state = [
            car_x,car_y,
            self.car_speed,
            *raycast_distances,
            finish_x - car_x,
            finish_y - car_y
        ]
        return state
    def play_step(self,action):
        state = ''
        if action == 0:  # Move up
            self.car_rect.y -= self.car_speed
            state = 'up'
        elif action == 1:  # Move right
            self.car_rect.x += self.car_speed
            state = 'right'
        elif action == 2:  # Move left
            self.car_rect.x -= self.car_speed
            state = 'left'

        # Update car orientation
        if state == 'down':
            self.tmp = self.car
        elif state == 'right':
            self.tmp = self.car1
        elif state == 'up':
            self.tmp = self.car2
        elif state == 'left':
            self.tmp = self.car3

        # Check collisions and compute reward
        reward = -1  # Default step cost
        done = False
        if self.check_collision(self.car_rect) or self.check_collision_wall(self.car_rect):
            reward = -10
            done = True
        elif self.car_rect.colliderect(self.finish_line):
            reward = 100
            done = True

        next_state = self.get_state()
        return next_state, reward, done
    
    
if __name__ == '__main__':
    game = CarRacing()
    game.run()