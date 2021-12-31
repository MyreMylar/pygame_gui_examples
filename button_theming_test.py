import pygame
import pygame_gui

# Rough current performance measure - Button creation time taken: 0.08 seconds.
# (54 x rounded rectangles)

pygame.init()


pygame.display.set_caption('Button Theming Test')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/button_theming_test_theme.json')
clock = pygame.time.Clock()

background = pygame.Surface((800, 600))
background.fill(manager.get_theme().get_colour('dark_bg'))

load_time_1 = clock.tick()

button_row_width = 100
button_row_height = 40
spacing = 20
for j in range(1, 10):
    for i in range(1, 7):
        position = (i * spacing + ((i - 1) * button_row_width),
                    (j * spacing + ((j - 1) * button_row_height)))
        pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position,
                                                               (button_row_width,
                                                                button_row_height)),
                                     text=str(i) + ',' + str(j),
                                     manager=manager,
                                     object_id='#' + str(i) + ',' + str(j))

load_time_2 = clock.tick()
print('Button creation time taken:', load_time_2/1000.0, 'seconds.')

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
