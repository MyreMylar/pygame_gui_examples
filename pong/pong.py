import pygame
from pygame.locals import *

from pong.wall import Wall
from pong.bat import Bat, ControlScheme
from pong.ball import Ball
from pong.score import Score


class PongGame:
    def __init__(self, size):
        self.background = pygame.Surface(size)  # make a background surface
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        font = pygame.font.Font(None, 24)

        self.score = Score(font)

        self.walls = [Wall((5, 5), (307, 10)),
                      Wall((5, 202), (307, 207))]

        self.bats = []

        control_scheme_1 = ControlScheme()
        control_scheme_1.up = K_w
        control_scheme_1.down = K_s

        control_scheme_2 = ControlScheme()
        control_scheme_2.up = K_UP
        control_scheme_2.down = K_DOWN

        self.bats.append(Bat((5, 141), control_scheme_1))
        self.bats.append(Bat((302, 141), control_scheme_2))

        self.ball = Ball((156, 106))

    def process_event(self, event):
        for bat in self.bats:
            bat.process_event(event)

    def update(self, time_delta):
        for bat in self.bats:
            bat.update(time_delta)

        self.ball.update(time_delta, self.bats, self.walls)

        if self.ball.position[0] < 0:
            self.ball.reset()
            self.score.increase_player_2_score()
        elif self.ball.position[0] > 312:
            self.ball.reset()
            self.score.increase_player_1_score()

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        for wall in self.walls:
            wall.render(surface)

        for bat in self.bats:
            bat.render(surface)

        self.ball.render(surface)
        self.score.render(surface)
