from typing import Union

import pygame
import pygame_gui

from pygame_gui.core.colour_gradient import ColourGradient

"""
Testing the quality of doing cheaper gradients.
"""


class Gradient:
    def __init__(self, angle_direction: int, colour_1: pygame.Color,
                 colour_2: pygame.Color, colour_3: Union[pygame.Color, None] = None):
        self.angle_direction = angle_direction
        self.colour_1 = colour_1
        self.colour_2 = colour_2
        self.colour_3 = colour_3

    def make_gradient(self, input_surface):
        inverse_rotated_input = pygame.transform.rotate(input_surface, -self.angle_direction)
        gradient_size = inverse_rotated_input.get_rect().size

        # create the initial 'pixel coloured' surface with a pixel for each colour
        if self.colour_3 is None:
            pixel_width = 2
            colour_pixels_surf = pygame.Surface((pixel_width, 1), flags=pygame.SRCALPHA)
            colour_pixels_surf.fill(self.colour_1, pygame.Rect((0, 0), (1, 1)))
            colour_pixels_surf.fill(self.colour_2, pygame.Rect((1, 0), (1, 1)))
        else:
            pixel_width = 3
            colour_pixels_surf = pygame.Surface((pixel_width, 1), flags=pygame.SRCALPHA)
            colour_pixels_surf.fill(self.colour_1, pygame.Rect((0, 0), (1, 1)))
            colour_pixels_surf.fill(self.colour_2, pygame.Rect((1, 0), (1, 1)))
            colour_pixels_surf.fill(self.colour_3, pygame.Rect((2, 0), (1, 1)))

        # create a surface large enough to overlap the input surface at any rotation angle
        gradient_surf = pygame.Surface(gradient_size, flags=pygame.SRCALPHA)

        # scale the pixel surface to fill our new large, gradient surface
        # pygame.transform.smoothscale Occasionally gives a
        # 'Fatal Python error: PyEval_SaveThread: NULL tstate'
        # which is apparently a threading issue with the GIL.

        # pygame.transform.smoothscale(colour_pixels_surf, gradient_size, gradient_surf)

        # Try this instead
        scale = float(max(gradient_size[0] / pixel_width, gradient_size[1]))
        zoomed_surf = pygame.transform.rotozoom(colour_pixels_surf, 0, scale)
        pygame.transform.scale(zoomed_surf, gradient_size, gradient_surf)

        # rotate the gradient surface to the correct angle for our gradient
        gradient_surf = pygame.transform.rotate(gradient_surf, self.angle_direction)
        return gradient_surf

    def make_gradient_2(self, input_surface):
        if self.colour_3 is None:
            pixel_width = 2
            colour_pixels_surf = pygame.Surface((pixel_width, 1), flags=pygame.SRCALPHA)
            colour_pixels_surf.fill(self.colour_1, pygame.Rect((0, 0), (1, 1)))
            colour_pixels_surf.fill(self.colour_2, pygame.Rect((1, 0), (1, 1)))
        else:
            pixel_width = 3
            colour_pixels_surf = pygame.Surface((pixel_width, 1), flags=pygame.SRCALPHA)
            colour_pixels_surf.fill(self.colour_1, pygame.Rect((0, 0), (1, 1)))
            colour_pixels_surf.fill(self.colour_2, pygame.Rect((1, 0), (1, 1)))
            colour_pixels_surf.fill(self.colour_3, pygame.Rect((2, 0), (1, 1)))

        gradient = pygame.transform.rotozoom(colour_pixels_surf, 0, 30)

        # scale the gradient up to the right size
        inverse_rotated_input = pygame.transform.rotate(input_surface, -self.angle_direction)
        gradient_size = inverse_rotated_input.get_rect().size
        gradient_surf = pygame.Surface(gradient_size, flags=pygame.SRCALPHA)

        pygame.transform.scale(gradient, gradient_size, gradient_surf)
        gradient_surf = pygame.transform.rotate(gradient_surf, self.angle_direction)

        return gradient_surf


pygame.init()


pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/quick_theme.json')

background = pygame.Surface((800, 600))
background.fill(manager.get_theme().get_colour('dark_bg'))

test_gradient_1 = ColourGradient(-90, pygame.Color("#FF0000"), pygame.Color("#FF80FF"))

long_thin_surf = pygame.Surface((300, 25))
long_thin_surf.fill("white")
test_gradient_1.apply_gradient_to_surface(long_thin_surf)

tall_thin_surf = pygame.Surface((25, 300))
tall_thin_surf.fill("white")
test_gradient_1.apply_gradient_to_surface(tall_thin_surf)

big_surf = pygame.Surface((300, 300))
big_surf.fill("white")
test_gradient_1.apply_gradient_to_surface(big_surf, pygame.Rect(0, 0, 150, 150))


# gradient 2

test_gradient_2 = Gradient(45,
                           pygame.Color("#8070A0"),
                           pygame.Color("#80E0CF"),
                           pygame.Color("#F0E0EF"))

long_thin_surf_2 = pygame.Surface((300, 25))
long_thin_surf_2 = test_gradient_2.make_gradient_2(long_thin_surf_2)

tall_thin_surf_2 = pygame.Surface((25, 300))
tall_thin_surf_2 = test_gradient_2.make_gradient_2(tall_thin_surf_2)

big_surf_2 = pygame.Surface((300, 300))
big_surf_2 = test_gradient_2.make_gradient_2(big_surf_2)

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

    window_surface.blit(long_thin_surf, (10, 10))
    window_surface.blit(tall_thin_surf, (350, 10))
    window_surface.blit(big_surf, (10, 50))

    window_surface.blit(long_thin_surf_2, (400, 10))
    window_surface.blit(tall_thin_surf_2, (750, 10))
    window_surface.blit(big_surf_2, (360, 50))

    pygame.display.update()
