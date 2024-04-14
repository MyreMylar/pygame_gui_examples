import pygame
import pygame_gui


pygame.init()


pygame.display.set_caption('Translations Test')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600),
                               theme_path='data/themes/translations_theme.json',
                               starting_language='en',
                               translation_directory_paths=['data/translations'])

background = pygame.Surface((800, 600))
background.fill(manager.ui_theme.get_colour('dark_bg'))

languages_list = ['pygame-gui.Arabic',
                  'pygame-gui.German',
                  'pygame-gui.English',
                  'pygame-gui.Spanish',
                  'pygame-gui.French',
                  'pygame-gui.Hebrew',
                  'pygame-gui.Georgian',
                  'pygame-gui.Indonesian',
                  'pygame-gui.Italian',
                  'pygame-gui.Japanese',
                  'pygame-gui.Korean',
                  'pygame-gui.Polish',
                  'pygame-gui.Portuguese',
                  'pygame-gui.Russian',
                  'pygame-gui.Ukrainian',
                  'pygame-gui.Vietnamese',
                  'pygame-gui.Chinese']

languages_dropdown = pygame_gui.elements.UIDropDownMenu(languages_list,
                                                        'pygame-gui.English',
                                                        pygame.Rect((10, 20), (250, 30)),
                                                        manager=manager)

test_label = pygame_gui.elements.UILabel(pygame.Rect((10, 100), (150, 40)),
                                         'pygame-gui.English',
                                         manager)

confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
    pygame.Rect((400, 350), (300, 200)),
    manager=manager,
    action_long_desc="examples.hello_world_message_text",
    blocking=False)

text_box = pygame_gui.elements.UITextBox(
        html_text="examples.holmes_text_test",
        relative_rect=pygame.Rect(300, 100, 400, 200),
        manager=manager)


clock = pygame.time.Clock()
is_running = True
debug_mode = False

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            debug_mode = False if debug_mode else True
            manager.set_visual_debug_mode(debug_mode)

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.text == 'pygame-gui.Arabic':
                manager.set_locale('ar')
            elif event.text == 'pygame-gui.German':
                manager.set_locale('de')
            elif event.text == 'pygame-gui.English':
                manager.set_locale('en')
            elif event.text == 'pygame-gui.Spanish':
                manager.set_locale('es')
            elif event.text == 'pygame-gui.French':
                manager.set_locale('fr')
            elif event.text == 'pygame-gui.Georgian':
                manager.set_locale('ge')
            elif event.text == 'pygame-gui.Hebrew':
                manager.set_locale('he')
            elif event.text == 'pygame-gui.Indonesian':
                manager.set_locale('id')
            elif event.text == 'pygame-gui.Italian':
                manager.set_locale('it')
            elif event.text == 'pygame-gui.Japanese':
                manager.set_locale('ja')
            elif event.text == 'pygame-gui.Korean':
                manager.set_locale('ko')
            elif event.text == 'pygame-gui.Polish':
                manager.set_locale('pl')
            elif event.text == 'pygame-gui.Portuguese':
                manager.set_locale('pt')
            elif event.text == 'pygame-gui.Russian':
                manager.set_locale('ru')
            elif event.text == 'pygame-gui.Ukrainian':
                manager.set_locale('uk')
            elif event.text == 'pygame-gui.Vietnamese':
                manager.set_locale('vi')
            elif event.text == 'pygame-gui.Chinese':
                manager.set_locale('zh')

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
