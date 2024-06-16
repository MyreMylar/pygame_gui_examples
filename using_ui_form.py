import pygame
import pygame_gui
from pygame_gui import UI_FORM_SUBMITTED
from pygame_gui.elements import UIButton, UIForm, UIDropDownMenu

pygame.init()

pygame.display.set_caption("UI Form Example")
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color("#000000"))

manager = pygame_gui.UIManager((800, 600))

test_rect = pygame.Rect(40, 50, 700, 500)

questionnaire = {
    "Just enter one character:": "character",
    "Perhaps some more text:": "short_text",
    "Or go wild!": "long_text",
    "how about a section?": {
        "do you like it?": "boolean",
        "well, here, section-ception": {
            "do you like it?": "boolean",
            "well, here, section-ception": {"finally...": "integer"},
        },
    },
    "Enter a float:": "decimal(default=0.01)",
    "You *must* enter something here:": "short_text('here', True)",
    "Let's make this form longer:": "long_text",
    "let's try a button": UIButton(pygame.Rect(100, 100, 100, 100), "button"),
    "Try entering a password!:": "password",
    "A dropdown appeared!": UIDropDownMenu(
        ["foo", "foo", "foo", "foo", "foo", "foo", "foo", "foo", "foo", "foo"],
        "foo",
        pygame.Rect(100, 100, 100, 100),
    ),
}
form_test = UIForm(test_rect, questionnaire, manager)

print(form_test.combined_element_ids)
print(form_test.get_container().combined_element_ids)
print(form_test.parsed_questionnaire["how about a section?"].combined_element_ids)
print(
    form_test.parsed_questionnaire["how about a section?"]
    .parsed_questionnaire["well, here, section-ception"]
    .combined_element_ids
)


clock = pygame.time.Clock()
is_running = True
pressed = False
element = None

while is_running:
    time_delta = clock.tick(30) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            print(event.ui_element.most_specific_combined_id)
            pressed = False
            element = None

        elif event.type == UI_FORM_SUBMITTED:
            print(event.form_values)

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))

    manager.draw_ui(window_surface)
    pygame.display.update()
