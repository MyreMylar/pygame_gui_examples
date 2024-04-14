import pygame
import pygame_gui
import random


pygame.init()


pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/quick_theme.json')

background = pygame.Surface((800, 600))
background.fill(manager.ui_theme.get_colour('dark_bg'))


static_dimensions_window = pygame_gui.elements.UIWindow(rect=pygame.Rect((50, 50), (600, 300)),
                                                        manager=manager, resizable=True,
                                                        window_display_title='Static Dimensions')
static_dimensions_window.set_minimum_dimensions((580, 270))

a1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                  text='A1', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'top',
                                           'left': 'left',
                                           'bottom': 'top',
                                           'right': 'left'})

a2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                  text='A2', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'top',
                                           'left': 'left',
                                           'bottom': 'top',
                                           'right': 'left',
                                           'top_target': a1})

a3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                  text='A3', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'top',
                                           'left': 'left',
                                           'bottom': 'top',
                                           'right': 'left',
                                           'left_target': a1})

a4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                  text='A4', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'top',
                                           'left': 'left',
                                           'bottom': 'top',
                                           'right': 'left',
                                           'top_target': a3,
                                           'left_target': a2})


b1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, -40), (100, 30)),
                                  text='B1', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'bottom',
                                           'left': 'left',
                                           'bottom': 'bottom',
                                           'right': 'left'})

b2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, -40), (100, 30)),
                                  text='B2', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'bottom',
                                           'left': 'left',
                                           'bottom': 'bottom',
                                           'right': 'left',
                                           'bottom_target': b1})

b3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, -40), (100, 30)),
                                  text='B3', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'bottom',
                                           'left': 'left',
                                           'bottom': 'bottom',
                                           'right': 'left',
                                           'left_target': b1})

b4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, -40), (100, 30)),
                                  text='B4', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'bottom',
                                           'left': 'left',
                                           'bottom': 'bottom',
                                           'right': 'left',
                                           'bottom_target': b3,
                                           'left_target': b2})


c1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-110, 10), (100, 30)),
                                  text='C1', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'top',
                                           'left': 'right',
                                           'bottom': 'top',
                                           'right': 'right'})

c2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-110, 10), (100, 30)),
                                  text='C2', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'top',
                                           'left': 'right',
                                           'bottom': 'top',
                                           'right': 'right',
                                           'top_target': c1})

c3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-110, 10), (100, 30)),
                                  text='C3', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'top',
                                           'left': 'right',
                                           'bottom': 'top',
                                           'right': 'right',
                                           'right_target': c1})

c4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-110, 10), (100, 30)),
                                  text='C4', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'top',
                                           'left': 'right',
                                           'bottom': 'top',
                                           'right': 'right',
                                           'top_target': c3,
                                           'right_target': c2})


d1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-110, -40), (100, 30)),
                                  text='D1', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'bottom',
                                           'left': 'right',
                                           'bottom': 'bottom',
                                           'right': 'right'})

d2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-110, -40), (100, 30)),
                                  text='D2', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'bottom',
                                           'left': 'right',
                                           'bottom': 'bottom',
                                           'right': 'right',
                                           'bottom_target': d1})

d3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-110, -40), (100, 30)),
                                  text='D3', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'bottom',
                                           'left': 'right',
                                           'bottom': 'bottom',
                                           'right': 'right',
                                           'right_target': d1})

d4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-110, -40), (100, 30)),
                                  text='D4', manager=manager,
                                  container=static_dimensions_window,
                                  anchors={'top': 'bottom',
                                           'left': 'right',
                                           'bottom': 'bottom',
                                           'right': 'right',
                                           'bottom_target': d3,
                                           'right_target': d2})

goose_gap_x = d4.get_abs_rect().left - a4.get_abs_rect().right - 20
goose_gap_y = d4.get_abs_rect().top - a4.get_abs_rect().bottom - 20

golden_goose = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10),
                                                                      (goose_gap_x, goose_gap_y)),
                                            text='Goose', manager=manager,
                                            container=static_dimensions_window,
                                            anchors={'top': 'top',
                                                     'left': 'left',
                                                     'bottom': 'bottom',
                                                     'right': 'right',
                                                     'top_target': a4,
                                                     'left_target': a4,
                                                     'bottom_target': d4,
                                                     'right_target': d4})

dynamic_dimensions_window = pygame_gui.elements.UIWindow(rect=pygame.Rect((150, 80), (600, 300)),
                                                         manager=manager, resizable=True,
                                                         window_display_title='Dynamic Dimensions')

da1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                   text='A1', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'top',
                                            'left': 'left',
                                            'bottom': 'top',
                                            'right': 'left'})

da2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                   text='A2', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'top',
                                            'left': 'left',
                                            'bottom': 'top',
                                            'right': 'left',
                                            'top_target': da1})

da3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                   text='A3', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'top',
                                            'left': 'left',
                                            'bottom': 'top',
                                            'right': 'left',
                                            'left_target': da1})

da4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                   text='A4', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'top',
                                            'left': 'left',
                                            'bottom': 'top',
                                            'right': 'left',
                                            'top_target': da3,
                                            'left_target': da2})


db1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, -10), (-1, -1)),
                                   text='DB1', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'bottom',
                                            'left': 'left',
                                            'bottom': 'bottom',
                                            'right': 'left'})

db2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, -10), (-1, -1)),
                                   text='DB2', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'bottom',
                                            'left': 'left',
                                            'bottom': 'bottom',
                                            'right': 'left',
                                            'bottom_target': db1})

db3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, -10), (-1, -1)),
                                   text='DB3', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'bottom',
                                            'left': 'left',
                                            'bottom': 'bottom',
                                            'right': 'left',
                                            'left_target': db1})

db4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, -10), (-1, -1)),
                                   text='DB4', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'bottom',
                                            'left': 'left',
                                            'bottom': 'bottom',
                                            'right': 'left',
                                            'bottom_target': db3,
                                            'left_target': db2})


dc1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-10, 10), (-1, 30)),
                                   text='DC1', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'top',
                                            'left': 'right',
                                            'bottom': 'top',
                                            'right': 'right'})

dc2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-10, 10), (-1, 30)),
                                   text='DC2', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'top',
                                            'left': 'right',
                                            'bottom': 'top',
                                            'right': 'right',
                                            'top_target': dc1})

dc3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-10, 10), (-1, 30)),
                                   text='DC3', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'top',
                                            'left': 'right',
                                            'bottom': 'top',
                                            'right': 'right',
                                            'right_target': dc1})

dc4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-10, 10), (-1, 30)),
                                   text='DC4', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'top',
                                            'left': 'right',
                                            'bottom': 'top',
                                            'right': 'right',
                                            'top_target': dc3,
                                            'right_target': dc2})


dd1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-10, -40), (-1, 30)),
                                   text='DD1', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'bottom',
                                            'left': 'right',
                                            'bottom': 'bottom',
                                            'right': 'right'})

dd2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-10, -40), (-1, 30)),
                                   text='DD2', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'bottom',
                                            'left': 'right',
                                            'bottom': 'bottom',
                                            'right': 'right',
                                            'bottom_target': dd1})

dd3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-10, -40), (-1, 30)),
                                   text='DD3', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'bottom',
                                            'left': 'right',
                                            'bottom': 'bottom',
                                            'right': 'right',
                                            'right_target': dd1})

dd4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-10, -40), (-1, 30)),
                                   text='DD4', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'bottom',
                                            'left': 'right',
                                            'bottom': 'bottom',
                                            'right': 'right',
                                            'bottom_target': dd3,
                                            'right_target': dd2})

dd5 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-10, -40), (-1, 30)),
                                   text='DD5', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'bottom',
                                            'left': 'right',
                                            'bottom': 'bottom',
                                            'right': 'right',
                                            'right_target': dd3})

dd6 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-10, -40), (-1, 30)),
                                   text='DD6', manager=manager,
                                   container=dynamic_dimensions_window,
                                   anchors={'top': 'bottom',
                                            'left': 'right',
                                            'bottom': 'bottom',
                                            'right': 'right',
                                            'right_target': dd4,
                                            'bottom_target': dd5})

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                random.choice([db1, db2, db3, db4, dc1, dc2, dc3, dc4]).set_text(
                    random.choice(['Heya', 'Sup', 'Whoooah', 'Amazing!',
                                   'Yipes!', 'Doh', 'Xylophonic']))

            if event.key == pygame.K_d:
                random.choice([dd1, dd2]).set_text(
                    random.choice(['Heya', 'Sup', 'Whoooah', 'Amazing!',
                                   'Yipes!', 'Doh', 'Xylophonic']))

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
