import pygame
import pygame_gui

from pygame_gui.elements import UIButton, UIImage
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path


class ImageLoadApp:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Image Load App')
        self.window_surface = pygame.display.set_mode((800, 600))
        self.ui_manager = pygame_gui.UIManager((800, 600), 'data/themes/image_load_app_theme.json')

        self.background = pygame.Surface((800, 600))
        self.background.fill(self.ui_manager.ui_theme.get_colour('dark_bg'))

        self.load_button = UIButton(relative_rect=pygame.Rect(-180, -60, 150, 30),
                                    text='Load Image',
                                    manager=self.ui_manager,
                                    anchors={'left': 'right',
                                             'right': 'right',
                                             'top': 'bottom',
                                             'bottom': 'bottom'})

        self.file_dialog = None

        # scale images, if necessary so that their largest dimension does not exceed these values
        self.max_image_display_dimensions = (400, 400)
        self.display_loaded_image = None

        self.clock = pygame.time.Clock()
        self.is_running = True

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == self.load_button):
                    self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                                    self.ui_manager,
                                                    window_title='Load Image...',
                                                    initial_file_path='data/images/',
                                                    allow_picking_directories=True,
                                                    allow_existing_files_only=True,
                                                    allowed_suffixes={""})
                    self.load_button.disable()

                if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                    if self.display_loaded_image is not None:
                        self.display_loaded_image.kill()

                    try:
                        image_path = create_resource_path(event.text)
                        loaded_image = pygame.image.load(image_path).convert_alpha()
                        image_rect = loaded_image.get_rect()
                        aspect_ratio = image_rect.width / image_rect.height
                        need_to_scale = False
                        if image_rect.width > self.max_image_display_dimensions[0]:
                            image_rect.width = self.max_image_display_dimensions[0]
                            image_rect.height = int(image_rect.width / aspect_ratio)
                            need_to_scale = True

                        if image_rect.height > self.max_image_display_dimensions[1]:
                            image_rect.height = self.max_image_display_dimensions[1]
                            image_rect.width = int(image_rect.height * aspect_ratio)
                            need_to_scale = True

                        if need_to_scale:
                            loaded_image = pygame.transform.smoothscale(loaded_image,
                                                                        image_rect.size)

                        image_rect.center = (400, 300)

                        self.display_loaded_image = UIImage(relative_rect=image_rect,
                                                            image_surface=loaded_image,
                                                            manager=self.ui_manager)

                    except pygame.error:
                        pass

                if (event.type == pygame_gui.UI_WINDOW_CLOSE
                        and event.ui_element == self.file_dialog):
                    self.load_button.enable()
                    self.file_dialog = None

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()


if __name__ == "__main__":
    app = ImageLoadApp()
    app.run()
