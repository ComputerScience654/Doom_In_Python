import pygame
import math
import numpy as np

# กำหนดค่าพื้นฐานของเกม
WIDTH, HEIGHT = 800, 600
FOV = math.pi / 3  # 60 องศา
NUM_RAYS = 120  # จำนวนรังสีที่ยิงออกไป
MAX_DEPTH = 800  # ระยะที่รังสีเดินทางไปได้ไกลสุด
TILE_SIZE = 50  # ขนาดของช่องตารางแผนที่

# กำหนดสี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)

# สร้างแผนที่
MAP = [
    "1111111111",
    "1000000001",
    "1000000001",
    "1000000001",
    "1000000001",
    "1000000001",
    "1000000001",
    "1111111111"
]
MAP_W, MAP_H = len(MAP[0]), len(MAP)

# สร้างหน้าจอ pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ตำแหน่งเริ่มต้นของผู้เล่น
player_x, player_y = 150, 150
player_angle = math.pi / 4  # มุมมองเริ่มต้น

def cast_rays():
    """ ยิงรังสีออกไปแล้ววาดกำแพงตามระยะที่ชน """
    for ray in range(NUM_RAYS):
        ray_angle = player_angle - (FOV / 2) + (ray / NUM_RAYS) * FOV
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # หาค่ากระทบกำแพง
        for depth in range(1, MAX_DEPTH, 5):
            target_x = int(player_x + cos_a * depth)
            target_y = int(player_y + sin_a * depth)
            
            col, row = target_x // TILE_SIZE, target_y // TILE_SIZE
            if MAP[row][col] == "1":  # ถ้าชนกำแพง
                depth *= math.cos(player_angle - ray_angle)  # แก้ Distortion
                wall_height = int(50000 / (depth + 0.0001))  # คำนวณขนาดกำแพง
                pygame.draw.rect(screen, GRAY, (ray * (WIDTH // NUM_RAYS), HEIGHT // 2 - wall_height // 2, WIDTH // NUM_RAYS, wall_height))
                break

def move_player(keys):
    """ เคลื่อนที่ตัวละครตามปุ่มกด """
    global player_x, player_y, player_angle
    speed = 3
    if keys[pygame.K_w]:
        player_x += math.cos(player_angle) * speed
        player_y += math.sin(player_angle) * speed
    if keys[pygame.K_s]:
        player_x -= math.cos(player_angle) * speed
        player_y -= math.sin(player_angle) * speed
    if keys[pygame.K_a]:
        player_angle -= 0.05
    if keys[pygame.K_d]:
        player_angle += 0.05

# ลูปเกม
running = True
while running:
    screen.fill(BLACK)

    # จับ event ต่างๆ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # จัดการการเคลื่อนที่
    keys = pygame.key.get_pressed()
    move_player(keys)

    # ยิงรังสีแล้ววาดกำแพง
    cast_rays()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
