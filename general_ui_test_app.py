import pygame
import random

from pygame_gui.ui_manager import UIManager

from pygame_gui.core.ui_window import UIWindow

from pygame_gui.windows.ui_message_window import UIMessageWindow

from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_horizontal_slider import UIHorizontalSlider
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu
from pygame_gui.elements.ui_screen_space_health_bar import UIScreenSpaceHealthBar
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_image import UIImage


class EverythingWindow(UIWindow):
    def __init__(self, rect, ui_manager):

        element_ids = ['everything_window']

        super().__init__(rect, ui_manager, element_ids=element_ids)

        # create shadow
        shadow_padding = (2, 2)
        background_surface = pygame.Surface((self.rect.width - shadow_padding[0] * 2,
                                             self.rect.height - shadow_padding[1] * 2))
        background_surface.fill(self.ui_manager.get_theme().get_colour(self.object_id, self.element_ids, 'dark_bg'))
        self.image = self.ui_manager.get_shadow(self.rect.size)
        self.image.blit(background_surface, shadow_padding)

        self.get_container().relative_rect.width = self.rect.width - shadow_padding[0] * 2
        self.get_container().relative_rect.height = self.rect.height - shadow_padding[1] * 2
        self.get_container().relative_rect.x = self.get_container().relative_rect.x + shadow_padding[0]
        self.get_container().relative_rect.y = self.get_container().relative_rect.y + shadow_padding[1]
        self.get_container().update_containing_rect_position()

        self.close_window_button = UIButton(relative_rect=pygame.Rect((self.get_container().rect.width-20, 0),
                                                                      (20, 20)),
                                            text='╳',
                                            ui_manager=ui_manager,
                                            ui_container=self.get_container()
                                            )
        self.menu_bar = UIButton(relative_rect=pygame.Rect((0, 0),
                                                           (self.get_container().rect.width-20, 20)),
                                 text='Everything Container',
                                 ui_manager=ui_manager,
                                 ui_container=self.get_container(),
                                 object_id='#message_window_title_bar'
                                 )
        self.menu_bar.set_hold_range((100, 100))

        self.grabbed_window = False
        self.starting_grab_difference = (0, 0)

        self.test_slider = UIHorizontalSlider(pygame.Rect((self.rect.width / 2,
                                                           self.rect.height * 0.70),
                                                          (240, 20)),
                                              50.0,
                                              (0.0, 100.0),
                                              self.ui_manager,
                                              ui_container=self.get_container())

        self.slider_label = UILabel(pygame.Rect(((self.rect.width / 2) + 250,
                                                 self.rect.height * 0.70),
                                                (24, 20)),
                                    str(int(self.test_slider.get_current_value())),
                                    self.ui_manager,
                                    ui_container=self.get_container())

        self.test_text_entry = UITextEntryLine(pygame.Rect((self.rect.width / 2,
                                                            self.rect.height * 0.50),
                                                           (200.0, -1)),
                                               self.ui_manager,
                                               ui_container=self.get_container())

        current_resolution_string = 'Item 1'
        self.test_drop_down_menu = UIDropDownMenu(['Item 1',
                                                   'Item 2',
                                                   'Item 3',
                                                   'Item 4',
                                                   'Item 5',
                                                   'Item 6'],
                                                  current_resolution_string,
                                                  pygame.Rect((self.rect.width / 2,
                                                               self.rect.height * 0.3),
                                                              (200.0, 20)),
                                                  self.ui_manager,
                                                  ui_container=self.get_container())

        self.health_bar = UIScreenSpaceHealthBar(pygame.Rect((self.rect.width / 9,
                                                              self.rect.height * 0.7),
                                                             (200.0, 20)),
                                                 self.ui_manager,
                                                 ui_container=self.get_container())

        loaded_test_image = pygame.image.load('data/images/splat.png').convert_alpha()

        self.test_image = UIImage(pygame.Rect((self.rect.width / 9,
                                               self.rect.height * 0.3),
                                              loaded_test_image.get_rect().size),
                                  loaded_test_image, self.ui_manager,
                                  ui_container=self.get_container())
        self.is_selected = False

    def select(self):
        self.is_selected = True

    def unselect(self):
        self.is_selected = False

    def process_event(self, event):
        processed_event = False
        if self.is_selected:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.test_slider.set_current_value(50)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if self.rect.collidepoint(mouse_x, mouse_y):
                    processed_event = True
                    self.window_stack.move_window_to_front(self)

        return processed_event

    def update(self, time_delta):
        if self.alive():
            if self.test_slider.has_moved_recently:
                self.slider_label.set_text(str(int(self.test_slider.get_current_value())))

            if self.menu_bar.held:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if not self.grabbed_window:
                    self.window_stack.move_window_to_front(self)
                    self.grabbed_window = True
                    self.starting_grab_difference = (mouse_x - self.rect.x,
                                                     mouse_y - self.rect.y)

                current_grab_difference = (mouse_x - self.rect.x,
                                           mouse_y - self.rect.y)

                adjustment_required = (current_grab_difference[0] - self.starting_grab_difference[0],
                                       current_grab_difference[1] - self.starting_grab_difference[1])

                self.rect.x += adjustment_required[0]
                self.rect.y += adjustment_required[1]
                self.get_container().relative_rect.x += adjustment_required[0]
                self.get_container().relative_rect.y += adjustment_required[1]
                self.get_container().update_containing_rect_position()

            else:
                self.grabbed_window = False

            if self.close_window_button.check_pressed_and_reset():
                self.kill()

        super().update(time_delta)


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
            self.window_surface = pygame.display.set_mode(self.options.resolution, pygame.FULLSCREEN)
        else:
            self.window_surface = pygame.display.set_mode(self.options.resolution)

        self.background_surface = None

        self.ui_manager = UIManager(self.options.resolution, 'data/themes/theme_2.json')
        self.ui_manager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
                                       {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
                                       {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
                                       {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
                                       {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
                                       ])

        self.test_button = None
        self.test_button_2 = None
        self.test_slider = None
        self.test_text_entry = None
        self.test_drop_down_menu = None
        self.recreate_ui()

        self.clock = pygame.time.Clock()
        self.running = True

    def recreate_ui(self):
        self.ui_manager.set_window_resolution(self.options.resolution)
        self.ui_manager.clear_and_reset()

        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(pygame.Color("#daaef9"))

        self.test_button = UIButton(pygame.Rect((self.options.resolution[0] / 2,
                                                 self.options.resolution[1] * 0.90),
                                                (100, 40)),
                                    'Hover me!',
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

        self.test_button_2 = UIButton(pygame.Rect((self.options.resolution[0] / 3,
                                                   self.options.resolution[1] * 0.90),
                                                  (100, 40)),
                                      'EVERYTHING',
                                      self.ui_manager)

        self.test_slider = UIHorizontalSlider(pygame.Rect((self.options.resolution[0] / 2,
                                                           self.options.resolution[1] * 0.70),
                                                          (240, 20)),
                                              100.0,
                                              (0.0, 100.0),
                                              self.ui_manager,
                                              object_id='#cool_slider')

        self.test_text_entry = UITextEntryLine(pygame.Rect((self.options.resolution[0] / 2,
                                                            self.options.resolution[1] * 0.50),
                                                           (200.0, -1)),
                                               self.ui_manager)

        current_resolution_string = str(self.options.resolution[0]) + 'x' + str(self.options.resolution[1])
        self.test_drop_down_menu = UIDropDownMenu(['640x480', '800x600', '1024x768'],
                                                  current_resolution_string,
                                                  pygame.Rect((self.options.resolution[0] / 2,
                                                               self.options.resolution[1] * 0.3),
                                                              (200.0, 20)),
                                                  self.ui_manager)

    def check_links(self):
        message_boxes = [sprite for sprite in self.ui_manager.ui_group.sprites()
                         if 'message_window' in sprite.element_ids]
        for message_window in message_boxes:
            if hasattr(message_window, 'text_block'):
                clicked_links = message_window.text_block.get_clicked_link_targets_and_reset()
                if 'test' in clicked_links:
                    print("clicked test link")
                if 'actually_link' in clicked_links:
                    print("clicked actually link")

    def check_test_button_pressed(self):
        if self.test_button.check_pressed_and_reset():
            UIMessageWindow(pygame.Rect((random.randint(0, self.options.resolution[0]-300),
                                         random.randint(0, self.options.resolution[1]-200)),
                                        (300, 200)),
                            'Test Message Window',
                            '<font color=normal_text>'
                            'This is a <a href="test">test</a> message to see if '
                            'this box <a href=actually_link>actually</a> works.'
                            ''
                            'In <i>bibendum</i> orci et velit</b> gravida lacinia.<br><br><br> '
                            'In hac a habitasse to platea dictumst.<br>'
                            ' <font color=#4CD656 size=4>Vivamus I interdum mollis lacus nec porttitor.<br> Morbi'
                            ' accumsan, lectus at'
                            ' tincidunt to dictum, neque <font color=#879AF6>erat tristique blob</font>,'
                            ' sed a tempus for <b>nunc</b> dolor in nibh.<br>'
                            ' Suspendisse in viverra dui <i>fringilla dolor laoreet</i>, sit amet on pharetra a ante'
                            ' sollicitudin.</font>'
                            '<br><br>'
                            'In <i>bibendum</i> orci et velit</b> gravida lacinia.<br><br><br> '
                            'In hac a habitasse to platea dictumst.<br>'
                            ' <font color=#4CD656 size=4>Vivamus I interdum mollis lacus nec porttitor.<br> Morbi'
                            ' accumsan, lectus at'
                            ' tincidunt to dictum, neque <font color=#879AF6>erat tristique erat</font>,'
                            ' sed a tempus for <b>nunc</b> dolor in nibh.<br>'
                            ' Suspendisse in viverra dui <i>fringilla dolor laoreet</i>, sit amet on pharetra a ante'
                            ' sollicitudin.</font>'
                            '<br><br>'
                            'In <i>bibendum</i> orci et velit</b> gravida lacinia.<br><br><br> '
                            'In hac a habitasse to platea dictumst.<br>'
                            ' <font color=#4CD656 size=4>Vivamus I interdum mollis lacus nec porttitor.<br> Morbi'
                            ' accumsan, lectus at'
                            ' tincidunt to dictum, neque <font color=#879AF6>erat tristique erat</font>,'
                            ' sed a tempus for <b>nunc</b> dolor in nibh.<br>'
                            ' Suspendisse in viverra dui <i>fringilla dolor laoreet</i>, sit amet on pharetra a ante'
                            ' sollicitudin.</font>'
                            '</font>',
                            self.ui_manager)

        if self.test_button_2.check_pressed_and_reset():
            EverythingWindow(pygame.Rect((10, 10), (640, 480)), self.ui_manager)

    def check_resolution_changed(self):
        resolution_string = self.test_drop_down_menu.selected_option.split('x')
        resolution_width = int(resolution_string[0])
        resolution_height = int(resolution_string[1])
        if resolution_width != self.options.resolution[0] or resolution_height != self.options.resolution[1]:
            self.options.resolution = (resolution_width, resolution_height)
            self.window_surface = pygame.display.set_mode(self.options.resolution)
            self.recreate_ui()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui_manager.process_events(event)

    def run(self):
        while self.running:
            time_delta = self.clock.tick(60)/1000.0

            # check for input
            self.process_events()

            # respond to input
            self.ui_manager.update(time_delta)
            self.check_resolution_changed()
            self.check_test_button_pressed()

            self.check_links()

            # draw graphics
            self.window_surface.blit(self.background_surface, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()


if __name__ == '__main__':
    app = OptionsUIApp()
    app.run()
