import random

import pygame
import pygame_gui

from pygame_gui import UIManager, PackageResource

from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIButton
from pygame_gui.elements import UIHorizontalSlider
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UIDropDownMenu
from pygame_gui.elements import UIScreenSpaceHealthBar
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIImage
from pygame_gui.elements import UIPanel
from pygame_gui.elements import UISelectionList

from pygame_gui.windows import UIMessageWindow


class ScalingWindow(UIWindow):
    def __init__(self, rect, ui_manager):
        super().__init__(rect, ui_manager,
                         window_display_title='Scale',
                         object_id='#scaling_window',
                         resizable=True)

        loaded_test_image = pygame.image.load('data/images/splat.png').convert_alpha()
        self.test_image = UIImage(pygame.Rect((10, 10), (self.get_container().get_size()[0] - 20,
                                                         self.get_container().get_size()[1] - 20)),
                                  loaded_test_image, self.ui_manager,
                                  container=self,
                                  anchors={'top': 'top', 'bottom': 'bottom',
                                           'left': 'left', 'right': 'right'})

        self.set_blocking(True)


class EverythingWindow(UIWindow):
    def __init__(self, rect, ui_manager):
        super().__init__(rect, ui_manager,
                         window_display_title='Everything Container',
                         object_id='#everything_window',
                         resizable=True)

        self.test_slider = UIHorizontalSlider(pygame.Rect((int(self.rect.width / 2),
                                                           int(self.rect.height * 0.70)),
                                                          (240, 25)),
                                              50.0,
                                              (0.0, 100.0),
                                              self.ui_manager,
                                              container=self)

        self.slider_label = UILabel(pygame.Rect((int(self.rect.width / 2) + 250,
                                                 int(self.rect.height * 0.70)),
                                                (27, 25)),
                                    str(int(self.test_slider.get_current_value())),
                                    self.ui_manager,
                                    container=self)

        self.test_text_entry = UITextEntryLine(pygame.Rect((int(self.rect.width / 2),
                                                            int(self.rect.height * 0.50)),
                                                           (200, -1)),
                                               self.ui_manager,
                                               container=self)
        self.test_text_entry.set_forbidden_characters('numbers')

        current_resolution_string = 'Item 1'
        self.test_drop_down_menu = UIDropDownMenu(['Item 1',
                                                   'Item 2',
                                                   'Item 3',
                                                   'Item 4',
                                                   'Item 5',
                                                   'Item 6',
                                                   'Item 7',
                                                   'Item 8',
                                                   'Item 9',
                                                   'Item 10',
                                                   'Item 11',
                                                   'Item 12',
                                                   'Item 13',
                                                   'Item 14',
                                                   'Item 15',
                                                   'Item 16',
                                                   'Item 17',
                                                   'Item 18',
                                                   'Item 19',
                                                   'Item 20',
                                                   'Item 21',
                                                   'Item 22',
                                                   'Item 23',
                                                   'Item 24',
                                                   'Item 25',
                                                   'Item 26',
                                                   'Item 27',
                                                   'Item 28',
                                                   'Item 29',
                                                   'Item 30'
                                                   ],
                                                  current_resolution_string,
                                                  pygame.Rect((int(self.rect.width / 2),
                                                               int(self.rect.height * 0.3)),
                                                              (200, 25)),
                                                  self.ui_manager,
                                                  container=self)

        self.health_bar = UIScreenSpaceHealthBar(pygame.Rect((int(self.rect.width / 9),
                                                              int(self.rect.height * 0.7)),
                                                             (200, 20)),
                                                 self.ui_manager,
                                                 container=self)

        loaded_test_image = pygame.image.load('data/images/splat.png').convert_alpha()

        self.test_image = UIImage(pygame.Rect((int(self.rect.width / 9),
                                               int(self.rect.height * 0.3)),
                                              loaded_test_image.get_rect().size),
                                  loaded_test_image, self.ui_manager,
                                  container=self)

    def update(self, time_delta):
        super().update(time_delta)

        if self.alive() and self.test_slider.has_moved_recently:
            self.slider_label.set_text(str(int(self.test_slider.get_current_value())))


class Options:
    def __init__(self):
        self.resolution = (800, 600)
        self.fullscreen = False


class OptionsUIApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Options UI")
        self.options = Options()
        if self.options.fullscreen:
            self.window_surface = pygame.display.set_mode(self.options.resolution,
                                                          pygame.FULLSCREEN)
        else:
            self.window_surface = pygame.display.set_mode(self.options.resolution)

        self.background_surface = None

        self.ui_manager = UIManager(self.options.resolution,
                                    PackageResource(package='data.themes',
                                                    resource='theme_2.json'))
        self.ui_manager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
                                       {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
                                       {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
                                       {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
                                       {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
                                       ])

        self.test_button = None
        self.test_button_2 = None
        self.test_button_3 = None
        self.test_slider = None
        self.test_text_entry = None
        self.test_drop_down = None
        self.panel = None

        self.message_window = None

        self.recreate_ui()

        self.clock = pygame.time.Clock()

        self.button_response_timer = pygame.time.Clock()
        self.running = True
        self.debug_mode = False

    def recreate_ui(self):
        self.ui_manager.set_window_resolution(self.options.resolution)
        self.ui_manager.clear_and_reset()

        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.ui_manager.get_theme().get_colour('dark_bg'))

        self.test_button = UIButton(pygame.Rect((int(self.options.resolution[0] / 2),
                                                 int(self.options.resolution[1] * 0.90)),
                                                (100, 40)),
                                    '',
                                    self.ui_manager,
                                    tool_tip_text="<font face=fira_code color=normal_text size=2>"
                                                  "<b><u>Test Tool Tip</u></b>"
                                                  "<br><br>"
                                                  "A little <i>test</i> of the "
                                                  "<font color=#FFFFFF><b>tool tip</b></font>"
                                                  " functionality."
                                                  "<br><br>"
                                                  "Unleash the Kraken!"
                                                  "</font>",
                                    object_id='#hover_me_button')

        self.test_button_2 = UIButton(pygame.Rect((int(self.options.resolution[0] / 3),
                                                   int(self.options.resolution[1] * 0.90)),
                                                  (100, 40)),
                                      'EVERYTHING',
                                      self.ui_manager,
                                      object_id='#everything_button')

        self.test_button_3 = UIButton(pygame.Rect((int(self.options.resolution[0] / 6),
                                                   int(self.options.resolution[1] * 0.90)),
                                                  (100, 40)),
                                      'Scaling?',
                                      self.ui_manager,
                                      object_id='#scaling_button')

        self.test_slider = UIHorizontalSlider(pygame.Rect((int(self.options.resolution[0] / 2),
                                                           int(self.options.resolution[1] * 0.70)),
                                                          (240, 25)),
                                              25.0,
                                              (0.0, 100.0),
                                              self.ui_manager,
                                              object_id='#cool_slider')

        self.test_text_entry = UITextEntryLine(pygame.Rect((int(self.options.resolution[0] / 2),
                                                            int(self.options.resolution[1] * 0.50)),
                                                           (200, -1)),
                                               self.ui_manager,
                                               object_id='#main_text_entry')

        current_resolution_string = (str(self.options.resolution[0]) +
                                     'x' +
                                     str(self.options.resolution[1]))
        self.test_drop_down = UIDropDownMenu(['640x480', '800x600', '1024x768'],
                                             current_resolution_string,
                                             pygame.Rect((int(self.options.resolution[0] / 2),
                                                          int(self.options.resolution[1] * 0.3)),
                                                         (200, 25)),
                                             self.ui_manager)

        self.panel = UIPanel(pygame.Rect(50, 50, 200, 300),
                             starting_layer_height=4,
                             manager=self.ui_manager)

        UIButton(pygame.Rect(10, 10, 174, 30), 'Panel Button',
                 manager=self.ui_manager,
                 container=self.panel)

        UISelectionList(pygame.Rect(10, 50, 174, 200),
                        item_list=['Item 1',
                                   'Item 2',
                                   'Item 3',
                                   'Item 4',
                                   'Item 5',
                                   'Item 6',
                                   'Item 7',
                                   'Item 8',
                                   'Item 9',
                                   'Item 10',
                                   'Item 11',
                                   'Item 12',
                                   'Item 13',
                                   'Item 14',
                                   'Item 15',
                                   'Item 16',
                                   'Item 17',
                                   'Item 18',
                                   'Item 19',
                                   'Item 20'
                                   ],
                        manager=self.ui_manager,
                        container=self.panel,
                        allow_multi_select=True)

    def create_message_window(self):
        self.button_response_timer.tick()
        self.message_window = UIMessageWindow(
            rect=pygame.Rect((random.randint(0, self.options.resolution[0] - 300),
                              random.randint(0, self.options.resolution[1] - 200)),
                             (300, 250)),
            window_title='Test Message Window',
            html_message='<font color=normal_text>'
                         'This is a <a href="test">test</a> message to see if '
                         'this box <a href=actually_link>actually</a> works.'
                         ''
                         'In <i>bibendum</i> orci et velit</b> gravida lacinia.<br><br><br> '
                         'In hac a habitasse to platea dictumst.<br>'
                         ' <font color=#4CD656 size=4>Vivamus I interdum mollis lacus nec '
                         'porttitor.<br> Morbi'
                         ' accumsan, lectus at'
                         ' tincidunt to dictum, neque <font color=#879AF6>erat tristique'
                         ' blob</font>,'
                         ' sed a tempus for <b>nunc</b> dolor in nibh.<br>'
                         ' Suspendisse in viverra dui <i>fringilla dolor laoreet</i>, sit amet '
                         'on pharetra a ante'
                         ' sollicitudin.</font>'
                         '<br><br>'
                         'In <i>bibendum</i> orci et velit</b> gravida lacinia.<br><br><br> '
                         'In hac a habitasse to platea dictumst.<br>'
                         ' <font color=#4CD656 size=4>Vivamus I interdum mollis lacus nec '
                         'porttitor.<br> Morbi'
                         ' accumsan, lectus at'
                         ' tincidunt to dictum, neque <font color=#879AF6>erat tristique '
                         'erat</font>,'
                         ' sed a tempus for <b>nunc</b> dolor in nibh.<br>'
                         ' Suspendisse in viverra dui <i>fringilla dolor laoreet</i>, sit amet '
                         'on pharetra a ante'
                         ' sollicitudin.</font>'
                         '<br><br>'
                         'In <i>bibendum</i> orci et velit</b> gravida lacinia.<br><br><br> '
                         'In hac a habitasse to platea dictumst.<br>'
                         ' <font color=#4CD656 size=4>Vivamus I interdum mollis lacus nec '
                         'porttitor.<br> Morbi'
                         ' accumsan, lectus at'
                         ' tincidunt to dictum, neque <font color=#879AF6>erat tristique '
                         'erat</font>,'
                         ' sed a tempus for <b>nunc</b> dolor in nibh.<br>'
                         ' Suspendisse in viverra dui <i>fringilla dolor laoreet</i>, '
                         'sit amet on pharetra a ante'
                         ' sollicitudin.</font>'
                         '</font>',
            manager=self.ui_manager)
        time_taken = self.button_response_timer.tick() / 1000.0
        # currently taking about 0.35 seconds down from 0.55 to create
        # an elaborately themed message window.
        # still feels a little slow but it's better than it was.
        print("Time taken to create message window: " + str(time_taken))

    def check_resolution_changed(self):
        resolution_string = self.test_drop_down.selected_option.split('x')
        resolution_width = int(resolution_string[0])
        resolution_height = int(resolution_string[1])
        if (resolution_width != self.options.resolution[0] or
                resolution_height != self.options.resolution[1]):
            self.options.resolution = (resolution_width, resolution_height)
            self.window_surface = pygame.display.set_mode(self.options.resolution)
            self.recreate_ui()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui_manager.process_events(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.debug_mode = False if self.debug_mode else True
                self.ui_manager.set_visual_debug_mode(self.debug_mode)

            if event.type == pygame.USEREVENT:
                if (event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                        event.ui_object_id == '#main_text_entry'):
                    print(event.text)

                if event.user_type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                    if event.link_target == 'test':
                        print("clicked test link")
                    elif event.link_target == 'actually_link':
                        print("clicked actually link")

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.test_button:
                        self.test_button.set_text(random.choice(['', 'Hover me!',
                                                                 'Click this.',
                                                                 'A Button']))
                        self.create_message_window()

                    if event.ui_element == self.test_button_3:
                        ScalingWindow(pygame.Rect((50, 50), (224, 224)), self.ui_manager)
                    if event.ui_element == self.test_button_2:
                        EverythingWindow(pygame.Rect((10, 10), (640, 480)), self.ui_manager)

                if (event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
                        and event.ui_element == self.test_drop_down):
                    self.check_resolution_changed()

    def run(self):
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0

            # check for input
            self.process_events()

            # respond to input
            self.ui_manager.update(time_delta)

            # draw graphics
            self.window_surface.blit(self.background_surface, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()


if __name__ == '__main__':
    app = OptionsUIApp()
    app.run()
