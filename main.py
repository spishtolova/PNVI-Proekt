import pygame
import sys
import random
import math

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Toon World theme.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catz")

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 20)
bamboo_font = pygame.font.Font("Da Bamboo.ttf.ttf", 48)

menu_img = pygame.image.load("assets/FreeDemo.png").convert_alpha()
menu_img = pygame.transform.scale(menu_img, (300, 300))
menu_rect = menu_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

forest_bg = pygame.image.load("assets/forest.jpg").convert()
forest_bg = pygame.transform.scale(forest_bg, (WIDTH, HEIGHT))

waterfall_bg = pygame.image.load("assets/waterfall.jpg").convert()
waterfall_bg = pygame.transform.scale(waterfall_bg, (WIDTH, HEIGHT))

play_button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 - 65, 120, 40)
settings_button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 - 15, 120, 40)
quit_button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 35, 120, 40)

MAIN_MENU = "main_menu"
GAME_LOADING = "game_loading"
SETTINGS = "settings"
PLAYING = "playing"
current_state = MAIN_MENU

loading_start_time = None
LOADING_DURATION = 3000


def play_game():
    global current_state, loading_start_time
    current_state = GAME_LOADING
    loading_start_time = pygame.time.get_ticks()


def quit_game():
    pygame.quit()
    sys.exit()


def show_settings():
    global current_state
    current_state = SETTINGS


def restart_game():
    global current_state
    current_state = MAIN_MENU


def run_level():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    GROUND_COLOR = (34, 139, 34)
    PLATFORM_COLOR = (139, 69, 19)
    gravity = 0.5
    scroll_threshold = 200
    game_over = False
    game_won = False
    paused = False

    title_font = pygame.font.SysFont('Arial', 48, bold=True)

    # Load images
    star_img = pygame.image.load("assets/star.png").convert_alpha()
    star_img = pygame.transform.scale(star_img, (30, 30))
    red_crystal_img = pygame.image.load("assets/red_crystal.png").convert_alpha()
    red_crystal_img = pygame.transform.scale(red_crystal_img, (30, 30))
    blue_crystal_img = pygame.image.load("assets/blue_crystal.png").convert_alpha()
    blue_crystal_img = pygame.transform.scale(blue_crystal_img, (30, 30))
    heart_img = pygame.image.load("assets/heart.png").convert_alpha()
    heart_img = pygame.transform.scale(heart_img, (25, 25))
    star_shadow_img = pygame.image.load("assets/starShadow.png").convert_alpha()
    star_shadow_img = pygame.transform.scale(star_shadow_img, (20, 20))
    red_shadow_img = pygame.image.load("assets/redcrystalShadow.png").convert_alpha()
    red_shadow_img = pygame.transform.scale(red_shadow_img, (20, 20))
    blue_shadow_img = pygame.image.load("assets/bluecrystalShadow.png").convert_alpha()
    blue_shadow_img = pygame.transform.scale(blue_shadow_img, (20, 20))

    class SpriteSheet():
        def __init__(self, image):
            self.sheet = image

        def get_image(self, frame, width, height, scale):
            image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
            image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))
            image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            return image

    # Player animation
    cat_frame_width = 256 // 8
    cat_frame_height = 18
    cat_scale = 2.5
    cat_sheet_img = pygame.image.load('assets/CatWalk.png').convert_alpha()
    cat_sprite_sheet = SpriteSheet(cat_sheet_img)
    cat_frames = [cat_sprite_sheet.get_image(i, cat_frame_width, cat_frame_height, cat_scale) for i in range(8)]

    # Enemy animation
    enemy_frame_width = 48
    enemy_frame_height = 48
    enemy_scale = 1.5
    enemy_sheet_img = pygame.image.load('assets/DogWalk.png').convert_alpha()
    enemy_sprite_sheet = SpriteSheet(enemy_sheet_img)
    enemy_frames = [enemy_sprite_sheet.get_image(i, enemy_frame_width, enemy_frame_height, enemy_scale) for i in
                    range(6)]

    class Player:
        def __init__(self, x, y):
            self.reset(x, y)

        def reset(self, x, y):
            self.x = x
            self.y = y
            self.vel_y = 0
            self.jump_power = -12
            self.speed = 5
            self.width = int(cat_frame_width * cat_scale)
            self.height = int(cat_frame_height * cat_scale)
            self.direction = 1
            self.invincible = 0
            self.shooting_power = False
            self.lives = 3
            self.projectiles = []
            self.animation_counter = 0
            self.jumping = False
            self.current_frame = 0
            self.animation_speed = 0.2

        def update(self, platforms, enemies, powerups, scroll):
            dx = 0
            dy = 0

            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx = -self.speed
                self.direction = -1
                self.animation_counter += 1
            elif key[pygame.K_RIGHT]:
                dx = self.speed
                self.direction = 1
                self.animation_counter += 1
            else:
                self.animation_counter = 0

            if key[pygame.K_SPACE] and not self.jumping:
                self.vel_y = self.jump_power
                self.jumping = True
            if key[pygame.K_z] and self.shooting_power:
                self.shoot()

            self.vel_y += gravity
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            for platform in platforms:
                if platform.rect.colliderect(self.x + dx, self.y, self.width, self.height):
                    dx = 0
                if platform.rect.colliderect(self.x, self.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = platform.rect.bottom - self.y
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = platform.rect.top - self.y - self.height
                        self.vel_y = 0
                        self.jumping = False

            for enemy in enemies:
                if enemy.rect.colliderect(self.x, self.y, self.width,
                                          self.height) and self.invincible <= 0 and not enemy.stunned:
                    self.lives -= 1
                    self.invincible = 60
                    if self.lives <= 0:
                        return True

            for powerup in powerups[:]:
                if powerup.rect.colliderect(self.x, self.y, self.width, self.height):
                    if powerup.type == "star":
                        self.invincible = 180
                    elif powerup.type == "red_crystal":
                        self.shooting_power = True
                    elif powerup.type == "blue_crystal":
                        self.lives += 1
                    powerups.remove(powerup)

            self.x += dx
            self.y += dy

            for proj in self.projectiles[:]:
                proj[0].x += proj[1] * 7
                if proj[0].x < scroll or proj[0].x > scroll + SCREEN_WIDTH:
                    self.projectiles.remove(proj)

            if self.invincible > 0:
                self.invincible -= 1

            if self.x < 0:
                self.x = 0
            if self.x > SCREEN_WIDTH - self.width:
                self.x = SCREEN_WIDTH - self.width

            if self.animation_counter > 0:
                self.current_frame += self.animation_speed
                if self.current_frame >= len(cat_frames):
                    self.current_frame = 0
            else:
                self.current_frame = 0

            return False

        def shoot(self):
            if len(self.projectiles) < 3:
                proj_rect = pygame.Rect(self.x + self.width // 2, self.y + self.height // 2, 8, 4)
                self.projectiles.append([proj_rect, self.direction])

        def draw(self, screen, scroll):
            for proj in self.projectiles:
                pygame.draw.rect(screen, (255, 0, 0), (proj[0].x - scroll, proj[0].y, proj[0].width, proj[0].height))

            if self.invincible > 0 and self.invincible % 6 < 3:
                return

            frame = cat_frames[int(self.current_frame)]
            if self.direction == -1:
                frame = pygame.transform.flip(frame, True, False)
            screen.blit(frame, (self.x - scroll, self.y))

    class Platform:
        def __init__(self, x, y, width, height):
            self.rect = pygame.Rect(x, y, width, height)

        def draw(self, screen, scroll):
            pygame.draw.rect(screen, PLATFORM_COLOR,
                             (self.rect.x - scroll, self.rect.y, self.rect.width, self.rect.height))
            pygame.draw.rect(screen, GROUND_COLOR, (self.rect.x - scroll, self.rect.y, self.rect.width, 5))

    class Enemy:
        def __init__(self, x, y, width, height):
            self.rect = pygame.Rect(x, y, width, height)
            self.direction = 1
            self.move_counter = 0
            self.animation_counter = 0
            self.current_frame = 0
            self.animation_speed = 0.2
            self.invincible = 0
            self.hit_flash = False
            self.health = 2
            self.stunned = False
            self.stun_timer = 0
            self.stun_duration = 90

        def update(self, platforms, player_projectiles, scroll):
            if self.stunned:
                self.stun_timer -= 1
                if self.stun_timer <= 0:
                    self.stunned = False
                return False

            if self.invincible > 0:
                self.invincible -= 1

            self.rect.x += self.direction
            self.move_counter += 1
            self.animation_counter += 1

            self.current_frame += self.animation_speed
            if self.current_frame >= len(enemy_frames):
                self.current_frame = 0

            if self.move_counter > 50:
                self.direction *= -1
                self.move_counter = 0

            for proj in player_projectiles[:]:
                proj_rect = pygame.Rect(proj[0].x - scroll, proj[0].y, proj[0].width, proj[0].height)
                if self.rect.colliderect(proj_rect) and self.invincible == 0:
                    player_projectiles.remove(proj)
                    self.invincible = 30
                    self.health -= 1
                    self.stunned = True
                    self.stun_timer = self.stun_duration
                    if self.health <= 0:
                        return True
            return False

        def draw(self, screen, scroll):
            frame = enemy_frames[int(self.current_frame)]
            if self.stunned:
                frame = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
                frame.fill((100, 100, 255, 100))

            if self.direction < 0:
                frame = pygame.transform.flip(frame, True, False)
            screen.blit(frame, (self.rect.x - scroll, self.rect.y))

    class Powerup:
        def __init__(self, x, y, type):
            self.rect = pygame.Rect(x, y, 30, 30)
            self.type = type
            self.animation_counter = 0

        def update(self):
            self.animation_counter += 1

        def draw(self, screen, scroll):
            y_offset = math.sin(self.animation_counter * 0.1) * 5
            if self.type == "star":
                screen.blit(star_img, (self.rect.x - scroll, self.rect.y + y_offset))
            elif self.type == "red_crystal":
                screen.blit(red_crystal_img, (self.rect.x - scroll, self.rect.y + y_offset))
            elif self.type == "blue_crystal":
                screen.blit(blue_crystal_img, (self.rect.x - scroll, self.rect.y + y_offset))

    class Goal:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 30, 60)
            self.animation_counter = 0

        def update(self):
            self.animation_counter += 1

        def draw(self, screen, scroll):
            pygame.draw.rect(screen, (200, 200, 200), (self.rect.x - scroll + 14, self.rect.y, 2, 60))
            flag_offset = math.sin(self.animation_counter * 0.1) * 3
            pygame.draw.polygon(screen, (255, 50, 50), [
                (self.rect.x - scroll + 16, self.rect.y + 20 + flag_offset),
                (self.rect.x - scroll + 16, self.rect.y + 40 + flag_offset),
                (self.rect.x - scroll + 36, self.rect.y + 30 + flag_offset)
            ])

    def create_level():
        platforms = [
            Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
            Platform(150, 500, 150, 20),
            Platform(400, 450, 200, 20),
            Platform(200, 380, 200, 20),
            Platform(500, 350, 150, 20),
            Platform(100, 300, 200, 20),
            Platform(400, 250, 150, 20),
            Platform(200, 180, 100, 20),
            Platform(500, 150, 150, 20),
            Platform(300, 100, 100, 20)
        ]

        enemies = [
            Enemy(300, SCREEN_HEIGHT - 105, 30, 30),
            Enemy(500, 385, 30, 30),
            Enemy(250, 315, 30, 30),
            Enemy(550, 285, 30, 30),
            Enemy(200, 235, 30, 30),
            Enemy(450, 185, 30, 30)
        ]

        powerups = [
            Powerup(150, 460, "star"),
            Powerup(450, 410, "red_crystal"),
            Powerup(250, 330, "blue_crystal"),
            Powerup(550, 300, "star"),
            Powerup(200, 250, "blue_crystal"),
            Powerup(500, 200, "red_crystal")
        ]

        goal = Goal(350, 60)
        player = Player(50, SCREEN_HEIGHT - 40 - int(cat_frame_height * cat_scale))
        return platforms, enemies, powerups, goal, player

    platforms, enemies, powerups, goal, player = create_level()
    clock = pygame.time.Clock()
    scroll = 0

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game_over or game_won):
                    platforms, enemies, powerups, goal, player = create_level()
                    game_over = False
                    game_won = False
                    scroll = 0
                if event.key == pygame.K_p and not game_over and not game_won:
                    paused = not paused

        if not game_over and not game_won and not paused:
            game_over = player.update(platforms, enemies, powerups, scroll)

            for enemy in enemies[:]:
                if enemy.update(platforms, player.projectiles, scroll):
                    enemies.remove(enemy)

            for powerup in powerups:
                powerup.update()

            goal.update()

            if player.x + player.width > goal.rect.x and player.x < goal.rect.x + goal.rect.width and \
                    player.y + player.height > goal.rect.y and player.y < goal.rect.y + goal.rect.height:
                game_won = True

            if player.x > SCREEN_WIDTH - scroll_threshold:
                scroll += player.x - (SCREEN_WIDTH - scroll_threshold)
            elif player.x < scroll_threshold:
                scroll -= scroll_threshold - player.x

            scroll = max(0, min(scroll, SCREEN_WIDTH * 2 - SCREEN_WIDTH))

        screen.blit(waterfall_bg, (0, 0))

        for platform in platforms:
            platform.draw(screen, scroll)

        for enemy in enemies:
            enemy.draw(screen, scroll)

        for powerup in powerups:
            powerup.draw(screen, scroll)

        goal.draw(screen, scroll)
        player.draw(screen, scroll)

        pygame.draw.rect(screen, WHITE, (10, 10, 200, 90), border_radius=10)
        pygame.draw.rect(screen, BLACK, (10, 10, 200, 90), width=2, border_radius=10)

        lives_text_surface = font.render('Lives:', True, BLACK)
        screen.blit(lives_text_surface, (20, 25))
        heart_start_x = 20 + lives_text_surface.get_width() + 5

        for i in range(player.lives):
            screen.blit(heart_img, (heart_start_x + i * (heart_img.get_width() + 5), 25))

        powerups_label = font.render("Powerups:", True, BLACK)
        screen.blit(powerups_label, (20, 60))
        icon_x = 20 + powerups_label.get_width() + 10
        icon_y = 60

        if player.invincible > 0:
            screen.blit(star_shadow_img, (icon_x, icon_y))
            icon_x += 30
        if player.shooting_power:
            screen.blit(red_shadow_img, (icon_x, icon_y))
            icon_x += 30
        if player.lives > 3:
            screen.blit(blue_shadow_img, (icon_x, icon_y))

        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            game_over_text = title_font.render('GAME OVER', True, (255, 50, 50))
            restart_text = font.render('Press R to Restart', True, (255, 255, 255))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

        elif game_won:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 100, 0, 150))
            screen.blit(overlay, (0, 0))
            win_text = title_font.render('LEVEL COMPLETE!', True, (50, 255, 50))
            restart_text = font.render('Press R to Play Again', True, (255, 255, 255))
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

        elif paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 100, 150))
            screen.blit(overlay, (0, 0))
            pause_text = title_font.render('GAME PAUSED', True, (100, 100, 255))
            resume_text = font.render('Press P to Resume', True, (255, 255, 255))
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

        pygame.display.update()


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_state == MAIN_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    play_game()
                elif settings_button_rect.collidepoint(event.pos):
                    show_settings()
                elif quit_button_rect.collidepoint(event.pos):
                    quit_game()

        elif current_state == SETTINGS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    restart_game()

    if current_state == MAIN_MENU:
        screen.blit(forest_bg, (0, 0))
        catz_logo = pygame.image.load("assets/catzlogo.png").convert_alpha()
        catz_logo = pygame.transform.scale(catz_logo, (400, 250))
        screen.blit(catz_logo, (WIDTH // 2 - catz_logo.get_width() // 2, -15))
        screen.blit(menu_img, menu_rect)

    elif current_state == SETTINGS:
        screen.blit(forest_bg, (0, 0))
        controls_rect = pygame.Rect(WIDTH // 2 - 320, HEIGHT // 2 - 240, 640, 480)
        pygame.draw.rect(screen, WHITE, controls_rect, border_radius=20)
        pygame.draw.rect(screen, DARK_GRAY, controls_rect, width=2, border_radius=20)
        controls_title = bamboo_font.render("Controls", True, BLACK)
        screen.blit(controls_title, (WIDTH // 2 - controls_title.get_width() // 2, HEIGHT // 2 - 220))
        controls_text = [
            "Arrow Keys - Move",
            "SPACE - Jump",
            "Z - Shoot (With Red Crystal Powerup)",
            "",
            "Power Ups:",
            "Star - Invincibility (5s)",
            "Red Crystal - Shooting Power",
            "Blue Crystal - Extra Life",
            "",
            "Press ESC to go back to the main menu"
        ]
        total_text_height = len(controls_text) * 35
        start_y = HEIGHT // 2 - total_text_height // 2 + 30
        for i, line in enumerate(controls_text):
            line_surface = small_font.render(line, True, BLACK)
            screen.blit(line_surface, (WIDTH // 2 - line_surface.get_width() // 2, start_y + i * 35))

    elif current_state == GAME_LOADING:
        loading_image = pygame.image.load("assets/loading.png").convert()
        loading_image = pygame.transform.scale(loading_image, (WIDTH, HEIGHT))
        screen.blit(loading_image, (0, 0))
        if pygame.time.get_ticks() - loading_start_time > LOADING_DURATION:
            current_state = PLAYING

    elif current_state == PLAYING:
        run_level()
        restart_game()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()