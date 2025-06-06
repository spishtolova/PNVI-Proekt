import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catz")

# Fonts
font = pygame.font.SysFont("Arial", 60)
small_font = pygame.font.SysFont("Arial", 20)

# Load and scale menu background image
menu_img = pygame.image.load("assets/FreeDemo.png").convert_alpha()
menu_img = pygame.transform.scale(menu_img, (300, 300))
menu_rect = menu_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

# Load background image for controls and game
forest_bg = pygame.image.load("assets/forest.jpg").convert()
forest_bg = pygame.transform.scale(forest_bg, (WIDTH, HEIGHT))

# Correctly aligned clickable button areas based on the uploaded image layout
play_button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 - 65, 120, 40)  # Play button area
settings_button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 - 15, 120, 40)  # Settings button area
quit_button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 35, 120, 40)  # Quit button area

# Game states
MAIN_MENU = "main_menu"
GAME_LOADING = "game_loading"
SETTINGS = "settings"
current_state = MAIN_MENU


def play_game():
    global current_state
    current_state = GAME_LOADING


def quit_game():
    pygame.quit()
    sys.exit()


def show_settings():
    global current_state
    current_state = SETTINGS


def restart_game():
    global current_state
    current_state = MAIN_MENU


clock = pygame.time.Clock()
running = True

# For loading screen timer
loading_start_time = None
LOADING_DURATION = 15000  # milliseconds


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

    # Draw based on state
    if current_state == MAIN_MENU:
        screen.blit(forest_bg, (0, 0))
        title = font.render("Catz", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        screen.blit(menu_img, menu_rect)

    elif current_state == SETTINGS:
        screen.blit(forest_bg, (0, 0))

        # Draw rounded rectangle for controls
        controls_rect = pygame.Rect(WIDTH // 2 - 320, HEIGHT // 2 - 240, 640, 480)
        pygame.draw.rect(screen, WHITE, controls_rect, border_radius=20)
        pygame.draw.rect(screen, DARK_GRAY, controls_rect, width=2, border_radius=20)

        # Title with more margin
        controls_title = font.render("Controls", True, BLACK)
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

        # Calculate total height of all text lines
        total_text_height = len(controls_text) * 35
        # Calculate starting y position to center the text block vertically with extra margin from title
        start_y = HEIGHT // 2 - total_text_height // 2 + 30  # Added 30 pixels of margin

        for i, line in enumerate(controls_text):
            line_surface = small_font.render(line, True, BLACK)
            screen.blit(line_surface, (WIDTH // 2 - line_surface.get_width() // 2, start_y + i * 35))

    elif current_state == GAME_LOADING:
        if loading_start_time is None:
            loading_start_time = pygame.time.get_ticks()

        screen.fill((100, 100, 100))  # Grey background
        loading_text = font.render("Game loading...", True, WHITE)
        screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT // 2 - loading_text.get_height() // 2))

        # Check if loading time passed
        if pygame.time.get_ticks() - loading_start_time > LOADING_DURATION:
            loading_start_time = None
            restart_game()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
