import pygame
import random

# กำหนดค่าสี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# กำหนดขนาดหน้าจอ
WIDTH, HEIGHT = 800, 600

# กำหนดขนาดและความเร็วของ paddle, ball, และ brick
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 75, 30

# กำหนดความเร็วของ paddle และ ball
PADDLE_SPEED = 10
BALL_SPEED_X, BALL_SPEED_Y = 5, -5

# กำหนดจำนวนแถวและคอลัมน์ของ brick
BRICK_ROWS, BRICK_COLS = 5, 10

# กำหนดคลาส Paddle
class Paddle:
    def __init__(self):
        self.x = (WIDTH - PADDLE_WIDTH) // 2
        self.y = HEIGHT - PADDLE_HEIGHT - 10
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed

# กำหนดคลาส Ball
class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = BALL_RADIUS
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # ตรวจสอบการชนขอบหน้าจอ
        if self.x <= 0 or self.x >= WIDTH:
            self.speed_x *= -1
        if self.y <= 0:
            self.speed_y *= -1

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

# กำหนดคลาส Brick
class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = random.choice([RED, GREEN, BLUE])
        self.is_destroyed = False

    def draw(self, screen):
        if not self.is_destroyed:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# ฟังก์ชันแสดงหน้า Game Over
def game_over_screen(screen, score):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 74)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 140, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))

    font = pygame.font.SysFont(None, 50)
    restart_text = font.render("Press R to Restart", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)
    screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 50))
    screen.blit(quit_text, (WIDTH // 2 - 100, HEIGHT // 2 + 100))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # เล่นใหม่
                if event.key == pygame.K_q:
                    return False  # ออกจากเกม

# ฟังก์ชันหลักสำหรับการทำงานของเกม
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Breakout Game")
    clock = pygame.time.Clock()

    while True:
        paddle = Paddle()
        ball = Ball()

        # สร้าง brick ทั้งหมด
        bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                brick = Brick(col * (BRICK_WIDTH + 5) + 30, row * (BRICK_HEIGHT + 5) + 50)
                bricks.append(brick)

        # กำหนดคะแนนและชีวิต
        score = 0
        lives = 3

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move("left")
            if keys[pygame.K_RIGHT]:
                paddle.move("right")

            ball.move()

            # ตรวจสอบการชน paddle
            if (ball.y + ball.radius >= paddle.y and
                paddle.x <= ball.x <= paddle.x + paddle.width):
                ball.speed_y *= -1

            # ตรวจสอบการชน brick
            for brick in bricks:
                if not brick.is_destroyed and (brick.x <= ball.x <= brick.x + brick.width and
                                               brick.y <= ball.y <= brick.y + brick.height):
                    brick.is_destroyed = True
                    ball.speed_y *= -1
                    score += 10  # เพิ่มคะแนนเมื่อทำลาย brick

            # ตรวจสอบการตกออกจากหน้าจอ
            if ball.y >= HEIGHT:
                lives -= 1  # ลดชีวิตเมื่อลูกบอลตก
                if lives == 0:
                    running = False
                else:
                    ball.reset()

            # ลบ brick ที่ถูกทำลายแล้ว
            bricks = [brick for brick in bricks if not brick.is_destroyed]

            # วาดทุกอย่างบนหน้าจอ
            screen.fill(BLACK)
            paddle.draw(screen)
            ball.draw(screen)
            for brick in bricks:
                brick.draw(screen)

            # แสดงคะแนนและชีวิต
            font = pygame.font.SysFont(None, 35)
            score_text = font.render(f"Score: {score}", True, WHITE)
            lives_text = font.render(f"Lives: {lives}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (WIDTH - 100, 10))

            pygame.display.flip()
            clock.tick(60)

        # แสดงหน้า Game Over
        if not game_over_screen(screen, score):
            break

    pygame.quit()

if __name__ == "__main__":
    main()