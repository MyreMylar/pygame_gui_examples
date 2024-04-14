import pygame

from pygame_gui import UIManager, UI_TEXT_ENTRY_CHANGED
from pygame_gui.elements import UIWindow, UITextEntryBox, UITextBox


pygame.init()


pygame.display.set_caption('Pygame Notepad')
window_surface = pygame.display.set_mode((800, 600))
manager = UIManager((800, 600), 'data/themes/notepad_theme.json')

background = pygame.Surface((800, 600))
background.fill(manager.ui_theme.get_colour('dark_bg'))


notepad_window = UIWindow(pygame.Rect(50, 20, 300, 400), window_display_title="Pygame Notepad")

output_window = UIWindow(pygame.Rect(400, 20, 300, 400), window_display_title="Pygame GUI Formatted Text")

# swap to editable text box
text_entry_box = UITextEntryBox(
        relative_rect=pygame.Rect((0, 0), notepad_window.get_container().get_size()),
        initial_text="",
        container=notepad_window,
        placeholder_text="Enter text here...")

text_output_box = UITextBox(
        relative_rect=pygame.Rect((0, 0), output_window.get_container().get_size()),
        html_text="",
        container=output_window)

clock = pygame.time.Clock()
is_running = True

debug_chunks = False

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == UI_TEXT_ENTRY_CHANGED and event.ui_element == text_entry_box:
            text_output_box.set_text(event.text)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            text_box_offset = (text_entry_box.padding[0] + text_entry_box.border_width +
                               text_entry_box.shadow_width +
                               text_entry_box.rounded_corner_width_offsets[0],
                               text_entry_box.padding[1] + text_entry_box.border_width +
                               text_entry_box.shadow_width +
                               text_entry_box.rounded_corner_width_offsets[0])
            for row in text_entry_box.text_box_layout.layout_rows:
                for chunk in row.items:
                    debug_rect = chunk.copy()
                    debug_rect.top += text_entry_box.rect.top + text_box_offset[1]
                    debug_rect.left += text_entry_box.rect.left + text_box_offset[0]
                    print("chunk rect: ", debug_rect)
                debug_row = row.copy()
                debug_row.top += text_entry_box.rect.top + text_box_offset[1]
                debug_row.left += text_entry_box.rect.left + text_box_offset[0]
                print("row rect: ", debug_row)

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    if debug_chunks:
        text_box_offset = (text_entry_box.padding[0] + text_entry_box.border_width +
                           text_entry_box.shadow_width +
                           text_entry_box.rounded_corner_width_offsets[0],
                           text_entry_box.padding[1] + text_entry_box.border_width +
                           text_entry_box.shadow_width +
                           text_entry_box.rounded_corner_width_offsets[0])
        for row in text_entry_box.text_box_layout.layout_rows:
            for chunk in row.items:
                debug_rect = chunk.copy()
                debug_rect.top += text_entry_box.rect.top + text_box_offset[1]
                debug_rect.left += text_entry_box.rect.left + text_box_offset[0]
                pygame.draw.rect(window_surface, pygame.Color('#FF0000'), debug_rect, 1)
            debug_row = row.copy()
            debug_row.top += text_entry_box.rect.top + text_box_offset[1]
            debug_row.left += text_entry_box.rect.left + text_box_offset[0]
            pygame.draw.rect(window_surface, pygame.Color('#0000FF'), debug_row, 1)

        layout_rect = text_entry_box.text_box_layout.layout_rect.copy()
        layout_rect.top = text_entry_box.rect.top + text_box_offset[1]
        layout_rect.left = text_entry_box.rect.left + text_box_offset[0]
        pygame.draw.rect(window_surface, pygame.Color('#00FF00'), layout_rect, 1)

    pygame.display.update()
