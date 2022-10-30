import pygame

from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton


pygame.init()


pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))
manager = UIManager((800, 600), 'data/themes/quick_theme.json')

background = pygame.Surface((800, 600))
background.fill(manager.ui_theme.get_colour('dark_bg'))


hello_button = UIButton((350, 280), 'Hello')

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print('Hello World!')
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
