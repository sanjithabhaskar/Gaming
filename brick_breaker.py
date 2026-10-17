import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings (optimized for standard view)
WIDTH, HEIGHT = 500, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Brick Breaker")

# Colors
DARK_BG = (10, 10, 20)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 240, 255)
NEON_PINK = (255, 50, 150)
COLORS = [(255, 50, 80), (255, 180, 50), (50, 220, 150), (50, 150, 255)]

clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 16, bold=True)
big_font = pygame.font.SysFont("monospace", 24, bold=True)

# Game State
score = 0
combo = 0
lives = 3
game_over = False
multiball_active = False

# Paddle
paddle = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, 100, 14)

# Balls list
balls = [{
    'x': WIDTH // 2,
    'y': HEIGHT - 70,
    'dx': random.choice([-3, 3]),
    'dy': -4,
    'radius': 8
}]

# Bricks setup
bricks = []
brick_rows = 4
brick_cols = 6
brick_width = 70
brick_height = 24
brick_padding = 10
offset_top = 60
offset_left = 35

def init_bricks():
    global bricks
    bricks = []
    for r in range(brick_rows):
        for c in range(brick_cols bx := offset_left + c * (brick_width + brick_padding)):
            by = offset_top + r * (brick_height + brick_padding)
            bricks.append({
                'rect': pygame.Rect(bx, by, brick_width, brick_height),
                'color': COLORS[r % len(COLORS)]
            })

init_bricks()

def reset_ball():
    global balls
    balls = [{
        'x': paddle.centerx,
        'y': paddle.y - 15,
        'dx': random.choice([-3, 3]),
        'dy': -4,
        'radius': 8
    }]

running = True
while running:
    screen.fill(DARK_BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                score = 0
                combo = 0
                lives = 3
                game_over = False
                init_bricks()
                reset_ball()

    if not game_over:
        # Paddle Movement
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and paddle.left > 10:
            paddle.x -= 8
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and paddle.right < WIDTH - 10:
            paddle.x += 8

        # Ball Physics & Collisions
        for ball in balls[:]:
            ball['x'] += ball['dx']
            ball['y'] += ball['dy']

            # Wall collisions
            if ball['x'] - ball['radius'] < 10 or ball['x'] + ball['radius'] > WIDTH - 10:
                ball['dx'] *= -1
            if ball['y'] - ball['radius'] < 50:
                ball['dy'] *= -1

            # Floor collision (lose ball/life)
            if ball['y'] > HEIGHT:
                balls.remove(ball)
                if len(balls) == 0:
                    lives -= 1
                    combo = 0
                    if lives <= 0:
                        game_over = True
                    else:
                        reset_ball()
                break

            # Paddle collision
            paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
            if paddle_rect.collidepoint(ball['x'], ball['y'] + ball['radius']):
                ball['dy'] = -abs(ball['dy'])
                # Add English based on hit position
                offset = ball['x'] - paddle.centerx
                ball['dx'] = offset * 0.15
                combo = max(0, combo)

            # Brick collisions
            ball_rect = pygame.Rect(ball['x'] - ball['radius'], ball['y'] - ball['radius'], ball['radius']*2, ball['radius']*2)
            for brick in bricks[:]:
                if ball_rect.colliderect(brick['rect']):
                    bricks.remove(brick)
                    ball['dy'] *= -1
                    score += 10
                    combo += 1
                    
                    # Random Multiball trigger chance
                    if len(bricks) % 8 == 0 and not multiball_active:
                        multiball_active = True
                        balls.append({
                            'x': ball['x'],
                            'y': ball['y'],
                            'dx': -ball['dx'],
                            'dy': ball['dy'],
                            'radius': 8
                        })
                    break

        if len(bricks) == 0:
            init_bricks()
            reset_ball()

    # --- DRAWING GRAPHICS ---
    # Draw Border Frame
    pygame.draw.rect(screen, NEON_BLUE, (10, 10, WIDTH - 20, HEIGHT - 20), 2, border_radius=8)

    # Draw Bricks
    for brick in bricks:
        pygame.draw.rect(screen, brick['color'], brick['rect'], border_radius=4)

    # Draw Paddle
    pygame.draw.rect(screen, NEON_BLUE, paddle, border_radius=6)

    # Draw Balls
    for ball in balls:
        pygame.draw.circle(screen, NEON_PINK, (int(ball['x']), int(ball['y'])), ball['radius'])

    # Draw UI (Score & Combo)
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    combo_text = font.render(f"COMBO: {combo}", True, NEON_BLUE)
    screen.blit(score_text, (25, 25))
    screen.blit(combo_text, (WIDTH - 150, 25))

    if multiball_active and not game_over:
        mb_text = big_font.render("MULTIBALL ACTIVE", True, NEON_PINK)
        screen.blit(mb_text, (WIDTH // 2 - mb_text.get_width() // 2, HEIGHT // 2 - 40))

    if game_over:
        go_text = big_font.render("GAME OVER", True, NEON_PINK)
        restart_text = font.render("Press 'R' to Restart", True, WHITE)
        screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
