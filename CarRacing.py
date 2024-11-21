import pygame
import sys
import random
import math


    





class CarGame:

    def getCarPosition(self):
        return self.car_rect.x, self.car_rect.y
    def getFinishLinePosition(self):
        return self.finish_line.x, self.finish_line.y
    
    
    def __init__(self):
        # Khởi tạo Pygame
        pygame.init()

        # Kích thước cửa sổ
        self.WIDTH = 1000
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Trường đua")

        # Load ảnh lên
        self.BG = pygame.image.load("Textures/bg.jpg")
        self.BG = pygame.transform.scale(self.BG, (1000, 800))

        # FPS, tốc độ game
        self.FPS = pygame.time.Clock()

        # Màu sắc
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.GRAY = (128, 128, 128)
        self.GRAY_LIGHT = (192, 192, 192)
        self.YELLOW = (255, 255, 0)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)

        # Tạo các phần của đường đua
        self.create_track()

        # Vật cản di chuyển được
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

        # Thiết lập hình ảnh ban đầu
        self.current_image = self.move1

        # Tạo các chướng ngại vật
        self.create_obstacles()

        # Chọn random các chướng ngại vật
        self.reset_game()

        # Xe
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

        self.score = -1
        self.tmp = self.car
        self.passed_finish_line = False

    def create_track(self):
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

        self.wall_11 = pygame.Rect(50, 30, 670, 20)
        self.wall_13 = pygame.Rect(150, 150, 400, 20)
        self.wall_12 = pygame.Rect(700, 50, 20, 100)
        self.wall_21 = pygame.Rect(550, 250, 180, 20)
        self.wall_22 = pygame.Rect(530, 170, 20, 100)
        self.wall_23 = pygame.Rect(720, 130, 150, 20)
        self.wall_31 = pygame.Rect(730, 250, 20, 200)
        self.wall_32 = pygame.Rect(730, 450, 100, 20)
        self.wall_33 = pygame.Rect(850, 150, 20, 200)
        self.wall_41 = pygame.Rect(830, 450, 20, 180)
        self.wall_42 = pygame.Rect(950, 350, 20, 420)
        self.wall_43 = pygame.Rect(870, 330, 100, 20)
        self.wall_51 = pygame.Rect(550, 750, 400, 20)
        self.wall_52 = pygame.Rect(670, 630, 180, 20)
        self.wall_61 = pygame.Rect(650, 330, 20, 320)
        self.wall_62 = pygame.Rect(530, 470, 20, 300)
        self.wall_71 = pygame.Rect(230, 330, 420, 20)
        self.wall_72 = pygame.Rect(350, 450, 200, 20)
        self.wall_81 = pygame.Rect(350, 470, 20, 300)
        self.wall_82 = pygame.Rect(230, 350, 20, 280)
        self.wall_91 = pygame.Rect(30, 750, 320, 20)
        self.wall_92 = pygame.Rect(150, 630, 100, 20)
        self.wall_101 = pygame.Rect(30, 30, 20, 720)
        self.wall_102 = pygame.Rect(150, 170, 20, 460)
        self.finish_line = pygame.Rect(50, 350, 100, 10)

    def create_obstacles(self):
        self.obstacles_1 = [
            pygame.Rect(120, 50, 30, 30),
            pygame.Rect(250, 120, 30, 30),
            pygame.Rect(350, 50, 30, 30),
            pygame.Rect(450, 120, 30, 30),
            pygame.Rect(500, 50, 30, 30),
            pygame.Rect(600, 70, 30, 30),
            pygame.Rect(250, 50, 30, 30),
            pygame.Rect(170, 120, 30, 30),
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
            pygame.Rect(620, 400, 30, 30),
        ]

    def reset_game(self):
        self.selected_obstacle1 = random.sample(self.obstacles_1, 4)
        self.selected_obstacle4 = random.sample(self.obstacles_4, 1)
        self.selected_obstacle7 = random.sample(self.obstacles_7, 3)

    def draw_track(self, car):
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

        pygame.draw.rect(self.screen, self.WHITE, self.wall_11)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_13)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_12)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_21)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_22)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_23)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_31)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_32)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_33)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_41)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_42)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_43)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_51)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_52)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_61)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_62)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_71)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_72)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_81)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_82)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_91)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_92)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_101)
        pygame.draw.rect(self.screen, self.WHITE, self.wall_102)

        pygame.draw.rect(self.screen, self.GRAY_LIGHT, self.finish_line)

        for i in self.selected_obstacle1:
            pygame.draw.rect(self.screen, self.WHITE, i)

        for i in self.selected_obstacle7:
            pygame.draw.rect(self.screen, self.WHITE, i)

        pygame.draw.rect(self.screen, self.WHITE, self.selected_obstacle4[0])

        self.screen.blit(self.current_image, self.moving_obstacle)
        self.screen.blit(self.move8, self.moving_obstacle_8)
        self.screen.blit(car, self.car_rect)

    def check_collision(self, rect):
        for obstacle in self.selected_obstacle1 + self.selected_obstacle4 + self.selected_obstacle7:
            if rect.colliderect(obstacle):
                return True
        return False

    def check_collision_slime(self, rect):
        if rect.colliderect(self.moving_obstacle_8):
            return True
        return False

    def check_collision_moving_obstacle(self, rect):
        if rect.colliderect(self.moving_obstacle):
            return True
        return False

    def check_collision_wall(self, rect):
        walls = [
            self.wall_11, self.wall_12, self.wall_13, self.wall_21, self.wall_22, self.wall_23,
            self.wall_31, self.wall_32, self.wall_33, self.wall_41, self.wall_42, self.wall_43,
            self.wall_51, self.wall_52, self.wall_61, self.wall_62, self.wall_71, self.wall_72,
            self.wall_81, self.wall_82, self.wall_91, self.wall_92, self.wall_101, self.wall_102
        ]
        for wall in walls:
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

            self.draw_track(self.tmp)
            walls = [
                self.wall_11, self.wall_12, self.wall_13, self.wall_21, self.wall_22, self.wall_23,
                self.wall_31, self.wall_32, self.wall_33, self.wall_41, self.wall_42, self.wall_43,
                self.wall_51, self.wall_52, self.wall_61, self.wall_62, self.wall_71, self.wall_72,
                self.wall_81, self.wall_82, self.wall_91, self.wall_92, self.wall_101, self.wall_102,
                self.moving_obstacle, self.moving_obstacle_8
            ]
            walls.extend(self.selected_obstacle1)
            walls.append(self.selected_obstacle4[0])
            walls.extend(self.selected_obstacle7)

            distances = self.ray_casting(self.car_rect, state, walls)
            print("Ray distances:", distances)
            pygame.display.flip()
            self.FPS.tick(60)


if __name__ == '__main__':
    game = CarGame()
    game.run()