import pygame
import pygame_gui


"""
Useful example for building documentation images
"""


class TestSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.health_capacity = 100
        self.current_health = 75
        self.rect = pygame.Rect(150, 150, 50, 75)


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/documentation_theme.json')

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#fcfcfc'))

# pygame_gui.elements.UIDropDownMenu(options_list=['Easy', 'Medium', 'Hard', 'Very Hard'],
#                                    starting_option='Medium',
#                                    relative_rect=pygame.Rect((350, 280), (250, 50)),
#                                    manager=manager)

# pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((350, 280), (250, 40)),
#                                        start_value=50,
#                                        value_range=(0, 100),
#                                        manager=manager)

# pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 280), (350, 60)),
#                             text='label text',
#                             manager=manager)

# pygame_gui.elements.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((350, 280), (250, 40)),
#                                            manager=manager)

# pygame_gui.elements.UITextBox(html_text="This is normal text. <a href='none'>This a link</a>",
#                               relative_rect=pygame.Rect((150, 150), (150, 100)),
#                               manager=manager)

# pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 280), (250, 40)),
#                                     manager=manager)

# pygame_gui.elements.UIVerticalScrollBar(relative_rect=pygame.Rect((280, 150), (30, 250)),
#                                         visible_percentage=0.8,
#                                         manager=manager)

# test_sprite = TestSprite()
# pygame_gui.elements.UIWorldSpaceHealthBar(relative_rect=pygame.Rect((350, 280), (150, 35)),
#                                           sprite_to_monitor=test_sprite,
#                                           manager=manager)

pygame_gui.windows.UIColourPickerDialog(rect=pygame.Rect(100, 100, 390, 390),
                                        manager=manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
