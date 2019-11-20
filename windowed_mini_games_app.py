import pygame
from pygame_gui.ui_manager import UIManager
from pygame_gui.core.ui_window import UIWindow
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_image import UIImage

from pong.pong import PongGame


class PongWindow(UIWindow):
    def __init__(self, position, ui_manager):
        super().__init__(pygame.Rect(position, (320, 240)), ui_manager, ['pong_window'])

        self.bg_colour = self.ui_manager.get_theme().get_colour(self.object_ids, self.element_ids, 'dark_bg')

        # create shadow
        shadow_width = 15
        shadow_padding = (shadow_width, shadow_width)
        background_surface = pygame.Surface((self.rect.width - shadow_padding[0] * 2,
                                             self.rect.height - shadow_padding[1] * 2))
        background_surface.fill(self.bg_colour)

        self.image = self.ui_manager.get_shadow(self.rect.size, shadow_width, corner_radius=shadow_width)
        self.image.blit(background_surface, shadow_padding)

        self.get_container().relative_rect.width = self.rect.width - shadow_padding[0] * 2
        self.get_container().relative_rect.height = self.rect.height - shadow_padding[1] * 2
        self.get_container().rect.width = self.rect.width - shadow_padding[0] * 2
        self.get_container().rect.height = self.rect.height - shadow_padding[1] * 2
        self.get_container().relative_rect.x = self.get_container().relative_rect.x + shadow_padding[0]
        self.get_container().relative_rect.y = self.get_container().relative_rect.y + shadow_padding[1]
        self.get_container().update_containing_rect_position()

        self.menu_bar = UIButton(relative_rect=pygame.Rect((0, 0),
                                                           ((self.rect.width - shadow_padding[0] * 2) - 20, 20)),
                                 text='Super Awesome Pong!',
                                 manager=ui_manager,
                                 container=self.get_container(),
                                 parent_element=self,
                                 object_id='#menu_bar'
                                 )
        self.menu_bar.set_hold_range((100, 100))

        self.grabbed_window = False
        self.starting_grab_difference = (0, 0)

        self.close_window_button = UIButton(relative_rect=pygame.Rect(((self.rect.width - shadow_padding[0] * 2) - 20,
                                                                       0),
                                                                      (20, 20)),
                                            text='╳',
                                            manager=ui_manager,
                                            container=self.get_container(),
                                            parent_element=self
                                            )

        game_surface_size = (self.get_container().rect.width - 4, self.get_container().rect.height - 24)
        self.game_surface_element = UIImage(pygame.Rect((2, 22),
                                                        game_surface_size),
                                            pygame.Surface(game_surface_size).convert(),
                                            manager=ui_manager,
                                            container=self.get_container(),
                                            parent_element=self)

        self.pong_game = PongGame(game_surface_size)

        self.is_active = False

    def process_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == 'ui_button_pressed':
                if event.ui_element == self.menu_bar:
                    window_selected_event = pygame.event.Event(pygame.USEREVENT,
                                                              {'user_type': 'pong_window_selected',
                                                               'ui_element': self,
                                                               'ui_object_id': self.object_ids[-1]})
                    pygame.event.post(window_selected_event)
        if self.is_active:
            self.pong_game.process_event(event)

    def update(self, time_delta):
        if self.alive():

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

            if not self.grabbed_window and self.is_active:
                self.pong_game.update(time_delta)

            if self.close_window_button.check_pressed():
                self.kill()

        super().update(time_delta)

        self.pong_game.draw(self.game_surface_element.image)


class MiniGamesApp:
    def __init__(self):
        pygame.init()

        self.root_window_surface = pygame.display.set_mode((1024, 600))

        self.background_surface = pygame.Surface((1024, 600)).convert()
        self.background_surface.fill(pygame.Color('#505050'))
        self.ui_manager = UIManager((1024, 600), 'data/themes/theme_3.json')
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.pong_window_1 = PongWindow((25, 25), self.ui_manager)
        self.pong_window_2 = PongWindow((50, 50), self.ui_manager)

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                self.ui_manager.process_events(event)

                if event.type == pygame.USEREVENT:
                    if event.user_type == 'pong_window_selected':
                        event.ui_element.is_active = True
                        if event.ui_element == self.pong_window_1:
                            self.pong_window_2.is_active = False
                        elif event.ui_element == self.pong_window_2:
                            self.pong_window_1.is_active = False

            self.ui_manager.update(time_delta)

            self.root_window_surface.blit(self.background_surface, (0, 0))
            self.ui_manager.draw_ui(self.root_window_surface)

            pygame.display.update()


if __name__ == '__main__':
    app = MiniGamesApp()
    app.run()
