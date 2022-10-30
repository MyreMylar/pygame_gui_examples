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
        container=notepad_window)

text_output_box = UITextBox(
        relative_rect=pygame.Rect((0, 0), output_window.get_container().get_size()),
        html_text="",
        container=output_window)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == UI_TEXT_ENTRY_CHANGED and event.ui_element == text_entry_box:
            text_output_box.set_text(event.text)

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
