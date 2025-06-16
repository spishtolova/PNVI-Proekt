import pygame
import sys
import random
import math


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Toon World theme.mp3")
pygame.mixer.music.set_volume(0.5)  # Optional: set volume between 0.0 and 1.0
pygame.mixer.music.play(-1) 

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catz")

font = pygame.font.SysFont("Arial", 60)
small_font = pygame.font.SysFont("Arial", 20)
bamboo_font = pygame.font.Font("Da Bamboo.ttf.ttf", 48)  # You can change the size


menu_img = pygame.image.load("assets/FreeDemo.png").convert_alpha()
menu_img = pygame.transform.scale(menu_img, (300, 300))
menu_rect = menu_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

forest_bg = pygame.image.load("assets/forest.jpg").convert()
forest_bg = pygame.transform.scale(forest_bg, (WIDTH, HEIGHT))

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
    import pygame
    import sys
    import random
    import math

    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Catz")

    BACKGROUND = (135, 206, 235)
    GROUND_COLOR = (34, 139, 34)
    PLATFORM_COLOR = (139, 69, 19)
    CAT_COLOR = (255, 165, 0)
    ENEMY_COLOR = (220, 20, 60)
    STAR_COLOR = (255, 255, 0)
    RED_CRYSTAL = (220, 20, 60)
    BLUE_CRYSTAL = (30, 144, 255)
    TEXT_COLOR = (0, 0, 0)
    UI_BG = (50, 50, 50, 180)

    gravity = 0.5
    scroll_threshold = 200
    game_over = False
    game_won = False
    level_complete = False

    font = pygame.font.SysFont('Arial', 24)
    title_font = pygame.font.SysFont('Arial', 48, bold=True)

    # Load power-up images
    star_img = pygame.image.load("assets/star.png").convert_alpha()
    star_img = pygame.transform.scale(star_img, (30, 30))
    
    red_crystal_img = pygame.image.load("assets/red_crystal.png").convert_alpha()
    red_crystal_img = pygame.transform.scale(red_crystal_img, (30, 30))
    
    blue_crystal_img = pygame.image.load("assets/blue_crystal.png").convert_alpha()
    blue_crystal_img = pygame.transform.scale(blue_crystal_img, (30, 30))

    # SpriteSheet class for enemy animation
    class SpriteSheet():
        def __init__(self, image):
            self.sheet = image

        def get_image(self, frame, width, height, scale, colour):
            image = pygame.Surface((width, height)).convert_alpha()
            image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
            image = pygame.transform.scale(image, (width * scale, height * scale))
            image.set_colorkey(colour)
            return image

    # Load enemy sprite sheet
    enemy_sheet_img = pygame.image.load('doux.png').convert_alpha()
    enemy_sprite_sheet = SpriteSheet(enemy_sheet_img)
    
    # Extract enemy frames
    enemy_frames = [
        enemy_sprite_sheet.get_image(0, 24, 24, 1.25, BLACK),
        enemy_sprite_sheet.get_image(1, 24, 24, 1.25, BLACK),
        enemy_sprite_sheet.get_image(2, 24, 24, 1.25, BLACK),
        enemy_sprite_sheet.get_image(3, 24, 24, 1.25, BLACK)
    ]

    class Player:
        def __init__(self, x, y):
            self.reset(x, y)

        def reset(self, x, y):
            self.x = x
            self.y = y
            self.vel_y = 0
            self.jump_power = -12
            self.speed = 5
            self.width = 30
            self.height = 40
            self.direction = 1  # 1 for right, -1 for left
            self.invincible = 0
            self.shooting_power = False
            self.lives = 3
            self.projectiles = []
            self.animation_counter = 0
            self.jumping = False

        def update(self, platforms, enemies, powerups, screen_scroll):
            dx = 0
            dy = 0

            # Process keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx = -self.speed
                self.direction = -1
                self.animation_counter += 1
            if key[pygame.K_RIGHT]:
                dx = self.speed
                self.direction = 1
                self.animation_counter += 1
            if key[pygame.K_SPACE] and not self.jumping:
                self.vel_y = self.jump_power
                self.jumping = True
            if key[pygame.K_z] and self.shooting_power:
                self.shoot()

            # Apply gravity
            self.vel_y += gravity
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Check for collisions with platforms
            for platform in platforms:
                # Check for collision in x direction
                if platform.rect.colliderect(self.x + dx, self.y, self.width, self.height):
                    dx = 0

                # Check for collision in y direction
                if platform.rect.colliderect(self.x, self.y + dy, self.width, self.height):
                    # Check if jumping (below platform)
                    if self.vel_y < 0:
                        dy = platform.rect.bottom - self.y
                        self.vel_y = 0
                    # Check if falling (above platform)
                    elif self.vel_y >= 0:
                        dy = platform.rect.top - self.y - self.height
                        self.vel_y = 0
                        self.jumping = False

            # Check for collisions with enemies
            for enemy in enemies:
                if enemy.rect.colliderect(self.x, self.y, self.width, self.height) and self.invincible <= 0:
                    self.lives -= 1
                    self.invincible = 60  # 2 seconds of invincibility
                    if self.lives <= 0:
                        return True  # Game over

            # Check for collisions with powerups
            for powerup in powerups[:]:
                if powerup.rect.colliderect(self.x, self.y, self.width, self.height):
                    if powerup.type == "star":
                        self.invincible = 180  # 6 seconds of invincibility
                    elif powerup.type == "red_crystal":
                        self.shooting_power = True
                    elif powerup.type == "blue_crystal":
                        self.lives += 1
                    powerups.remove(powerup)

            # Update position
            self.x += dx
            self.y += dy

            # Update projectiles
            for proj in self.projectiles[:]:
                proj[0] += proj[2] * 7
                if proj[0] < 0 or proj[0] > SCREEN_WIDTH:
                    self.projectiles.remove(proj)

            # Update invincibility timer
            if self.invincible > 0:
                self.invincible -= 1

            # Prevent player from going off screen
            if self.x < 0:
                self.x = 0
            if self.x > SCREEN_WIDTH - self.width:
                self.x = SCREEN_WIDTH - self.width

            return False  # Game not over

        def shoot(self):
            if len(self.projectiles) < 3:  # Limit number of projectiles
                self.projectiles.append([self.x + self.width // 2, self.y + self.height // 2, self.direction])

        def draw(self, screen):
            # Draw projectiles
            for proj in self.projectiles:
                pygame.draw.circle(screen, (255, 0, 0), (int(proj[0]), int(proj[1])), 5)

            # Draw player (cat)
            if self.invincible > 0 and self.invincible % 6 < 3:  # Blinking effect when invincible
                return

            # Draw cat body
            pygame.draw.rect(screen, CAT_COLOR, (self.x, self.y, self.width, self.height), border_radius=10)

            # Draw cat ears
            pygame.draw.polygon(screen, CAT_COLOR,
                                [(self.x, self.y + 10), (self.x - 5, self.y), (self.x + 10, self.y + 5)])
            pygame.draw.polygon(screen, CAT_COLOR,
                                [(self.x + self.width, self.y + 10), (self.x + self.width + 5, self.y),
                                 (self.x + self.width - 10, self.y + 5)])

            # Draw cat eyes
            eye_offset = 5 if self.direction == 1 else -5
            pygame.draw.circle(screen, (0, 0, 0),
                               (int(self.x + self.width // 2 - 5 + eye_offset // 2), int(self.y + 15)), 4)
            pygame.draw.circle(screen, (0, 0, 0),
                               (int(self.x + self.width // 2 + 5 + eye_offset // 2), int(self.y + 15)), 4)

            # Draw cat nose
            pygame.draw.polygon(screen, (255, 150, 150), [(self.x + self.width // 2, self.y + 25),
                                                          (self.x + self.width // 2 - 4, self.y + 30),
                                                          (self.x + self.width // 2 + 4, self.y + 30)])

            # Draw cat tail
            tail_points = [
                (self.x + self.width, self.y + self.height - 10),
                (self.x + self.width + 15, self.y + self.height - 20),
                (self.x + self.width + 20, self.y + self.height - 10),
                (self.x + self.width + 10, self.y + self.height - 5),
                (self.x + self.width, self.y + self.height)
            ]
            pygame.draw.polygon(screen, CAT_COLOR, tail_points)

            # Draw legs
            leg_y = self.y + self.height - 5
            pygame.draw.rect(screen, CAT_COLOR, (self.x + 5, leg_y, 5, 10))
            pygame.draw.rect(screen, CAT_COLOR, (self.x + self.width - 10, leg_y, 5, 10))

            # Animation effect
            if self.animation_counter > 0:
                leg_offset = math.sin(self.animation_counter * 0.5) * 3
                pygame.draw.rect(screen, CAT_COLOR, (self.x + 15, leg_y + leg_offset, 5, 10))
                pygame.draw.rect(screen, CAT_COLOR, (self.x + self.width - 20, leg_y - leg_offset, 5, 10))
            else:
                pygame.draw.rect(screen, CAT_COLOR, (self.x + 15, leg_y, 5, 10))
                pygame.draw.rect(screen, CAT_COLOR, (self.x + self.width - 20, leg_y, 5, 10))

    class Platform:
        def __init__(self, x, y, width, height):
            self.rect = pygame.Rect(x, y, width, height)

        def draw(self, screen, scroll):
            pygame.draw.rect(screen, PLATFORM_COLOR,
                             (self.rect.x - scroll, self.rect.y, self.rect.width, self.rect.height))
            # Draw grass on top
            pygame.draw.rect(screen, GROUND_COLOR, (self.rect.x - scroll, self.rect.y, self.rect.width, 5))

    class Enemy:
        def __init__(self, x, y, width, height):
            self.rect = pygame.Rect(x, y, width, height)
            self.direction = 1
            self.move_counter = 0
            self.animation_counter = 0
            self.current_frame = 0
            self.animation_speed = 0.2  # Speed of animation

        def update(self, platforms, player_projectiles, screen_scroll):
            # Move enemy
            self.rect.x += self.direction
            self.move_counter += 1
            self.animation_counter += 1

            # Update animation frame
            self.current_frame += self.animation_speed
            if self.current_frame >= len(enemy_frames):
                self.current_frame = 0

            # Change direction if moved too far or hit a wall
            if self.move_counter > 50:
                self.direction *= -1
                self.move_counter = 0

            # Check for collisions with projectiles
            for proj in player_projectiles[:]:
                if self.rect.collidepoint(proj[0], proj[1]):
                    player_projectiles.remove(proj)
                    return True  # Enemy is dead
            return False  # Enemy still alive

        def draw(self, screen, scroll):
            # Get current frame
            frame = enemy_frames[int(self.current_frame)]
            
            # Flip image based on direction
            if self.direction < 0:
                frame = pygame.transform.flip(frame, True, False)
            
            # Draw enemy
            screen.blit(frame, (self.rect.x - scroll - 5, self.rect.y - 5))  # Adjust position for sprite

    class Powerup:
        def __init__(self, x, y, type):
            self.rect = pygame.Rect(x, y, 30, 30)  # Increased size for images
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
            # Draw flag pole
            pygame.draw.rect(screen, (200, 200, 200), (self.rect.x - scroll + 14, self.rect.y, 2, 60))

            # Draw flag
            flag_offset = math.sin(self.animation_counter * 0.1) * 3
            pygame.draw.polygon(screen, (255, 50, 50), [
                (self.rect.x - scroll + 16, self.rect.y + 20 + flag_offset),
                (self.rect.x - scroll + 16, self.rect.y + 40 + flag_offset),
                (self.rect.x - scroll + 36, self.rect.y + 30 + flag_offset)
            ])

    # Create game objects
    def create_level():
        platforms = [
            Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),  # Ground
            Platform(100, 500, 200, 20),
            Platform(400, 450, 150, 20),
            Platform(200, 380, 100, 20),
            Platform(500, 350, 150, 20),
            Platform(100, 300, 200, 20),
            Platform(400, 250, 150, 20),
            Platform(200, 180, 100, 20),
            Platform(500, 150, 150, 20),
            Platform(300, 100, 100, 20)
        ]

        enemies = [
            Enemy(300, SCREEN_HEIGHT - 80, 30, 30),
            Enemy(500, 410, 30, 30),
            Enemy(250, 330, 30, 30),
            Enemy(550, 300, 30, 30),
            Enemy(150, 250, 30, 30),
            Enemy(450, 200, 30, 30)
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

        player = Player(50, SCREEN_HEIGHT - 100)

        return platforms, enemies, powerups, goal, player

    # Create level
    platforms, enemies, powerups, goal, player = create_level()

    # Game loop
    clock = pygame.time.Clock()
    scroll = 0

    while True:
        clock.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game_over or game_won):
                    # Reset game
                    platforms, enemies, powerups, goal, player = create_level()
                    game_over = False
                    game_won = False
                    level_complete = False
                    scroll = 0

        if not game_over and not game_won:
            # Update game objects
            game_over = player.update(platforms, enemies, powerups, scroll)

            # Update enemies and check for collisions with projectiles
            for enemy in enemies[:]:
                if enemy.update(platforms, player.projectiles, scroll):
                    enemies.remove(enemy)

            # Update powerups
            for powerup in powerups:
                powerup.update()

            # Update goal
            goal.update()

            # Check if player reached the goal
            if player.x + player.width > goal.rect.x and player.x < goal.rect.x + goal.rect.width and \
                    player.y + player.height > goal.rect.y and player.y < goal.rect.y + goal.rect.height:
                game_won = True

            # Update scroll based on player position
            if player.x > SCREEN_WIDTH - scroll_threshold:
                scroll += player.x - (SCREEN_WIDTH - scroll_threshold)
            elif player.x < scroll_threshold:
                scroll -= scroll_threshold - player.x

            scroll = max(0, min(scroll, SCREEN_WIDTH * 2 - SCREEN_WIDTH))

        screen.fill(BACKGROUND)

        for i in range(5):
            cloud_x = (i * 200 + scroll // 3) % (SCREEN_WIDTH + 200) - 100
            pygame.draw.circle(screen, (255, 255, 255), (cloud_x, 80), 30)
            pygame.draw.circle(screen, (255, 255, 255), (cloud_x + 20, 70), 30)
            pygame.draw.circle(screen, (255, 255, 255), (cloud_x + 40, 80), 30)
            pygame.draw.circle(screen, (255, 255, 255), (cloud_x + 20, 90), 30)

        for platform in platforms:
            platform.draw(screen, scroll)

        for enemy in enemies:
            enemy.draw(screen, scroll)

        for powerup in powerups:
            powerup.draw(screen, scroll)

        goal.draw(screen, scroll)
        player.draw(screen)
        pygame.draw.rect(screen, UI_BG, (10, 10, 200, 90), border_radius=10)
        for i in range(player.lives):
            pygame.draw.circle(screen, (255, 50, 50), (30 + i * 30, 35), 10)

        if player.invincible > 0:
            pygame.draw.circle(screen, STAR_COLOR, (30, 70), 8)
        if player.shooting_power:
            pygame.draw.circle(screen, RED_CRYSTAL, (60, 70), 8)

        lives_text = font.render(f'Lives: {player.lives}', True, TEXT_COLOR)
        screen.blit(lives_text, (70, 25))

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
        screen.fill((100, 100, 100))
        loading_text = font.render("Game loading...", True, WHITE)
        screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT // 2 - loading_text.get_height() // 2))
        if pygame.time.get_ticks() - loading_start_time > LOADING_DURATION:
            current_state = PLAYING

    elif current_state == PLAYING:
        run_level()
        restart_game()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
