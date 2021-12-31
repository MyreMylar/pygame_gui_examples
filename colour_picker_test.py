import pygame
import pygame_gui

from pygame_gui.elements import UIButton
from pygame_gui.windows import UIColourPickerDialog


class ColourPickingApp:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Colour Picking App')
        self.window_surface = pygame.display.set_mode((800, 600))
        self.ui_manager = pygame_gui.UIManager((800, 600),
                                               'data/themes/colour_picker_app_theme.json')

        self.background = pygame.Surface((800, 600))
        self.background.fill(self.ui_manager.ui_theme.get_colour('dark_bg'))

        self.pick_colour_button = UIButton(relative_rect=pygame.Rect(-180, -60, 150, 30),
                                           text='Pick Colour',
                                           manager=self.ui_manager,
                                           anchors={'left': 'right',
                                                    'right': 'right',
                                                    'top': 'bottom',
                                                    'bottom': 'bottom'})

        self.colour_picker = None

        self.current_colour = pygame.Color(0, 0, 0)
        self.picked_colour_surface = pygame.Surface((400, 400))
        self.picked_colour_surface.fill(self.current_colour)

        self.clock = pygame.time.Clock()
        self.is_running = True

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == self.pick_colour_button):
                    self.colour_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                              self.ui_manager,
                                                              window_title='Change Colour...',
                                                              initial_colour=self.current_colour)
                    self.pick_colour_button.disable()

                if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                    self.current_colour = event.colour
                    self.picked_colour_surface.fill(self.current_colour)

                if (event.type == pygame_gui.UI_WINDOW_CLOSE and
                        event.ui_element == self.colour_picker):
                    self.pick_colour_button.enable()
                    self.colour_picker = None

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.window_surface.blit(self.picked_colour_surface, (200, 100))
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()


if __name__ == "__main__":
    app = ColourPickingApp()
    app.run()
