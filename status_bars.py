import pygame
import pygame_gui
from pygame_gui.core import ObjectID


class HappySprite(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)

        self.image = pygame.image.load('data/images/test_emoji.png')

        self.position = pygame.Vector2(200.0, 300.0)
        self.rect = self.image.get_rect()
        self.rect.topleft = (200, 300)

        self.max_health = 100
        self.current_health = 75

        self.max_mana = 100
        self.current_mana = 30

        self.max_stamina = 100.0
        self.current_stamina = 100.0

        self.speed = 100.0
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

        self.stam_recharge_tick = 0.05
        self.stam_recharge_acc = 0.0

    def get_health_percentage(self) -> float:
        return self.current_health/self.max_health

    def get_mana_percentage(self) -> float:
        return self.current_mana/self.max_mana

    def get_stamina_percentage(self) -> float:
        return self.current_stamina/self.max_stamina

    def update(self, time_delta_secs: float) -> None:

        if self.moving_left:
            self.position.x -= self.speed * time_delta_secs
            self.current_stamina -= 0.4
        if self.moving_right:
            self.position.x += self.speed * time_delta_secs
            self.current_stamina -= 0.4
        if self.moving_up:
            self.position.y -= self.speed * time_delta_secs
            self.current_stamina -= 0.4
        if self.moving_down:
            self.position.y += self.speed * time_delta_secs
            self.current_stamina -= 0.4

        self.current_stamina = max(self.current_stamina, 0)

        if self.current_stamina < self.max_stamina:
            self.stam_recharge_acc += time_delta_secs
            if self.stam_recharge_acc >= self.stam_recharge_tick:
                self.current_stamina += 1
                self.stam_recharge_acc = 0.0

        self.current_stamina = min(self.current_stamina, self.max_stamina)

        self.rect.topleft = (int(self.position.x), int(self.position.y))


pygame.init()


pygame.display.set_caption('Status Bars')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/status_bar_theme.json')

background = pygame.Surface((800, 600))
background.fill(manager.ui_theme.get_colour('dark_bg'))

sprite_list = pygame.sprite.Group()
happy_sprite = HappySprite(sprite_list)


progress_bar = pygame_gui.elements.UIStatusBar(pygame.Rect((100, 100), (200, 30)),
                                               manager,
                                               None,
                                               object_id=ObjectID('#progress_bar', '@UIStatusBar'))

health_bar = pygame_gui.elements.UIStatusBar(pygame.Rect((0, 30), (50, 6)),
                                             manager,
                                             sprite=happy_sprite,
                                             percent_method=happy_sprite.get_health_percentage,
                                             object_id=ObjectID(
                                                 '#health_bar', '@player_status_bars'))
mana_bar = pygame_gui.elements.UIStatusBar(pygame.Rect((0, 40), (50, 6)),
                                           manager,
                                           sprite=happy_sprite,
                                           percent_method=happy_sprite.get_mana_percentage,
                                           object_id=ObjectID(
                                                 '#mana_bar', '@player_status_bars'))
stamina_bar = pygame_gui.elements.UIStatusBar(pygame.Rect((0, 50), (50, 6)),
                                              manager,
                                              sprite=happy_sprite,
                                              percent_method=happy_sprite.get_stamina_percentage,
                                              object_id=ObjectID(
                                                  '#stamina_bar', '@player_status_bars'))

progress = 0
time_acc = 0
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                happy_sprite.moving_left = True
            if event.key == pygame.K_RIGHT:
                happy_sprite.moving_right = True
            if event.key == pygame.K_UP:
                happy_sprite.moving_up = True
            if event.key == pygame.K_DOWN:
                happy_sprite.moving_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                happy_sprite.moving_left = False
            if event.key == pygame.K_RIGHT:
                happy_sprite.moving_right = False
            if event.key == pygame.K_UP:
                happy_sprite.moving_up = False
            if event.key == pygame.K_DOWN:
                happy_sprite.moving_down = False

        manager.process_events(event)

    sprite_list.update(time_delta)
    manager.update(time_delta)

    time_acc += time_delta
    progress = (time_acc/10.0)
    if progress > 1.0:
        time_acc = 0.0
    progress_bar.percent_full = progress

    window_surface.blit(background, (0, 0))
    sprite_list.draw(window_surface)
    manager.draw_ui(window_surface)

    pygame.display.update()
