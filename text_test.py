#!/usr/bin/env python3
import pygame

from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_text_box import UITextBox


pygame.init()

pygame.display.set_caption("Text test")
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)  # FULLSCREEN

background_surface = pygame.Surface(screen_size)
background_surface.fill(pygame.Color("#000000"))
clock = pygame.time.Clock()
ui_manager = UIManager(screen_size, 'data/themes/theme_1.json')
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
                          {'name': 'fira_code', 'html_size': 2, 'style': 'regular'},
                          {'name': 'fira_code', 'html_size': 2, 'style': 'bold'},
                          {'name': 'fira_code', 'html_size': 2, 'style': 'bold_italic'}
                          ])
load_time_2 = clock.tick()
print('Font load time taken:', load_time_2/1000.0, 'seconds.')

time_1 = clock.tick()
html_text_line = UITextBox(
    '<font face=Montserrat color=#E0E2E4><font color=#E784A2 size=4.5><br><b><u>Lorem</u><br><br><br>'
    'ipsum dolor sit amet</b></font>,'
    ' <b><a href="test">consectetur</a></b> adipiscing elit. in a flibb de dib do '
    'rub a la clob slip the perry tin fo glorp yip dorp'
    'skorp si pork flum de dum be dung, slob be robble glurp destination flum kin slum. Ram slim gordo, fem '
    'tulip squirrel slippers save socks certainly.<br>'
    'Vestibulum in <i>commodo me</i> tellus in nisi finibus a sodales.<br>Vestibulum'
    ' <font size=2>hendrerit mi <i>sed nulla</i> scelerisque</font>, posuere ullamcorper '
    'sem pulvinar.'
    ' Nulla at pulvinar a odio, a dictum dolor.<br>Maecenas at <font size=6><b>tellus a'
    ' tortor. a<br>'
    'In <i>bibendum</i> orci et velit</b> gravida lacinia.<br><br><br>'
    'In hac a habitasse to platea dictumst.<br>'
    '<font color=#4CD656 size=4>Vivamus I interdum mollis lacus nec porttitor.<br>Morbi'
    ' accumsan, lectus at'
    ' tincidunt to dictum, neque <font color=#879AF6>erat tristique erat</font>,'
    ' sed a tempus for <b>nunc</b> dolor in nibh.<br>'
    ' Suspendisse in viverra dui <i>fringilla dolor laoreet</i>, sit amet on pharetra a ante'
    ' sollicitudin.</font></font>'
    '<br><br>'
    ' <b>consectetur</b> adipiscing elit. in a<br>'
    'Vestibulum in <i>commodo me</i> tellus in nisi finibus a sodales.<br> Vestibulum'
    ' <font size=2>hendrerit mi <i>sed nulla</i> scelerisque</font>, posuere ullamcorper '
    'sem pulvinar.'
    ' Nulla at pulvinar a odio, a dictum dolor.<br> Maecenas at <font size=6><b>tellus a'
    ' tortor. a<br> '
    'In <i>bibendum</i> orci et velit</b> gravida lacinia.<br><br><br> '
    'In hac a habitasse to platea dictumst.<br>'
    ' <font color=#4CD656 size=4>Vivamus I interdum mollis lacus nec porttitor.<br>Morbi'
    ' accumsan, lectus at'
    ' tincidunt to dictum, neque <font color=#879AF6>erat tristique erat</font>,'
    ' sed a tempus for <b>nunc</b> dolor in nibh.<br>'
    ' Suspendisse in viverra dui <i>fringilla dolor laoreet</i>, sit amet on pharetra a ante'
    ' sollicitudin.</font></font>',
    pygame.Rect(10, 10, 500, 580),
    manager=ui_manager,
    object_id='#text_box_1')

time_2 = clock.tick()


htm_text_block_2 = UITextBox('<font face=fira_code size=2 color=#000000><b>Hey, What the heck!</b>'
                             '<br><br>'
                             'This is some <a href="test">text</a> in a different box, hooray for variety - '
                             'if you want then you should put a ring upon it. '
                             '<body bgcolor=#990000>What if we do a really long word?</body> '
                             '<b><i>derp FALALALALALALALXALALALXALALALALAAPaaaaarp gosh</b></i></font>',
                             pygame.Rect((520, 10), (250, 200)),
                             manager=ui_manager,
                             object_id="#text_box_2")
htm_text_block_2.set_active_effect('typing_appear')
time_3 = clock.tick()

print('Time taken 1st window:', time_2/1000.0, 'seconds.')
print('Time taken 2nd window:', time_3/1000.0, 'seconds.')


ui_manager.print_unused_fonts()

running = True

clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                htm_text_block_2.set_active_effect('fade_out')
        if event.type == pygame.USEREVENT:
            if event.user_type == 'ui_text_box_link_clicked':
                if event.ui_element is htm_text_block_2:
                    if event.link_target == 'test':
                        print('clicked test link')
                else:
                    print('clicked link in text block 1')

        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    screen.blit(background_surface, (0, 0))
    ui_manager.draw_ui(screen)

    pygame.display.update()
