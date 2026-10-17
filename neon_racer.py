import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Neon Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 16, bold=True)
big_font = pygame.font.SysFont("monospace", 28, bold=True)

# Colors
DARK_BG = (12, 12, 24)
ROAD_GRAY = (30, 30, 45)
NEON_BLUE = (0, 200, 255)
NEON_YELLOW = (255, 220, 0)
NEON_RED = (255, 50, 80)
WHITE = (255, 255, 255)

# Game State
lanes = [135, 250, 365]  # X positions for 3 lanes
lane = 1
score = 0
speed = 6
boost = False
boost_timer = 0
lives = 3
game_over = False

# Player Car
player_width, player_height = 40, 70
player_y = HEIGHT - 120

# Traffic / Obstacles
traffic = []
boost_pads = []

def spawn_obstacle():
    lane_idx = random.randint(0, 2)
    y_pos = random.randint(-400, -100)
    if random.random() < 0.2:
        boost_pads.append({'lane': lane_idx, 'y': y_pos})
    else:
        traffic.append({'lane': lane_idx, 'y': y_pos, 'color': random.choice([NEON_RED, (150, 0, 255)])})

for _ in range(3):
    spawn_obstacle()

running = True
while running:
    screen.fill(DARK_BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and lane > 0 and not game_over:
                lane -= 1
            elif event.key == pygame.K_RIGHT and lane < 2 and not game_over:
                lane += 1
            elif event.key == pygame.K_r and game_over:
                # Reset game
                lane = 1
                score = 0
                speed = 6
                boost = False
                lives = 3
                traffic.clear()
                boost_pads.clear()
                for _ in range(3):
                    spawn_obstacle()
                game_over = False

    if not game_over:
        # Boost mechanics
        if boost:
            current_speed = speed * 2
            boost_timer -= 1
            if boost_timer <= 0:
                boost = False
        else:
            current_speed = speed

        score += int(current_speed // 3)

        # Move Traffic & Boost Pads
        for car in traffic[:]:
            car['y'] += current_speed
            if car['y'] > HEIGHT:
                traffic.remove(car)
                spawn_obstacle()

            # Collision check with player
            player_rect = pygame.Rect(lanes[lane] - player_width//2, player_y, player_width, player_height)
            car_rect = pygame.Rect(lanes[car['lane']] - player_width//2, car['y'], player_width, player_height)
            if player_rect.colliderect(car_rect):
                lives -= 1
                traffic.remove(car)
                spawn_obstacle()
                if lives <= 0:
                    game_over = True

        for pad in boost_pads[:]:
            pad['y'] += current_speed
            if pad['y'] > HEIGHT:
                boost_pads.remove(pad)
                spawn_obstacle()

            # Boost pad collection check
            player_rect = pygame.Rect(lanes[lane] - player_width//2, player_y, player_width, player_height)
            pad_rect = pygame.Rect(lanes[pad['lane']] - 25, pad['y'], 50, 30)
            if player_rect.colliderect(pad_rect):
                boost = True
                boost_timer = 60  # duration of boost
                boost_pads.remove(pad)
                spawn_obstacle()

    # --- DRAWING ---
    # Draw Road
    pygame.draw.rect(screen, ROAD_GRAY, (80, 0, WIDTH - 160, HEIGHT))
    # Lane divider dashes
    for i in range(-20, HEIGHT, 40):
        offset = (pygame.time.get_ticks() * int(current_speed) // 10) % 40
        pygame.draw.line(screen, WHITE, (195, i + offset), (195, i + 20 + offset), 2)
        pygame.draw.line(screen, WHITE, (305, i + offset), (305, i + 20 + offset), 2)

    # Draw Boost Pads
    for pad in boost_pads:
        pygame.draw.polygon(screen, NEON_YELLOW, [
            (lanes[pad['lane']], pad['y']),
            (lanes[pad['lane']] - 20, pad['y'] + 25),
            (lanes[pad['lane']] + 20, pad['y'] + 25)
        ])

    # Draw Traffic Cars
    for car in traffic:
        car_rect = pygame.Rect(lanes[car['lane']] - player_width//2, car['y'], player_width, player_height)
        pygame.draw.rect(screen, car['color'], car_rect, border_radius=8)

    # Draw Player Car
    player_x = lanes[lane] - player_width // 2
    pygame.draw.rect(screen, NEON_BLUE, (player_x, player_y, player_width, player_height), border_radius=8)

    # UI Top Bar
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    speed_text = font.render(f"SPEED: {int(current_speed * 10)}", True, NEON_YELLOW)
    screen.blit(score_text, (20, 20))
    screen.blit(speed_text, (WIDTH - 160, 20))

    if boost:
        boost_msg = big_font.render("BOOST x2", True, NEON_YELLOW)
        screen.blit(boost_msg, (WIDTH // 2 - boost_msg.get_width() // 2, 70))

    if game_over:
        go_text = big_font.render("CRASHED / GAME OVER", True, NEON_RED)
        restart_text = font.render("Press 'R' to Restart", True, WHITE)
        screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 25))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
