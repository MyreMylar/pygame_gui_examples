import random
import math

import pygame
import pygame_gui

GOLDEN_RATIO = (math.sqrt(5) - 1) / 2


def add_random_rectangle_to_cache():
    width = random.randint(20, 200)
    height = random.randint(20, 200)
    surface = pygame.Surface((width, height))
    color = pygame.Color("#000000")
    color.hsla = 360 * ((width * GOLDEN_RATIO) % 1), 50, 70, 100
    color.a = 128
    surface.fill(color)

    manager.ui_theme.shape_cache.add_surface_to_cache(surface, str(color.hsla))


pygame.init()


pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((1024, 1024))
manager = pygame_gui.UIManager((1024, 1024), 'data/themes/quick_theme.json')

background = pygame.Surface((1024, 1024))
background.fill(manager.get_theme().get_colour(None, None, 'dark_bg'))

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                add_random_rectangle_to_cache()

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    window_surface.blit(manager.ui_theme.shape_cache.cache_surfaces[0], (0, 0))
    for rectangle in manager.ui_theme.shape_cache.free_space_rectangles:
        pygame.draw.rect(window_surface, pygame.Color('#A00000'), rectangle, 2)

    pygame.display.update()
