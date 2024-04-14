import pygame
import pygame_gui

from pygame_gui.elements import UITextBox
from pygame_gui.core import ObjectID

pygame.init()


pygame.display.set_caption('Embedding images in Text Boxes')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/embedded_images_theme.json')

background = pygame.Surface((800, 600))
background.fill(manager.ui_theme.get_colour('dark_bg'))


text_box = UITextBox('<font face=noto_sans size=3 color=#FFFFFF>'
                     ''
                     '<img src="data/images/test_images/london.jpg" '
                     'float=left '
                     'padding="5px 10px 5px 5px">'
                     'Some test text in a box that will '
                     'hopefully wrap correctly around embedded images. '
                     'Best if we have a lot of text to embed the images into to give it a good testing '
                     '<img src="data/images/test_emoji.png">. This is '
                     'the first version of embedding images and is based around how HTML used to work, though '
                     'probably does not anymore.<br><br>'
                     'Some test text in a box that will hopefully wrap correctly around embedded images. '
                     'Best if we have a lot of text to embed the images into to give it a good testing. This is '
                     'the first version of embedding images and is based around how HTML used to work, though '
                     'probably does not anymore.<br><br>'
                     'Some test text in a box that will hopefully wrap correctly around embedded images. '
                     'Best if we have a lot of text to embed the images into to give it a good testing. This is '
                     'the first version of embedding images and is based around how HTML used to work, though '
                     'probably does not anymore. <br><br>'
                     'Some test text in a box that will hopefully wrap correctly around embedded images. '
                     '<img src="data/images/test_images/paris.jpg" float=right>'
                     'Best if we have a lot of text to embed the images into to give it a good testing. This is '
                     'the first version of embedding images and is based around how HTML used to work, though '
                     'probably does not anymore. <br><br>'


                     '</font>',
                     pygame.Rect((10, 10), (780, 300)),
                     manager=manager,
                     object_id=ObjectID(class_id="@text_box", object_id="#text_box_1"))

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
