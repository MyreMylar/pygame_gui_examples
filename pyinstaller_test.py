import os
import sys
import pygame
import pygame_gui


"""
TO build an executable run:
   pip install pyinstaller

Then:
   pyinstaller pyinstaller_specs/pyinstaller_build.spec
   
Or:
   pyinstaller pyinstaller_specs/pyinstaller_onefile_build.spec

in the terminal.
"""


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller's 'onefile' mode """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), resource_path('data/themes/pyinstaller_theme.json'))

background = pygame.Surface((800, 600))
background.fill(manager.ui_theme.get_colour('dark_bg'))

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 280), (150, 40)),
                                            text='Hello',
                                            manager=manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == hello_button:
            print('Hello World!')

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
