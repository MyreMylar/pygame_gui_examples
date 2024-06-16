import pygame
import pygame_gui

import pygame_gui.data

from pygame.color import Color
from pygame.surface import Surface

from pygame_gui.elements.ui_text_box import UITextBox

"""
A test bed to tinker with future text features.
"""


def test_app():
    pygame.init()

    display_surface = pygame.display.set_mode((800, 600))

    ui_manager = pygame_gui.UIManager((800, 600), 'data/themes/theme_1.json')

    background = Surface((800, 600), depth=32)
    background.fill(Color("#606060"))

    text_box = UITextBox(
        html_text="<body><font color=#E0E080>hey hey hey "
                  "what are the <a href=haps>haps</a> my "
                  "<u>brand new friend?</u> These are the "
                  "days of our <i>disco tent. </i>"
                  "<shadow size=2 offset=0,0 color=#306090><font color=#E0F0FF>Why the "
                  "long night</font></shadow> of <font color=regular_text>absolution</font>, "
                  "shall <b>becometh </b>the man. Lest "
                  "forth "
                  "betwixt moon under one nation "
                  "before and beyond opus grande "
                  "just in time for the last time "
                  "three nine nine. Toight."
                  "<br><br>"
                  "hella toight.</font>",
        relative_rect=pygame.Rect(100, 100, 400, 200),
        manager=ui_manager)

    is_running = True
    clock = pygame.time.Clock()

    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            ui_manager.process_events(event)

        display_surface.blit(background, (0, 0))

        ui_manager.update(0.01)
        ui_manager.draw_ui(window_surface=display_surface)

        pygame.display.update()


if __name__ == "__main__":
    test_app()
