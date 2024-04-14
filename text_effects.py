import pygame
import pygame_gui

from pygame_gui.elements import UITextBox, UILabel, UIButton, UITooltip

pygame.init()


pygame.display.set_caption('Text Effects')
window_surface = pygame.display.set_mode((800, 600))
ui_manager = pygame_gui.UIManager((800, 600), 'data/themes/text_effects_theme.json')

background = pygame.Surface((800, 600))
background.fill((50, 50, 40))  # ui_manager.get_theme().get_colour('dark_bg')

ui_manager.add_font_paths("PermanentMarker",
                          "data/fonts/PermanentMarker-Regular.ttf")

ui_manager.preload_fonts([{'name': 'PermanentMarker', 'point_size': 14, 'style': 'regular'}])

text_box = UITextBox(
        html_text="My "
                  "<shadow size=1 color=#553520>"
                  "<font face=PermanentMarker color=#A06545>"
                  "<effect id=test>EARTHQUAKE</effect> "
                  "</font>"
                  "</shadow>"
                  "will <font face=PermanentMarker>"
                  "<effect id=shatter>SHATTER</effect>"
                  "</font>"
                  " your bones. Puny Mortals.",
        relative_rect=pygame.Rect(100, 100, 200, 100),
        manager=ui_manager)

effect_label = UILabel(
        relative_rect=pygame.Rect(500, 100, -1, -1),
        text='A row of appearing text',
        manager=ui_manager)

clock = pygame.time.Clock()
is_running = True

debug_chunks = False

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            effect_label.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR,
                                           params={'time_per_letter': 0.01})

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            effect_label.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_IN,
                                           params={'time_per_alpha_change': 0.1})

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR,
                                       params={'time_per_letter': 0.05,
                                               'time_per_letter_deviation': 0.02})

        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR,
                                       params={'time_per_letter': 0.05,
                                               'time_per_letter_deviation': 0.02},
                                       effect_tag='test')

        if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            text_box.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_OUT,
                                       effect_tag='test')

        if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            text_box.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_IN,
                                       effect_tag='test')

        if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            text_box.set_active_effect(pygame_gui.TEXT_EFFECT_BOUNCE,
                                       effect_tag='test')

        if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
            text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TILT,
                                       effect_tag='test')

        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            text_box.set_active_effect(pygame_gui.TEXT_EFFECT_SHAKE,
                                       params={'loop': False,
                                               'frequency': 45,
                                               'amplitude': 10,
                                               'duration': 3.0},
                                       effect_tag='test')

        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TILT,
                                       effect_tag='shatter')

        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            debug_chunks = not debug_chunks

            for row in text_box.text_box_layout.layout_rows:
                for chunk in row.items:
                    print(chunk)

        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    ui_manager.draw_ui(window_surface)

    if debug_chunks:
        text_box_offset = (text_box.padding[0] + text_box.border_width +
                           text_box.shadow_width +
                           text_box.rounded_corner_width_offsets[0],
                           text_box.padding[1] + text_box.border_width +
                           text_box.shadow_width +
                           text_box.rounded_corner_width_offsets[0])
        for row in text_box.text_box_layout.layout_rows:
            for chunk in row.items:
                debug_rect = chunk.copy()
                debug_rect.top += text_box.rect.top + text_box_offset[1]
                debug_rect.left += text_box.rect.left + text_box_offset[0]
                pygame.draw.rect(window_surface, pygame.Color('#FF0000'), debug_rect, 1)
            debug_row = row.copy()
            debug_row.top += text_box.rect.top + text_box_offset[1]
            debug_row.left += text_box.rect.left + text_box_offset[0]
            pygame.draw.rect(window_surface, pygame.Color('#0000FF'), debug_row, 1)

    pygame.display.update()
