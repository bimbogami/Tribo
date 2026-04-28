import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Space Survival")
clock = pygame.time.Clock()

ship_images = [
    pygame.transform.scale(pygame.image.load("ship1.png").convert_alpha(), (120, 120)),
    pygame.transform.scale(pygame.image.load("ship2.png").convert_alpha(), (120, 120))
]

asteroid_sheet = pygame.image.load("AsteroidAnimation_1.png").convert_alpha()

FRAME_WIDTH = asteroid_sheet.get_width() // 4
FRAME_HEIGHT = asteroid_sheet.get_height()

asteroid_frames = []
for i in range(4):
    frame = pygame.Surface((FRAME_WIDTH, FRAME_HEIGHT), pygame.SRCALPHA)
    frame.blit(asteroid_sheet, (0, 0), (i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
    asteroid_frames.append(pygame.transform.scale(frame, (90, 90)))

asteroid_sheet = pygame.image.load("AsteroidAnimation_1.png").convert_alpha()

FRAME_WIDTH = asteroid_sheet.get_width() // 4
FRAME_HEIGHT = asteroid_sheet.get_height()

asteroid_frames = []
for i in range(4):
    frame = pygame.Surface((FRAME_WIDTH, FRAME_HEIGHT), pygame.SRCALPHA)
    frame.blit(asteroid_sheet, (0, 0), (i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
    asteroid_frames.append(pygame.transform.scale(frame, (90, 90)))

restart_img = pygame.transform.scale(pygame.image.load("restart.png").convert_alpha(), (80, 80))
exit_img = pygame.transform.scale(pygame.image.load("exit.png").convert_alpha(), (80, 80))

restart_rect = restart_img.get_rect(center=(WIDTH//2 - 150, HEIGHT//2))
exit_rect = exit_img.get_rect(center=(WIDTH//2 + 150, HEIGHT//2))

trophy_img = pygame.transform.scale(pygame.image.load("New_Highest.png"), (140, 140))

WHITE = (244, 244, 244)

font = pygame.font.Font("fonts/pokemon-emerald.ttf", 48)

stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(150)]

def draw_background():
    screen.fill((10, 12, 30))
    for star in stars:
        pygame.draw.rect(screen, WHITE, (*star, 3, 3))
        star[1] += 2
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0

def reset_player():
    img = random.choice(ship_images)
    rect = img.get_rect(center=(WIDTH // 2, HEIGHT - 150))
    return img, rect

player_img, player_rect = reset_player()

asteroids = []
asteroid_speed = 8
frame_index = 0

def spawn_asteroid():
    x = random.randint(0, WIDTH - 90)
    rect = pygame.Rect(x, -90, 50, 50)
    asteroids.append({"rect": rect, "frame": random.randint(0, 3)})

def move_asteroids():
    for a in asteroids:
        a["rect"].y += asteroid_speed

def draw_asteroids():
    global frame_index
    frame_index += 0.15
    for a in asteroids:
        img = asteroid_frames[int(frame_index) % len(asteroid_frames)]
        screen.blit(img, a["rect"])

def check_collision():
    player_hitbox = player_rect.inflate(-40, -40)
    for a in asteroids:
        asteroid_hitbox = a["rect"].inflate(-35, -35)
        if player_hitbox.colliderect(asteroid_hitbox):
            return True
    return False

MENU = 0
PLAYING = 1
GAME_OVER = 2

state = MENU
score = 0
high_score = 0
new_high = False
spawn_timer = 0

def draw_text(text, y):
    render = font.render(text, True, WHITE)
    rect = render.get_rect(center=(WIDTH // 2, y))
    screen.blit(render, rect)

def reset_game():
    global player_img, player_rect, asteroids, score, spawn_timer, asteroid_speed, new_high
    player_img, player_rect = reset_player()
    asteroids.clear()
    score = 0
    spawn_timer = 0
    asteroid_speed = 8
    new_high = False

while True:
    clock.tick(60)

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if state == MENU and event.key == pygame.K_SPACE:
                state = PLAYING
                reset_game()

    if state == MENU:
        draw_background()
        draw_text("PIXEL SPACE", 400)
        draw_text("Press SPACE to Start", 520)

    elif state == PLAYING:
        spawn_timer += 1
        score += 1

        if score % 500 == 0:
            asteroid_speed += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a] and player_rect.left > 0:
            player_rect.x -= 10
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and player_rect.right < WIDTH:
            player_rect.x += 10

        if spawn_timer > 25:
            spawn_asteroid()
            spawn_timer = 0

        move_asteroids()

        draw_background()
        draw_asteroids()
        screen.blit(player_img, player_rect)

        draw_text(f"Score: {score}", 80)

        if check_collision(): # Logic for high score
            if score > high_score:
                high_score = score
                new_high = True
            state = GAME_OVER

    elif state == GAME_OVER:
        draw_background()

        draw_text("GAME OVER", 300)
        draw_text(f"Score: {score}", 380)
        draw_text(f"High Score: {high_score}", 120)

        if new_high:
            screen.blit(trophy_img, (WIDTH//2 + 220, 60))
            draw_text("NEW HIGHEST!", 200)

        screen.blit(restart_img, restart_rect)
        screen.blit(exit_img, exit_rect)

        if mouse_click:
            if restart_rect.collidepoint(mouse_pos):
                reset_game()
                state = PLAYING
            if exit_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    pygame.display.update()