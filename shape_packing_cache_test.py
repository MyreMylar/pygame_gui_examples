import random
import math

import pygame
import pygame_gui

GOLDEN_RATIO = (math.sqrt(5) - 1) / 2


def add_random_rectangle_to_cache(added_surfaces_list):
    width = random.randint(20, 200)
    height = random.randint(20, 200)
    surface = pygame.Surface((width, height))
    color = pygame.Color("#000000")
    color.hsla = 360 * ((width * GOLDEN_RATIO) % 1), 50, 70, 100
    color.a = 128
    surface.fill(color)

    added_surfaces_list.append(str(color.hsla))
    manager.ui_theme.shape_cache.add_surface_to_cache(surface, str(color.hsla))


def remove_use_from_cache_surface(surf_id):
    added_surfaces.remove(surf_id)
    manager.ui_theme.shape_cache.remove_user_from_cache_item(surf_id)


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((1024, 1024))
manager = pygame_gui.UIManager((1024, 1024), 'data/themes/quick_theme.json')

background = pygame.Surface((1024, 1024))
background.fill(manager.get_theme().get_colour('dark_bg'))

clock = pygame.time.Clock()
is_running = True
current_surf = 0
added_surfaces = []

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                add_random_rectangle_to_cache(added_surfaces)
            if event.key == pygame.K_BACKSPACE:
                if len(added_surfaces) > 0:
                    remove_use_from_cache_surface(random.choice(added_surfaces))
            if event.key == pygame.K_RIGHT:
                if current_surf < len(manager.ui_theme.shape_cache.cache_surfaces) - 1:
                    current_surf += 1
            if event.key == pygame.K_LEFT:
                if current_surf > 0:
                    current_surf -= 1

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    cache_surface = manager.ui_theme.shape_cache.cache_surfaces[current_surf]
    window_surface.blit(cache_surface['surface'],
                        (0, 0))
    for rectangle in cache_surface['free_space_rectangles']:
        pygame.draw.rect(window_surface, pygame.Color('#A00000'), rectangle, 2)

    pygame.display.update()
