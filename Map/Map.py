import pygame
import sys
import random
import math
# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trường đua")

#load ảnh lên
BG = pygame.image.load("bg.jpg")
BG = pygame.transform.scale(BG, (1000,800))
#FPS, tốc độ game
FPS = pygame.time.Clock()
# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
GRAY_LIGHT = (192, 192, 192)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Tạo các phần của đường đua
road_1 = pygame.Rect(50, 50, WIDTH - 350, 100) 
road_2 = pygame.Rect(550, 150, 300, 100)  
road_3 = pygame.Rect(750, 250, 100, 200)  
road_4 = pygame.Rect(850, 350, 100, 400)  
road_5 = pygame.Rect(550, 650, 400, 100)
road_6 = pygame.Rect(550, 350, 100, 300)
road_7 = pygame.Rect(250, 350, 300, 100)
road_8 = pygame.Rect(250, 450, 100, 300)    
road_9 = pygame.Rect(150, 650, 100, 100)
road_10 = pygame.Rect(50, 150, 100, 600)    

#Vật cản di chuyển được
moving_obstacle = pygame.Rect(700, 650, 40, 40)  # Đặt vị trí ban đầu (trong khoảng road_5)
moving_obstacle_speed = 1
# Thay đổi hình ảnh của vật cản di chuyển
move1 = pygame.image.load("move1.png")
move1 = pygame.transform.scale(move1, (40, 40))
move2 = pygame.image.load("move2.png")
move2 = pygame.transform.scale(move2, (40, 40))

moving_obstacle_8 = pygame.Rect(280, 450, 30, 30)  # Vị trí ban đầu (trong khoảng road_8)
moving_obstacle_8_speed = 1
#Vật cản slime (làm chậm)
move8 = pygame.image.load("move8.png")
move8 = pygame.transform.scale(move8, (30, 30))
# Thiết lập hình ảnh ban đầu
current_image = move1
#Tạo các tường của đường đua
wall_11 = pygame.Rect(50, 30, 670, 20)
wall_13 = pygame.Rect(150, 150, 400, 20)
wall_12 = pygame.Rect(700, 50, 20, 100)
wall_21 = pygame.Rect(550, 250, 180, 20)
wall_22 = pygame.Rect(530, 170, 20, 100)
wall_23 = pygame.Rect(720, 130, 150, 20)
wall_31 = pygame.Rect(730, 250, 20, 200)
wall_32 = pygame.Rect(730, 450, 100, 20)
wall_33 = pygame.Rect(850, 150, 20, 200)
wall_41 = pygame.Rect(830, 450, 20, 180)
wall_42 = pygame.Rect(950, 350, 20, 420)
wall_43 = pygame.Rect(870, 330, 100, 20)
wall_51 = pygame.Rect(550, 750, 400, 20)
wall_52 = pygame.Rect(670, 630, 180, 20)
wall_61 = pygame.Rect(650, 330, 20, 320)
wall_62 = pygame.Rect(530, 470, 20, 300)
wall_71 = pygame.Rect(230, 330, 420, 20)
wall_72 = pygame.Rect(350, 450, 200, 20)
wall_81 = pygame.Rect(350, 470, 20, 300)
wall_82 = pygame.Rect(230, 350, 20, 280)
wall_91 = pygame.Rect(30, 750, 320, 20)
wall_92 = pygame.Rect(150, 630, 100, 20)
wall_101 = pygame.Rect(30, 30, 20, 720)
wall_102 = pygame.Rect(150, 170, 20, 460)
# Vạch đích 
finish_line = pygame.Rect(50,350, 100, 10) 

# Tạo các chướng ngại vật
obstacles_1 = [
    pygame.Rect(120, 50, 30, 30),
    pygame.Rect(250, 120, 30, 30),
    pygame.Rect(350, 50, 30, 30),
    pygame.Rect(450, 120, 30, 30),
    pygame.Rect(500, 50, 30, 30),
    pygame.Rect(600, 70, 30, 30),
    pygame.Rect(250, 50, 30, 30),
    pygame.Rect(170, 120, 30, 30),
]

obstacles_4 = [
    pygame.Rect(850, 450, 30, 100),
    pygame.Rect(860, 450, 30, 100),
    pygame.Rect(870, 450, 30, 100),
    pygame.Rect(880, 450, 30, 100),
    pygame.Rect(890, 450, 30, 100),
    pygame.Rect(900, 450, 30, 100),
    pygame.Rect(910, 450, 30, 100),
    pygame.Rect(920, 450, 30, 100)
]

obstacles_7 = [
    pygame.Rect(300, 370, 30, 30),
    pygame.Rect(400, 400, 30, 30),
    pygame.Rect(540, 400, 30, 30),
    pygame.Rect(620, 400, 30, 30),
]

#chọn random các chướng ngại vật
selected_obstacle1 = random.sample(obstacles_1, 4)
selected_obstacle4 = random.sample(obstacles_4, 1)
selected_obstacle7 = random.sample(obstacles_7, 3)
# Vẽ đường đua và chướng ngại vật
def draw_track(car):
    screen.blit(BG, (0, 0))
    pygame.draw.rect(screen, GRAY, road_1,0)
    pygame.draw.rect(screen, GRAY, road_2,0)
    pygame.draw.rect(screen, GRAY, road_3,0)
    pygame.draw.rect(screen, GRAY, road_4,0)
    pygame.draw.rect(screen, GRAY, road_5,0)
    pygame.draw.rect(screen, GRAY, road_6,0)
    pygame.draw.rect(screen, GRAY, road_7,0)
    pygame.draw.rect(screen, GRAY, road_8,0)
    pygame.draw.rect(screen, GRAY, road_9,0)
    pygame.draw.rect(screen, GRAY, road_10,0)

    pygame.draw.rect(screen, WHITE, wall_11)
    pygame.draw.rect(screen, WHITE, wall_13)
    pygame.draw.rect(screen, WHITE, wall_12)
    pygame.draw.rect(screen, WHITE, wall_21)
    pygame.draw.rect(screen, WHITE, wall_22)
    pygame.draw.rect(screen, WHITE, wall_23)
    pygame.draw.rect(screen, WHITE, wall_31)
    pygame.draw.rect(screen, WHITE, wall_32)
    pygame.draw.rect(screen, WHITE, wall_33)
    pygame.draw.rect(screen, WHITE, wall_41)
    pygame.draw.rect(screen, WHITE, wall_42)
    pygame.draw.rect(screen, WHITE, wall_43)
    pygame.draw.rect(screen, WHITE, wall_51)
    pygame.draw.rect(screen, WHITE, wall_52)
    pygame.draw.rect(screen, WHITE, wall_61)
    pygame.draw.rect(screen, WHITE, wall_62)
    pygame.draw.rect(screen, WHITE, wall_71)
    pygame.draw.rect(screen, WHITE, wall_72)
    pygame.draw.rect(screen, WHITE, wall_81)
    pygame.draw.rect(screen, WHITE, wall_82)
    pygame.draw.rect(screen, WHITE, wall_91)
    pygame.draw.rect(screen, WHITE, wall_92)
    pygame.draw.rect(screen, WHITE, wall_101)
    pygame.draw.rect(screen, WHITE, wall_102)

    pygame.draw.rect(screen, GRAY_LIGHT, finish_line)
    #vẽ từng chướng ngại vật đã random ra
    for i in selected_obstacle1:
        pygame.draw.rect(screen, WHITE, i)

    for i in selected_obstacle7:    
        pygame.draw.rect(screen, WHITE, i)
    
    pygame.draw.rect(screen, WHITE, selected_obstacle4[0])

    screen.blit(current_image, moving_obstacle)
    # Hiển thị vật cản di chuyển trên road_8
    screen.blit(move8, moving_obstacle_8)
    screen.blit(car, car_rect)
car = pygame.image.load('car.png')  
car = pygame.transform.scale(car, (30, 30))
car_rect = car.get_rect(topleft=(85, 320))
car_speed = 3

car1 = pygame.image.load('car1.png')  
car1 = pygame.transform.scale(car1, (30, 30))

car2 = pygame.image.load('car2.png')
car2 = pygame.transform.scale(car2, (30, 30))

car3 = pygame.image.load('car3.png')        
car3 = pygame.transform.scale(car3, (30, 30))

#Hàm kiem tra va cham với các chuong ngai vat tĩnh
def check_collision(rect):
    for obstacle in selected_obstacle1 + selected_obstacle4 + selected_obstacle7:
        if rect.colliderect(obstacle):
            return True
    return False
#Ham kiem tra va cham với slime (làm chậm)
def check_collision_slime(rect): 
    if rect.colliderect(moving_obstacle_8):
        return True
    return False
#Ham kiem tra va cham với vat can di chuyen
def check_collision_moving_obstacle(rect):
    if rect.colliderect(moving_obstacle):
        return True
    return False

#hàm kiểm tra va chạm với tường
def check_collision_wall(rect):
    if rect.colliderect(wall_11):
        return True
    if rect.colliderect(wall_12):
        return True
    if rect.colliderect(wall_13):
        return True
    if rect.colliderect(wall_21):
        return True
    if rect.colliderect(wall_22):
        return True
    if rect.colliderect(wall_23):
        return True
    if rect.colliderect(wall_31):
        return True
    if rect.colliderect(wall_32):
        return True
    if rect.colliderect(wall_33):
        return True
    if rect.colliderect(wall_41):
        return True
    if rect.colliderect(wall_42):
        return True
    if rect.colliderect(wall_43):
        return True
    if rect.colliderect(wall_51):
        return True
    if rect.colliderect(wall_52):
        return True
    if rect.colliderect(wall_61):
        return True
    if rect.colliderect(wall_62):
        return True
    if rect.colliderect(wall_71):
        return True
    if rect.colliderect(wall_72):
        return True
    if rect.colliderect(wall_81):
        return True
    if rect.colliderect(wall_82):
        return True
    if rect.colliderect(wall_91):
        return True
    if rect.colliderect(wall_92):
        return True
    if rect.colliderect(wall_101):
        return True
    if rect.colliderect(wall_102):
        return True
    return False

#hàm reset map khi xe qua vạch đích
def reset_game():
    global selected_obstacle1, selected_obstacle4, selected_obstacle7, car_rect

    selected_obstacle1 = random.sample(obstacles_1, 4)
    selected_obstacle4 = random.sample(obstacles_4, 1)
    selected_obstacle7 = random.sample(obstacles_7, 3)
# Hàm tính khoảng cách giữa hai điểm
def ray_casting(car_rect, state, walls, num_rays=11, max_distance=300):
   
    ray_distances = []  # Lưu khoảng cách các tia
    
    # Tính điểm phát tia (đầu xe)
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
        return []  # Không di chuyển, không phát tia

    # Góc chia đều quanh hướng xe
    angles = [math.radians(base_angle - 60 + i * 120 / (num_rays - 1)) for i in range(num_rays)]

    # Phát tia và kiểm tra va chạm
    for angle in angles:
        for dist in range(1, max_distance):
            # Tính vị trí điểm cuối của tia theo góc
            ray_x = origin[0] + dist * math.cos(angle)
            ray_y = origin[1] + dist * math.sin(angle)
            ray_end = (ray_x, ray_y)

            # Kiểm tra va chạm với tường
            ray_hit = any(wall.collidepoint(ray_end) for wall in walls)
            if ray_hit:
                ray_distances.append(dist)
                break
        else:
            ray_distances.append(max_distance)  # Không va chạm, khoảng cách tối đa

        # Vẽ tia lên màn hình
        pygame.draw.line(screen, YELLOW, origin, ray_end, 1)
        pygame.draw.circle(screen, RED, (int(ray_end[0]), int(ray_end[1])), 3)

    return ray_distances

score = -1
tmp = car
passed_finish_line = False  # Biến để kiểm tra xe đã qua vạch đích
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  
            sys.exit()

    # Cập nhật vị trí của vật cản di chuyển
    moving_obstacle.y += moving_obstacle_speed
    if moving_obstacle.bottom >= road_5.bottom or moving_obstacle.top <= road_5.top:
        moving_obstacle_speed = -moving_obstacle_speed

    moving_obstacle_8.y += moving_obstacle_8_speed
    if moving_obstacle_8.bottom >= road_8.bottom or moving_obstacle_8.top <= road_8.top:
        moving_obstacle_8_speed = -moving_obstacle_8_speed

    # Kiểm tra va chạm và xử lý logic
    if check_collision_slime(car_rect):
        car_speed = 1
    else:
        car_speed = 3

    if check_collision_moving_obstacle(car_rect):
        pygame.time.delay(500)
        car_rect.topleft = (85, 310)

    if check_collision(car_rect):
        pygame.time.delay(500)
        car_rect.topleft = (85, 310)

    if check_collision_wall(car_rect):
        pygame.time.delay(500)
        car_rect.topleft = (85, 310)

    if car_rect.colliderect(finish_line):
        if not passed_finish_line:
            score += 1
            reset_game()
            passed_finish_line = True
    else:
        passed_finish_line = False

    # Điều khiển xe
    keys = pygame.key.get_pressed()
    state = ''
    if keys[pygame.K_w]:
        car_rect.y -= car_speed
        state = 'up'
    if keys[pygame.K_s]:
        car_rect.y += car_speed
        state = 'down'
    if keys[pygame.K_a]:
        car_rect.x -= car_speed
        state = 'left'
    if keys[pygame.K_d]:
        car_rect.x += car_speed
        state = 'right'

    if state == 'down':
        tmp = car
    elif state == 'right':
        tmp = car1
    elif state == 'up':
        tmp = car2
    elif state == 'left':
        tmp = car3

    draw_track(tmp)    
    walls = [
        wall_11, wall_12, wall_13, wall_21, wall_22, wall_23,
        wall_31, wall_32, wall_33, wall_41, wall_42, wall_43,
        wall_51, wall_52, wall_61, wall_62, wall_71, wall_72,
        wall_81, wall_82, wall_91, wall_92, wall_101, wall_102,
        moving_obstacle, moving_obstacle_8

    ]
    walls.extend(selected_obstacle1)
    walls.append(selected_obstacle4[0])
    walls.extend(selected_obstacle7)
    # Gọi hàm ray casting
    distances = ray_casting(car_rect, state, walls)
    print("Ray distances:", distances)
    pygame.display.flip()
    FPS.tick(60)
