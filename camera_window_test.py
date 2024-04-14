import pygame
import pygame.camera
import pygame_gui


"""
Uses Pygame Camera module to display a webcam in a window 
"""


class CameraWindow(pygame_gui.elements.UIWindow):
    def __init__(self,
                 rect: pygame.Rect,
                 camera_name,
                 ui_manager: pygame_gui.core.interfaces.IUIManagerInterface):
        super().__init__(rect, ui_manager, window_display_title=camera_name, resizable=True)

        self.camera = None

        self.camera = pygame.camera.Camera(camera_name, (640, 480))
        self.camera.start()

        print(self.camera.get_controls())

        cam_rect = pygame.Rect((0, 0), self.get_container().rect.size)
        self.cam_image = pygame_gui.elements.UIImage(relative_rect=cam_rect,
                                                     image_surface=self.camera.get_image(),
                                                     manager=self.ui_manager,
                                                     container=self,
                                                     anchors={'left': 'left',
                                                              'right': 'right',
                                                              'top': 'top',
                                                              'bottom': 'bottom'})

    def update(self, time_delta: float):
        super().update(time_delta)

        if self.camera is not None:

            self.cam_image.set_image(pygame.transform.smoothscale(self.camera.get_image(),
                                                                  self.get_container().rect.size))


pygame.init()
pygame.camera.init()

print(pygame.camera.get_backends())
print(pygame.camera.list_cameras())

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/camera_theme.json')

background = pygame.Surface((800, 600))
background.fill(manager.ui_theme.get_colour('dark_bg'))


cam_window_pos = [10, 10]
num_connected_cameras = 1
cam_names = pygame.camera.list_cameras()
for cam_name in cam_names:
    cam_window_rect = pygame.Rect(0, 0, 400, 300)
    cam_window_rect.topleft = cam_window_pos
    CameraWindow(cam_window_rect, cam_name, manager)
    cam_window_pos = (cam_window_pos[0] + 420,
                      cam_window_pos[1])

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
