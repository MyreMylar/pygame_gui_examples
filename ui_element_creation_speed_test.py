import pygame
import pygame_gui


# (182 x rounded rectangles)

# in 0.42
# --------
# Button creation time taken: 0.092 seconds.
# Clear and recreation time taken: 0.088 seconds.

# in 0.55
# --------
# Button creation time taken: 0.21 seconds.
# Clear and recreation time taken: 0.229 seconds.

pygame.init()


pygame.display.set_caption('Button Theming Test')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/quick_theme.json')
clock = pygame.time.Clock()

background = pygame.Surface((800, 600))
background.fill(manager.get_theme().get_colour(None, None, 'dark_bg'))

load_time_1 = clock.tick()

test_container = pygame_gui.core.UIContainer(pygame.Rect(0, 0, 800, 600),
                                             manager=manager)

button_row_width = 50
button_row_height = 40
spacing = 10
for j in range(1, 15):
    for i in range(1, 14):
        position = (i * spacing + ((i - 1) * button_row_width),
                    (j * spacing + ((j - 1) * button_row_height)))
        pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position,
                                                               (button_row_width,
                                                                button_row_height)),
                                     text=str(i)+',' + str(j),
                                     manager=manager,
                                     container=test_container,
                                     object_id='#'+str(i) + str(j))
load_time_2 = clock.tick()
print('Button creation time taken:', load_time_2 / 1000.0, 'seconds.')
test_container.clear()

for j in range(1, 15):
    for i in range(1, 14):
        position = (i * spacing + ((i - 1) * button_row_width),
                    (j * spacing + ((j - 1) * button_row_height)))
        pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position,
                                                               (button_row_width,
                                                                button_row_height)),
                                     text=str(i)+',' + str(j),
                                     manager=manager,
                                     container=test_container,
                                     object_id='#'+str(i) + str(j))

load_time_3 = clock.tick()
print('Clear and recreation time taken:', load_time_3 / 1000.0, 'seconds.')


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
