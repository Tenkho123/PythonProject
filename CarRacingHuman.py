import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trường đua")

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Tạo các phần của đường đua
track_outer_rect = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 200)  # Rìa ngoài
track_inner_rect = pygame.Rect(180, 180, WIDTH - 360, HEIGHT - 360)  # Rìa trong

# Vạch đích nằm ngang theo chiều đường đua
finish_line = pygame.Rect(WIDTH - 200, HEIGHT // 2 - 50, 100, 10)  # Vạch đích nằm ngang

# Tạo các chướng ngại vật
obstacles = [
    pygame.Rect(300, 200, 40, 40),
    pygame.Rect(500, 400, 40, 40),
    pygame.Rect(250, 500, 40, 40)
]

# Vẽ đường đua và chướng ngại vật
def draw_track():
    screen.fill(GREEN)
    # Vẽ rìa ngoài của đường đua
    pygame.draw.rect(screen, GRAY, track_outer_rect, 0)
    pygame.draw.rect(screen, WHITE, track_outer_rect, 20)
    # Vẽ rìa trong của đường đua        
    pygame.draw.rect(screen, GREEN, track_inner_rect, 0)
    pygame.draw.rect(screen, WHITE, track_inner_rect, 20)

    # Vẽ các đường rẽ (khúc cua) bằng các đoạn đường thẳng
    # pygame.draw.line(screen, GRAY, (180, 300), (WIDTH - 180, 300), 20)
    # pygame.draw.line(screen, GRAY, (300, 180), (300, HEIGHT - 180), 20)
    # pygame.draw.line(screen, GRAY, (WIDTH - 300, 180), (WIDTH - 300, HEIGHT - 180), 20)

    # Vẽ vạch đích
    pygame.draw.rect(screen, WHITE, finish_line)
    pygame.draw.line(screen, YELLOW, (finish_line.x, finish_line.y + 10), (finish_line.x + finish_line.width, finish_line.y + 10), 5)

    # Vẽ chướng ngại vật
    # for obstacle in obstacles:
    #     pygame.draw.rect(screen, RED, obstacle)

# Tạo xe đua và đặt vị trí trùng với vạch đích
car = pygame.image.load('Texture/car1.png')  # Thay đường dẫn ảnh xe của bạn
car = pygame.transform.scale(car, (40, 20))
car_rect = car.get_rect(center=(finish_line.x + finish_line.width // 2, finish_line.y + 10))

# Tốc độ xe
car_speed = 5
car_angle = 0

# Biến điểm số
score = 0
font = pygame.font.Font(None, 36)

# Hàm xoay xe
def rotate_car(image, rect, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=rect.center)
    return rotated_image, new_rect

# Hàm kiểm tra va chạm
def check_collision(car_rect):
    # Kiểm tra xem xe có nằm ngoài rìa ngoài hoặc bên trong rìa trong không
    if not track_outer_rect.contains(car_rect) or track_inner_rect.contains(car_rect):
        return True
    # Kiểm tra va chạm với chướng ngại vật
    # for obstacle in obstacles:
    #     if car_rect.colliderect(obstacle):
    #         return True
    return False

# Game loop
clock = pygame.time.Clock()
running = True
passed_finish_line = False  # Biến để kiểm tra xe đã qua vạch đích

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Điều khiển xe
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car_rect.x += int(car_speed * pygame.math.Vector2(1, 0).rotate(-car_angle).x)
        car_rect.y += int(car_speed * pygame.math.Vector2(1, 0).rotate(-car_angle).y)
    if keys[pygame.K_LEFT]:
        car_angle += 5
    if keys[pygame.K_RIGHT]:
        car_angle -= 5

    # Kiểm tra va chạm với tường và chướng ngại vật
    if check_collision(car_rect):
        print("Bạn đã đụng vào tường hoặc chướng ngại vật! Trò chơi kết thúc!")
        running = False  # Kết thúc trò chơi nếu va chạm

    # Kiểm tra va chạm với vạch đích để tăng điểm
    if car_rect.colliderect(finish_line):
        if not passed_finish_line:
            score += 1
            passed_finish_line = True  # Đảm bảo chỉ cộng điểm một lần khi qua vạch đích
    else:
        passed_finish_line = False  # Reset lại biến khi xe rời khỏi vạch đích

    # Vẽ trường đua và xe
    draw_track()
    rotated_car, rotated_rect = rotate_car(car, car_rect, car_angle)
    screen.blit(rotated_car, rotated_rect)
    
    # Hiển thị điểm số
    # score_text = font.render(f"Score: {score}", True, BLACK)
    # screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
