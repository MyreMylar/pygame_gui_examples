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
    background.fill(Color("#FFFFFF"))

    text_box = UITextBox(
        html_text="<body><font color=#E0E080>hey hey hey "
                  "what are the <a href=haps>haps</a> my "
                  "<u>brand new friend?</u> These are the "
                  "days of our <i>disco tent. </i>"
                  "<shadow size=1 offset=0,0 color=#306090><font color=#E0F0FF><b>Why the "
                  "long night</b></font></shadow> of <font color=regular_text>absolution</font>, "
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

    text_box.scroll_bar.has_moved_recently = True
    text_box.update(5.0)

    is_running = True
    row_key_pos = 13
    typing_row = len(text_box.text_box_layout.layout_rows) - 1

    clock = pygame.time.Clock()

    cursor_toggle = 0
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                text_block_full_height = text_box.text_box_layout.layout_rect.height
                height_adjustment = (text_box.scroll_bar.start_percentage *
                                     text_block_full_height)
                base_x = int(text_box.rect[0] + text_box.padding[0] + text_box.border_width +
                             text_box.shadow_width + text_box.rounded_corner_offset)
                base_y = int(text_box.rect[1] + text_box.padding[1] + text_box.border_width +
                             text_box.shadow_width + text_box.rounded_corner_offset - height_adjustment)
                text_box.text_box_layout.set_cursor_from_click_pos((event.pos[0] - base_x,
                                                                         event.pos[1] - base_y))

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                text_box.text_box_layout.set_text_selection(48, 245)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                text_box.text_box_layout.set_text_selection(56, 220)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                text_box.text_box_layout.set_text_selection(0, 5)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                text_box.text_box_layout.set_text_selection(0, 4)

            ui_manager.process_events(event)

        cursor_toggle += time_delta
        if cursor_toggle >= 0.4:
            cursor_toggle = 0.0
            text_box.text_box_layout.toggle_cursor()
            text_box.redraw_from_text_block()

        display_surface.blit(background, (0, 0))

        ui_manager.update(0.01)
        ui_manager.draw_ui(window_surface=display_surface)

        pygame.display.update()


if __name__ == "__main__":
    test_app()
