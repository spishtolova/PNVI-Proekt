import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cats Platformer")

# Colors
BACKGROUND = (135, 206, 235)  # Sky blue
GROUND_COLOR = (34, 139, 34)  # Forest green
PLATFORM_COLOR = (139, 69, 19)  # Saddle brown
CAT_COLOR = (255, 165, 0)  # Orange
ENEMY_COLOR = (220, 20, 60)  # Crimson red
STAR_COLOR = (255, 255, 0)  # Yellow
RED_CRYSTAL = (220, 20, 60)  # Red
BLUE_CRYSTAL = (30, 144, 255)  # Dodger blue
TEXT_COLOR = (0, 0, 0)  # Black
UI_BG = (50, 50, 50, 180)  # Semi-transparent dark gray

# Game variables
gravity = 0.5
scroll_threshold = 200
game_over = False
game_won = False
level_complete = False

# Font
font = pygame.font.SysFont('Arial', 24)
title_font = pygame.font.SysFont('Arial', 48, bold=True)

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
        pygame.draw.polygon(screen, CAT_COLOR, [(self.x, self.y + 10), (self.x - 5, self.y), (self.x + 10, self.y + 5)])
        pygame.draw.polygon(screen, CAT_COLOR, [(self.x + self.width, self.y + 10), (self.x + self.width + 5, self.y), (self.x + self.width - 10, self.y + 5)])
        
        # Draw cat eyes
        eye_offset = 5 if self.direction == 1 else -5
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + self.width//2 - 5 + eye_offset//2), int(self.y + 15)), 4)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + self.width//2 + 5 + eye_offset//2), int(self.y + 15)), 4)
        
        # Draw cat nose
        pygame.draw.polygon(screen, (255, 150, 150), [(self.x + self.width//2, self.y + 25), 
                                                     (self.x + self.width//2 - 4, self.y + 30), 
                                                     (self.x + self.width//2 + 4, self.y + 30)])
        
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
        pygame.draw.rect(screen, PLATFORM_COLOR, (self.rect.x - scroll, self.rect.y, self.rect.width, self.rect.height))
        # Draw grass on top
        pygame.draw.rect(screen, GROUND_COLOR, (self.rect.x - scroll, self.rect.y, self.rect.width, 5))

class Enemy:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = 1
        self.move_counter = 0
        self.animation_counter = 0
        
    def update(self, platforms, player_projectiles, screen_scroll):
        # Move enemy
        self.rect.x += self.direction
        self.move_counter += 1
        self.animation_counter += 1
        
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
        # Draw enemy body
        pygame.draw.rect(screen, ENEMY_COLOR, (self.rect.x - scroll, self.rect.y, self.rect.width, self.rect.height), border_radius=8)
        
        # Draw enemy eyes
        eye_offset = 5 if self.direction == 1 else -5
        pygame.draw.circle(screen, (0, 0, 0), (int(self.rect.x - scroll + self.rect.width//2 - 5 + eye_offset//2), int(self.rect.y + 15)), 4)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.rect.x - scroll + self.rect.width//2 + 5 + eye_offset//2), int(self.rect.y + 15)), 4)
        
        # Draw enemy spikes
        for i in range(3):
            spike_x = self.rect.x - scroll + i * (self.rect.width // 2) + 10
            pygame.draw.polygon(screen, (100, 0, 0), [
                (spike_x, self.rect.y - 5),
                (spike_x - 5, self.rect.y + 10),
                (spike_x + 5, self.rect.y + 10)
            ])
        
        # Draw enemy legs (animated)
        leg_y = self.rect.y + self.rect.height - 5
        leg_offset = math.sin(self.animation_counter * 0.2) * 5
        pygame.draw.rect(screen, ENEMY_COLOR, (self.rect.x - scroll + 5, leg_y + leg_offset, 5, 10))
        pygame.draw.rect(screen, ENEMY_COLOR, (self.rect.x - scroll + self.rect.width - 10, leg_y - leg_offset, 5, 10))

class Powerup:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.type = type
        self.animation_counter = 0
        
    def update(self):
        self.animation_counter += 1
        
    def draw(self, screen, scroll):
        y_offset = math.sin(self.animation_counter * 0.1) * 5
        
        if self.type == "star":
            # Draw star
            points = []
            for i in range(5):
                # Outer points
                angle = math.pi/2 + i * 2*math.pi/5
                points.append((self.rect.x - scroll + 10 + 10 * math.cos(angle), 
                             self.rect.y + 10 + y_offset + 10 * math.sin(angle)))
                # Inner points
                angle += math.pi/5
                points.append((self.rect.x - scroll + 10 + 4 * math.cos(angle), 
                             self.rect.y + 10 + y_offset + 4 * math.sin(angle)))
            pygame.draw.polygon(screen, STAR_COLOR, points)
            
        elif self.type == "red_crystal":
            # Draw red crystal
            pygame.draw.polygon(screen, RED_CRYSTAL, [
                (self.rect.x - scroll + 10, self.rect.y + y_offset),
                (self.rect.x - scroll + 3, self.rect.y + 10 + y_offset),
                (self.rect.x - scroll + 10, self.rect.y + 20 + y_offset),
                (self.rect.x - scroll + 17, self.rect.y + 10 + y_offset)
            ])
            
        elif self.type == "blue_crystal":
            # Draw blue crystal
            pygame.draw.polygon(screen, BLUE_CRYSTAL, [
                (self.rect.x - scroll + 10, self.rect.y + y_offset),
                (self.rect.x - scroll, self.rect.y + 10 + y_offset),
                (self.rect.x - scroll + 10, self.rect.y + 20 + y_offset),
                (self.rect.x - scroll + 20, self.rect.y + 10 + y_offset)
            ])

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
            
        # Ensure scroll doesn't go beyond level boundaries
        scroll = max(0, min(scroll, SCREEN_WIDTH * 2 - SCREEN_WIDTH))
    
    # Draw background
    screen.fill(BACKGROUND)
    
    # Draw clouds
    for i in range(5):
        cloud_x = (i * 200 + scroll // 3) % (SCREEN_WIDTH + 200) - 100
        pygame.draw.circle(screen, (255, 255, 255), (cloud_x, 80), 30)
        pygame.draw.circle(screen, (255, 255, 255), (cloud_x + 20, 70), 30)
        pygame.draw.circle(screen, (255, 255, 255), (cloud_x + 40, 80), 30)
        pygame.draw.circle(screen, (255, 255, 255), (cloud_x + 20, 90), 30)
    
    # Draw game objects
    for platform in platforms:
        platform.draw(screen, scroll)
        
    for enemy in enemies:
        enemy.draw(screen, scroll)
        
    for powerup in powerups:
        powerup.draw(screen, scroll)
        
    goal.draw(screen, scroll)
    player.draw(screen)
    
    # Draw UI
    pygame.draw.rect(screen, UI_BG, (10, 10, 200, 90), border_radius=10)
    
    # Draw lives
    for i in range(player.lives):
        pygame.draw.circle(screen, (255, 50, 50), (30 + i * 30, 35), 10)
    
    # Draw powerup indicators
    if player.invincible > 0:
        pygame.draw.circle(screen, STAR_COLOR, (30, 70), 8)
    if player.shooting_power:
        pygame.draw.circle(screen, RED_CRYSTAL, (60, 70), 8)
    
    # Draw text
    lives_text = font.render(f'Lives: {player.lives}', True, TEXT_COLOR)
    screen.blit(lives_text, (70, 25))
    
    # Draw game over or win message
    if game_over:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        game_over_text = title_font.render('GAME OVER', True, (255, 50, 50))
        restart_text = font.render('Press R to Restart', True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
        
    elif game_won:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 100, 0, 150))
        screen.blit(overlay, (0, 0))
        
        win_text = title_font.render('LEVEL COMPLETE!', True, (50, 255, 50))
        restart_text = font.render('Press R to Play Again', True, (255, 255, 255))
        screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
    
    # Draw instructions
    instructions = [
        "Controls:",
        "Arrow Keys - Move",
        "SPACE - Jump",
        "Z - Shoot (with red crystal)"
    ]
    
    pygame.draw.rect(screen, UI_BG, (SCREEN_WIDTH - 210, 10, 200, 130), border_radius=10)
    for i, line in enumerate(instructions):
        text = font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH - 200, 20 + i * 25))
    
    # Draw powerup info
    powerup_info = [
        "Powerups:",
        "★ - Invincibility (5s)",
        "♦ - Shooting power",
        "🔷 - Extra life"
    ]
    
    pygame.draw.rect(screen, UI_BG, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 150, 200, 140), border_radius=10)
    for i, line in enumerate(powerup_info):
        text = font.render(line, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 140 + i * 25))
    
    pygame.display.update()
