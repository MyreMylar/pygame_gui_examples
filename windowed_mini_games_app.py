import pygame
import pygame_gui

from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_image import UIImage

from pong.pong import PongGame

PONG_WINDOW_SELECTED = pygame.event.custom_type()


class PongWindow(UIWindow):
    def __init__(self, position, ui_manager):
        super().__init__(pygame.Rect(position, (320, 240)), ui_manager,
                         window_display_title='Super Awesome Pong!',
                         object_id='#pong_window')

        game_surface_size = self.get_container().get_size()
        self.game_surface_element = UIImage(pygame.Rect((0, 0),
                                                        game_surface_size),
                                            pygame.Surface(game_surface_size).convert(),
                                            manager=ui_manager,
                                            container=self,
                                            parent_element=self)

        self.pong_game = PongGame(game_surface_size)

        self.is_active = False

    def process_event(self, event):
        handled = super().process_event(event)
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == "#pong_window.#title_bar" and
                event.ui_element == self.title_bar):
            handled = True
            event_data = {'ui_element': self,
                          'ui_object_id': self.most_specific_combined_id}
            window_selected_event = pygame.event.Event(PONG_WINDOW_SELECTED,
                                                       event_data)
            pygame.event.post(window_selected_event)
        if self.is_active:
            handled = self.pong_game.process_event(event)
        return handled

    def update(self, time_delta):
        if self.alive() and self.is_active:
            self.pong_game.update(time_delta)

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

                if event.type == PONG_WINDOW_SELECTED:
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
