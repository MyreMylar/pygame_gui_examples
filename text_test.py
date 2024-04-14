#!/usr/bin/env python3
import pygame
import pygame_gui

from pygame_gui.ui_manager import UIManager
from pygame_gui.elements import UITextBox, UIScrollingContainer, UIDropDownMenu
from pygame_gui.core import IncrementalThreadedResourceLoader, ObjectID
from pygame_gui import UI_TEXT_BOX_LINK_CLICKED, UI_TEXT_EFFECT_FINISHED

"""
Font load time taken: 0.911 seconds.
Time taken 1st window: 1.509 seconds.
Time taken 2nd window: 0.181 seconds.
"""


def create_large_text_box():
    return UITextBox(
            '<font face=Montserrat color=regular_text><font color=#E784A2 size=4.5>'
            '<br><b><u><effect id=spin_me>Lorem</effect></u><br><br><br>'
            'ipsum dolor sit amet</b></font>,'
            ' <b><a href="test"><effect id=spin_me>consectetur</effect></a></b> '
            'adipiscing elit. in a flibb de dib do '
            'rub a la clob slip the perry tin fo glorp yip dorp'
            'skorp si pork flum de dum be dung, slob be robble glurp destination flum kin '
            'slum. Ram slim gordo, fem '
            'tulip squirrel slippers save socks certainly.<br>'
            'Vestibulum in <i>commodo me</i> tellus in nisi finibus a sodales.<br>Vestibulum '
            '<font size=2>hendrerit mi <i>sed nulla</i> scelerisque</font>, posuere ullamcorper '
            'sem pulvinar. '
            'Nulla at pulvinar a odio, a dictum dolor.<br>Maecenas at <font size=6><b>tellus a'
            'tortor. a<br>'
            'In <i><effect id=spin_me>bibendum</effect></i> orci et velit</b> gravida lacinia.'
            '<br><br>'
            'In hac a habitasse to platea dictumst.<br>'
            '<font color=#4CD656 size=4>Vivamus I interdum mollis lacus nec porttitor.<br>Morbi '
            'accumsan, lectus at '
            'tincidunt to dictum, neque <font color=#879AF6>erat tristique erat</font>, '
            'sed a tempus for <b>nunc</b> dolor in nibh.<br>'
            'Suspendisse in viverra dui <i>fringilla dolor laoreet</i>, '
            'sit amet on pharetra a ante '
            'sollicitudin.</font></font>'
            '<br><br>'
            '<b><effect id=spin_me>consectetur</effect></b> adipiscing elit. in a<br>'
            'Vestibulum in <i>commodo me</i> tellus in nisi finibus a sodales.<br>'
            'Vestibulum <font size=2>hendrerit mi <i>sed nulla</i> scelerisque</font>,'
            ' posuere ullamcorper '
            'sem pulvinar. '
            'Nulla at pulvinar a odio, a dictum dolor.<br>'
            'Maepenas at <font size=6><b>tellus a tortor. a<br>'
            'In <i>bibendum</i> orci et velit</b> gravida lacinia.<br><br>'
            'In hac a habitasse to platea dictumst.<br>'
            '<font color=#4CD656 size=4>Vivamus I interdum mollis lacus nec porttitor.<br>Morbi '
            'accumsan, lectus at'
            'tincidunt to dictum, neque <font color=#879AF6>erat tristique erat</font>, '
            'sed a <effect id=spin_me>tempus</effect> for <b><effect id=spin_me>nunc</effect>'
            '</b> dolor in nibh.<br>'
            'Suspendisse in viverra dui <i>fringilla dolor laoreet</i>, sit amet on'
            ' pharetra a ante '
            'sollicitudin.</font></font>',
            pygame.Rect(10, 10, 500, 580),
            manager=ui_manager,
            object_id='#text_box_1')


pygame.init()

pygame.display.set_caption("Text test")
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)  # FULLSCREEN

background_surface = pygame.Surface(screen_size)
background_surface.fill(pygame.Color("#000000"))

loader = IncrementalThreadedResourceLoader()
clock = pygame.time.Clock()
ui_manager = UIManager(screen_size, 'data/themes/theme_1.json', resource_loader=loader)
ui_manager.add_font_paths("Montserrat",
                          "data/fonts/Montserrat-Regular.ttf",
                          "data/fonts/Montserrat-Bold.ttf",
                          "data/fonts/Montserrat-Italic.ttf",
                          "data/fonts/Montserrat-BoldItalic.ttf")

load_time_1 = clock.tick()
ui_manager.preload_fonts([{'name': 'Montserrat', 'html_size': 4.5, 'style': 'bold'},
                          {'name': 'Montserrat', 'html_size': 4.5, 'style': 'regular'},
                          {'name': 'Montserrat', 'html_size': 2, 'style': 'regular'},
                          {'name': 'Montserrat', 'html_size': 2, 'style': 'italic'},
                          {'name': 'Montserrat', 'html_size': 6, 'style': 'bold'},
                          {'name': 'Montserrat', 'html_size': 6, 'style': 'regular'},
                          {'name': 'Montserrat', 'html_size': 6, 'style': 'bold_italic'},
                          {'name': 'Montserrat', 'html_size': 4, 'style': 'bold'},
                          {'name': 'Montserrat', 'html_size': 4, 'style': 'regular'},
                          {'name': 'Montserrat', 'html_size': 4, 'style': 'italic'},
                          {'name': 'noto_sans', 'html_size': 2, 'style': 'regular'},
                          {'name': 'noto_sans', 'html_size': 2, 'style': 'bold'},
                          {'name': 'noto_sans', 'html_size': 2, 'style': 'bold_italic'}
                          ])
loader.start()
finished_loading = False
while not finished_loading:
    finished_loading, progress = loader.update()
load_time_2 = clock.tick()
print('Font load time taken:', load_time_2/1000.0, 'seconds.')

time_1 = clock.tick()
html_text_line = create_large_text_box()
time_2 = clock.tick()


htm_text_block_2 = UITextBox('<font face=noto_sans size=2 color=#000000><b>Hey, What the heck! </b>'
                             '<br><br>'
                             '<body bgcolor=#A0A050>This is</body> some <a href="test">text</a> '
                             'in a different box,'
                             ' hooray for variety - '
                             'if you want then you should put a ring upon it. '
                             '<body bgcolor=#990000>What if we do a really long word?</body> '
                             '<b><i>derp FALALALALALALALXALALALXALALALALAAPaaaaarp gosh'
                             '</b></i></font>',
                             pygame.Rect((520, 10), (250, -1)),
                             manager=ui_manager,
                             object_id=ObjectID(class_id="@white_text_box",
                                                object_id="#text_box_2"))
htm_text_block_2.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)

time_3 = clock.tick()

print('Time taken 1st window:', time_2/1000.0, 'seconds.')
print('Time taken 2nd window:', time_3/1000.0, 'seconds.')


ui_manager.print_unused_fonts()

scrolling_container = UIScrollingContainer(pygame.Rect(520, 250, 250, 300),
                                           allow_scroll_x=False,
                                           should_grow_automatically=False)
scrolling_container.set_scrollable_area_dimensions((250, 600))


text_box_inside_scrolling_container = UITextBox(html_text="Some text inside a text box, itself"
                                                          " inside a container that scrolls",
                                                relative_rect=pygame.Rect(20, 20, 150, 200),
                                                container=scrolling_container)

scrolling_text_box_inside_scrolling_container = UITextBox(html_text="Some text inside a scrolling text box, itself"
                                                                    " inside a container that scrolls. "
                                                                    "scrolling should work correctly with the mousewheel, "
                                                                    "depending on whether we are hovering this text box, or"
                                                                    " whether we are hovering other stuff in the "
                                                                    "scrolling container",
                                                          relative_rect=pygame.Rect(20, 280, 180, 200),
                                                          container=scrolling_container)

running = True

while running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                htm_text_block_2.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_OUT)
            if event.key == pygame.K_g:
                htm_text_block_2.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_IN)
            if event.key == pygame.K_h:
                htm_text_block_2.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
            if event.key == pygame.K_k:
                html_text_line.kill()
            if event.key == pygame.K_b:
                html_text_line = create_large_text_box()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            html_text_line.set_active_effect(pygame_gui.TEXT_EFFECT_TILT,
                                             effect_tag='spin_me')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            html_text_line.set_active_effect(pygame_gui.TEXT_EFFECT_EXPAND_CONTRACT,
                                             params={'max_scale': 5.0},
                                             effect_tag='spin_me')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
            html_text_line.set_active_effect(pygame_gui.TEXT_EFFECT_BOUNCE,
                                             params={'bounce_max_height': 50,
                                                     'time_to_complete_bounce': 0.8},
                                             effect_tag='spin_me')

        if event.type == UI_TEXT_BOX_LINK_CLICKED:
            if event.ui_element is htm_text_block_2:
                if event.link_target == 'test':
                    print('clicked test link')
            else:
                print('clicked link in text block 1')

        if event.type == UI_TEXT_EFFECT_FINISHED:
            print("finished text effect: " + event.effect)

        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    screen.blit(background_surface, (0, 0))
    ui_manager.draw_ui(screen)

    pygame.display.update()
