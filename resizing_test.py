import pygame
import pygame_gui
import random


class HealthySprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.health_capacity = 100
        self.current_health = 75
        self.rect = pygame.Rect(150, 150, 50, 75)


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/quick_theme.json')

background = pygame.Surface((800, 600))
background.fill(manager.ui_theme.get_colour('dark_bg'))

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 280), (150, 40)),
                                            text='Hello',
                                            manager=manager)

drop_down = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(200, 100, 200, 30),
                                               manager=manager, options_list=['Dan', 'Trev', 'Bob'],
                                               starting_option='Dan')

label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(50, 50, 100, 20),
                                    text='A Label', manager=manager)

slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(40, 540, 150, 40),
                                                start_value=50,
                                                value_range=(0, 200),
                                                manager=manager)

scroll_bar = pygame_gui.elements.UIVerticalScrollBar(relative_rect=pygame.Rect(80, 100, 30, 200),
                                                     visible_percentage=0.25,
                                                     manager=manager)

healthy_sprite = HealthySprite()

ss_health_bar = pygame_gui.elements.UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 500,
                                                                                     150, 30),
                                                           sprite_to_monitor=healthy_sprite,
                                                           manager=manager)

# UITextBox(html_text=text, relative_rect=rect, manager=manager, wrap_to_height=True,
# layer_starting_height=100, object_id="screen_message")
text_box = pygame_gui.elements.UITextBox(html_text='la la LA LA LAL LAL ALALA'
                                                   'LLALAALALA ALALA ALAL ALA'
                                                   'LAALA ALALA ALALA AAaal aa'
                                                   'ALALAa laalal alalal alala'
                                                   'alalalala alalalalalal alal'
                                                   'alalalala <a href=none>alala</a> '
                                                   'alalala ala'
                                                   'alalalalal lalal alalalal al'
                                                   'al alalalal lfed alal alal alal al'
                                                   'ala lalalal lasda lal a lalalal slapl'
                                                   'alalala lal la blop lal alal aferlal al',
                                         relative_rect=pygame.Rect(500, 0, 320, 10),
                                         manager=manager,
                                         wrap_to_height=True)

text_entry = pygame_gui.elements.UITextEntryLine(pygame.Rect((500, 500),
                                                             (200, -1)),
                                                 manager=manager)

ws_health_bar = pygame_gui.elements.UIWorldSpaceHealthBar(relative_rect=pygame.Rect(100, 500,
                                                                                    150, 30),
                                                          sprite_to_monitor=healthy_sprite,
                                                          manager=manager)

loaded_test_image = pygame.image.load('data/images/splat.png').convert_alpha()
test_image = pygame_gui.elements.UIImage(pygame.Rect((0, 0),
                                                     loaded_test_image.get_rect().size),
                                         loaded_test_image,
                                         manager=manager)

tool_tip = pygame_gui.elements.UITooltip(html_text='What a tip this tool is.',
                                         hover_distance=(0, 10),
                                         manager=manager)

clock = pygame.time.Clock()
is_running = True
debug_mode = False

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                hello_button.set_dimensions((random.randint(50, 200), random.randint(20, 60)))
            if event.key == pygame.K_k:
                drop_down.set_dimensions((random.randint(50, 200), random.randint(20, 60)))
            if event.key == pygame.K_l:
                label.set_dimensions((random.randint(50, 200), random.randint(20, 60)))
            if event.key == pygame.K_h:
                slider.set_dimensions((random.randint(50, 200), random.randint(20, 60)))
            if event.key == pygame.K_g:
                scroll_bar.set_dimensions((random.randint(20, 60), random.randint(50, 300)))
            if event.key == pygame.K_f:
                ss_health_bar.set_dimensions((random.randint(50, 200), random.randint(20, 60)))
            if event.key == pygame.K_s:
                random_dimensions = (random.randint(56, 300), random.randint(80, 400))
                text_box.set_dimensions(random_dimensions)
            if event.key == pygame.K_a:
                text_entry.set_dimensions((random.randint(50, 300), random.randint(20, 60)))
            if event.key == pygame.K_z:
                ws_health_bar.set_dimensions((random.randint(50, 200), random.randint(20, 60)))

            if event.key == pygame.K_x:
                test_image.set_dimensions((random.randint(32, 256), random.randint(32, 256)))

            if event.key == pygame.K_c:
                tool_tip.set_dimensions((random.randint(100, 200), random.randint(60, 200)))

            if event.key == pygame.K_d:
                debug_mode = False if debug_mode else True
                manager.set_visual_debug_mode(debug_mode)

            if event.key == pygame.K_l:
                print(text_entry.get_text())

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_element == hello_button):
            print('Hello World!')

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
