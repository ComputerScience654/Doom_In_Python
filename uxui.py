import pygame
import sys

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (255, 255, 0)  # สีไฮไลท์

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DoomPython")

# Fonts
font = pygame.font.SysFont(None, 55)

# Menu options
menu_options = ["Start Game", "Settings", "Quit"]
settings_options = ["Volume", "Resolution", "Back"]

# Load background image
background_image = pygame.image.load('resources/textures/doom1.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load icons
start_icon = pygame.image.load('resources/icons/newgame.png')
settings_icon = pygame.image.load('resources/icons/option.png')
quit_icon = pygame.image.load('resources/icons/quit.png')
title_image = pygame.image.load('resources/icons/logo.png')  # โหลดรูปชื่อเกม

# Scale icons
start_icon = pygame.transform.scale(start_icon, (200, 50))
settings_icon = pygame.transform.scale(settings_icon, (200, 50))
quit_icon = pygame.transform.scale(quit_icon, (200, 50))
title_image = pygame.transform.scale(title_image, (600, 150))  # ปรับขนาดรูปชื่อเกม

# Volume settings
volume_levels = ["Mute", "Low", "Medium", "High"]
current_volume = 2  # Default to Medium

# Resolution settings
resolutions = [(800, 600), (1280, 720), (1600, 900)]
current_resolution = 2  # Default to 1600x900

# Load music
menu_music = 'resources/sound/mainmenu.mp3'
game_music = 'resources/sound/theme1.wav'

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu(game_instance):
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)
    selected = 0
    while True:
        screen.blit(background_image, (0, 0))
        screen.blit(title_image, (SCREEN_WIDTH // 2 - title_image.get_width() // 2, SCREEN_HEIGHT // 2 - 300))  # วาดรูปชื่อเกม

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 200)
        button_2 = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 200)
        button_3 = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 350, 200, 200)

        buttons = [button_1, button_2, button_3]
        icons = [start_icon, settings_icon, quit_icon]

        for i, button in enumerate(buttons):
            screen.blit(icons[i], (button.x, button.y))
            if i == selected:
                pygame.draw.rect(screen, HIGHLIGHT, (button.x, button.y + 200, 200, 10))  # ไฮไลท์ข้างใต้

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        pygame.mixer.music.load(game_music)
                        pygame.mixer.music.play(-1)
                        game_instance.run()
                    if selected == 1:
                        settings(game_instance)
                    if selected == 2:
                        pygame.quit()
                        sys.exit()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def settings(game_instance):
    global current_volume, current_resolution, screen, background_image
    selected = 0
    while True:
        screen.blit(background_image, (0, 0))
        draw_text('Settings', font, WHITE, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 200)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, 200, 50)
        button_2 = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 200, 50)
        button_3 = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 150, 200, 50)

        buttons = [button_1, button_2, button_3]

        for i, button in enumerate(buttons):
            color = WHITE if i == selected else BLACK
            pygame.draw.rect(screen, color, button)
            draw_text(settings_options[i], font, BLACK, screen, button.x + 10, button.y + 10)

        if selected == 0:
            draw_text(f'Volume: {volume_levels[current_volume]}', font, WHITE, screen, SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 - 50)
        elif selected == 1:
            draw_text(f'Resolution: {resolutions[current_resolution][0]}x{resolutions[current_resolution][1]}', font, WHITE, screen, SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(settings_options)
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(settings_options)
                if event.key == pygame.K_RETURN:
                    if selected == 2:
                        main_menu(game_instance)
                if event.key == pygame.K_ESCAPE:
                    main_menu(game_instance)
                if event.key == pygame.K_LEFT:
                    if selected == 0:
                        current_volume = (current_volume - 1) % len(volume_levels)
                        pygame.mixer.music.set_volume(current_volume / (len(volume_levels) - 1))
                    elif selected == 1:
                        current_resolution = (current_resolution - 1) % len(resolutions)
                        screen = pygame.display.set_mode(resolutions[current_resolution])
                        background_image = pygame.transform.scale(pygame.image.load('resources/textures/doom.jpg'), resolutions[current_resolution])
                if event.key == pygame.K_RIGHT:
                    if selected == 0:
                        current_volume = (current_volume + 1) % len(volume_levels)
                        pygame.mixer.music.set_volume(current_volume / (len(volume_levels) - 1))
                    elif selected == 1:
                        current_resolution = (current_resolution + 1) % len(resolutions)
                        screen = pygame.display.set_mode(resolutions[current_resolution])
                        background_image = pygame.transform.scale(pygame.image.load('resources/textures/doom.jpg'), resolutions[current_resolution])

        pygame.display.update()

def game(game_instance):
    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        if paused:
            draw_text('Paused', font, WHITE, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
        else:
            screen.blit(background_image, (0, 0))
            game_instance.update()
            game_instance.draw()

        pygame.display.update()
