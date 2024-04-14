import random
import pygame_gui
from collections import deque
from typing import Optional

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
from pygame_gui.core import ObjectID


import pygame


class ScalingWindow(UIWindow):
    def __init__(self, rect, ui_manager):
        super().__init__(rect, ui_manager,
                         window_display_title='Scale',
                         object_id='#scaling_window',
                         resizable=True)

        loaded_test_image = pygame.image.load('data/images/splat.bmp').convert_alpha()
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
                                              container=self,
                                              click_increment=5)

        self.slider_label = UILabel(pygame.Rect((int(self.rect.width / 2) + 250,
                                                 int(self.rect.height * 0.70)),
                                                (28, 25)),
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
                                                             (200, 30)),
                                                 self.ui_manager,
                                                 container=self)

        loaded_test_image = pygame.image.load('data/images/splat.bmp').convert_alpha()

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
        self.ui_manager.preload_fonts([{'name': 'noto_sans', 'point_size': 10, 'style': 'bold'},
                                       {'name': 'noto_sans', 'point_size': 10, 'style': 'regular'},
                                       {'name': 'noto_sans', 'point_size': 10, 'style': 'italic'},
                                       {'name': 'noto_sans', 'point_size': 14, 'style': 'italic'},
                                       {'name': 'noto_sans', 'point_size': 14, 'style': 'bold'}
                                       ])

        self.test_button = None
        self.test_button_2 = None
        self.test_button_3 = None
        self.test_slider = None
        self.test_text_entry: Optional[UITextEntryLine] = None
        self.test_drop_down = None
        self.test_drop_down_2 = None
        self.panel = None
        self.fps_counter = None
        self.frame_timer = None
        self.disable_toggle = None
        self.hide_toggle = None
        self.list: Optional[UISelectionList] = None

        self.message_window = None

        self.recreate_ui()

        self.clock = pygame.time.Clock()
        self.time_delta_stack = deque([])

        self.button_response_timer = pygame.time.Clock()
        self.running = True
        self.debug_mode = False

        self.all_enabled = True
        self.all_shown = True

    def recreate_ui(self):
        self.ui_manager.set_window_resolution(self.options.resolution)
        self.ui_manager.clear_and_reset()

        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.ui_manager.get_theme().get_colour('dark_bg'))

        self.test_button = UIButton(pygame.Rect((int(self.options.resolution[0] / 2),
                                                 int(self.options.resolution[1] * 0.90)),
                                                (120, 40)),
                                    '',
                                    self.ui_manager,
                                    tool_tip_text="<font face=noto_sans color=normal_text size=2>"
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
                                                  (110, 40)),
                                      'EVERYTHING',
                                      self.ui_manager,
                                      tool_tip_text="A <i>little</i> Tool Tip",
                                      object_id=ObjectID(object_id='#everything_button', class_id=None))

        self.test_button_3 = UIButton(pygame.Rect((int(self.options.resolution[0] / 6),
                                                   int(self.options.resolution[1] * 0.90)),
                                                  (100, 40)),
                                      '|Scaling?',
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
        # self.test_text_entry.set_text_length_limit(3)
        self.test_text_entry.set_text('hello hello hello hello hello hello')

        current_resolution_string = (str(self.options.resolution[0]) +
                                     'x' +
                                     str(self.options.resolution[1]))
        self.test_drop_down = UIDropDownMenu(['640x480', '800x600', '1024x768'],
                                             current_resolution_string,
                                             pygame.Rect((int(self.options.resolution[0] / 2),
                                                          int(self.options.resolution[1] * 0.3)),
                                                         (200, 30)),
                                             self.ui_manager)

        self.test_drop_down_2 = UIDropDownMenu(['Penguins', 'drop down', 'menu',
                                                'testing', 'overlaps'],
                                               'Penguins',
                                               pygame.Rect((int(self.options.resolution[0] / 2),
                                                            int(self.options.resolution[1] * 0.22)),
                                                           (200, 30)),
                                               self.ui_manager)

        self.panel = UIPanel(pygame.Rect(50, 50, 200, 300),
                             starting_height=4,
                             manager=self.ui_manager)

        UIButton(pygame.Rect(10, 10, 174, 30), 'Panel Button',
                 manager=self.ui_manager,
                 container=self.panel)

        self.list = UISelectionList(pygame.Rect(10, 50, 174, 200),
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

        self.fps_counter = UILabel(pygame.Rect(self.options.resolution[0] - 250,
                                               20,
                                               230,
                                               44),
                                   "FPS: 0",
                                   self.ui_manager,
                                   object_id='#fps_counter')
        self.fps_counter.set_tooltip("The <b>F</b>rames <b>P</b>er <b>S</b>econd", wrap_width=200, delay=0.1)

        self.frame_timer = UILabel(pygame.Rect(self.options.resolution[0] - 250,
                                               64,
                                               230,
                                               24),
                                   "Frame time: 0",
                                   self.ui_manager,
                                   object_id='#frame_timer')

        self.disable_toggle = UIButton(pygame.Rect((int(self.options.resolution[0] * 0.85),
                                                    int(self.options.resolution[1] * 0.90)),
                                                   (100, 30)),
                                       'Disable',
                                       self.ui_manager,
                                       object_id='#disable_button')

        self.hide_toggle = UIButton(pygame.Rect((int(self.options.resolution[0] * 0.85),
                                                 int(self.options.resolution[1] * 0.85)),
                                                (100, 30)),
                                    'Hide',
                                    self.ui_manager,
                                    object_id='#hide_button')

    def create_message_window(self):
        self.button_response_timer.tick()
        self.message_window = UIMessageWindow(
            rect=pygame.Rect((random.randint(0, self.options.resolution[0] - 300),
                              random.randint(0, self.options.resolution[1] - 200)),
                             (300, 250)),
            window_title='Test Message Window',
            html_message='<font color=normal_text>'
                         'This is a <a href="test">test</a> message to see if '
                         'this box <a href=actually_link>actually</a> works. '
                         '<br>'
                         'In <i>bibendum</i> orci et velit</b> gravida lacinia.<br><br>'
                         'In hac a habitasse to platea dictumst.<br>'
                         '<font color=#4CD656 size=4>Vivamus I interdum mollis lacus nec '
                         'porttitor. <br>Morbi '
                         'accumsan, lectus at '
                         'tincidunt to dictum, neque <font color=#879AF6>erat tristique '
                         'blob</font>, '
                         'sed a tempus for <b>nunc</b> dolor in nibh.<br>'
                         'Suspendisse in viverra dui <i>fringilla dolor laoreet</i>, sit amet '
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
        # still feels a little slow, but it's better than it was.
        print("Time taken to create message window: " + str(time_taken))

    def check_resolution_changed(self):
        resolution_string = self.test_drop_down.selected_option[0].split('x')
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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                print("self.ui_manager.focused_set:", self.ui_manager.focused_set)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.list.add_items(['New Item'])

            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                print(event.text)

            if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                if event.link_target == 'test':
                    print("clicked test link")
                elif event.link_target == 'actually_link':
                    print("clicked actually link")

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.test_button:
                    self.test_button.set_text(random.choice(['', 'Hover me!',
                                                             'Click this',
                                                             'A Button']))
                    self.create_message_window()

                    if not self.test_text_entry.is_text_hidden:
                        self.test_text_entry.set_text_hidden(True)
                    else:
                        self.test_text_entry.set_text_hidden(False)

                if event.ui_element == self.test_button_3:
                    ScalingWindow(pygame.Rect((50, 50), (224, 224)), self.ui_manager)
                if event.ui_element == self.test_button_2:
                    EverythingWindow(pygame.Rect((10, 10), (640, 480)), self.ui_manager)

                if event.ui_element == self.disable_toggle:
                    if self.all_enabled:
                        self.disable_toggle.set_text('Enable')
                        self.all_enabled = False
                        self.ui_manager.root_container.disable()
                        self.disable_toggle.enable()
                        self.hide_toggle.enable()
                    else:
                        self.disable_toggle.set_text('Disable')
                        self.all_enabled = True
                        self.ui_manager.root_container.enable()

                if event.ui_element == self.hide_toggle:
                    if self.all_shown:
                        self.hide_toggle.set_text('Show')
                        self.all_shown = False
                        self.ui_manager.root_container.hide()
                        self.hide_toggle.show()
                    else:
                        self.hide_toggle.set_text('Hide')
                        self.all_shown = True
                        self.ui_manager.root_container.show()

            if (event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
                    and event.ui_element == self.test_drop_down):
                self.check_resolution_changed()

    def run(self):
        while self.running:
            time_delta = self.clock.tick() / 1000.0
            self.time_delta_stack.append(time_delta)
            if len(self.time_delta_stack) > 2000:
                self.time_delta_stack.popleft()

            # check for input
            self.process_events()

            # respond to input
            self.ui_manager.update(time_delta)

            if len(self.time_delta_stack) == 2000:
                self.fps_counter.set_text(
                    f'FPS: {min(999.0, 1.0/max(sum(self.time_delta_stack)/2000.0, 0.0000001)):.2f}')
                self.frame_timer.set_text(f'frame_time: {sum(self.time_delta_stack)/2000.0:.4f}')

            # draw graphics
            self.window_surface.blit(self.background_surface, (0, 0))

            # Debug stuff
            # chunk = self.test_slider.right_button.drawable_shape.text_box_layout.layout_rows[0].items[0]
            # pygame.draw.line(self.test_slider.right_button.image,
            #                  pygame.Color('#FFFFFF'),
            #                  self.test_slider.right_button.drawable_shape.text_box_layout.layout_rows[0].midleft,
            #                  self.test_slider.right_button.drawable_shape.text_box_layout.layout_rows[0].midright,#chunk.centering_rect,
            #                  1)

            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()


if __name__ == '__main__':
    app = OptionsUIApp()
    app.run()
