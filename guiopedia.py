import re
from collections import OrderedDict
from os import listdir, linesep
from os.path import isfile, join, basename, splitext

import pygame
import pygame_gui


class GUIopediaWindow(pygame_gui.core.UIWindow):
    def __init__(self, manager):
        super().__init__(pygame.Rect((200, 50), (400, 500)), manager, ['guiopedia_window'])

        self.bg_colour = self.ui_manager.get_theme().get_colour(self.object_ids, self.element_ids, 'normal_bg')
        # create shadow
        shadow_padding = (2, 2)
        background_surface = pygame.Surface((self.rect.width - shadow_padding[0] * 2,
                                             self.rect.height - shadow_padding[1] * 2))
        background_surface.fill(self.bg_colour)
        self.image = self.ui_manager.get_shadow(self.rect.size)
        self.image.blit(background_surface, shadow_padding)

        self.get_container().relative_rect.width = self.rect.width - shadow_padding[0] * 2
        self.get_container().relative_rect.height = self.rect.height - shadow_padding[1] * 2
        self.get_container().relative_rect.x = self.get_container().relative_rect.x + shadow_padding[0]
        self.get_container().relative_rect.y = self.get_container().relative_rect.y + shadow_padding[1]
        self.get_container().update_containing_rect_position()

        self.menu_bar = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0),
                                                                               ((self.rect.width - shadow_padding[
                                                                                   0] * 2) - 28, 28)),
                                                     text='GUIopedia!',
                                                     manager=manager,
                                                     container=self.get_container(),
                                                     parent_element=self,
                                                     object_id='#menu_bar'
                                                     )
        self.menu_bar.set_hold_range((100, 100))

        self.grabbed_window = False
        self.starting_grab_difference = (0, 0)

        self.close_window_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(((self.rect.width - shadow_padding[0] * 2) - 28,
                                       0),
                                      (28, 28)),
            text='╳',
            manager=manager,
            container=self.get_container(),
            parent_element=self,
            object_id='#menu_bar_close_button'
        )

        self.window_border = [4, 4]

        search_bar_y_start = self.window_border[1] + self.menu_bar.rect.height
        self.search_box = pygame_gui.elements.UITextEntryLine(pygame.Rect((150, search_bar_y_start),
                                                                          (240, 20)),
                                                              manager=manager,
                                                              container=self.get_container(),
                                                              parent_element=self)

        self.search_label = pygame_gui.elements.UILabel(pygame.Rect((90, search_bar_y_start),
                                                                    (56, self.search_box.rect.height)),
                                                        "Search:",
                                                        manager=manager,
                                                        container=self.get_container(),
                                                        parent_element=self)

        self.home_button = pygame_gui.elements.UIButton(pygame.Rect((20, search_bar_y_start),
                                                                    (20, 20)),
                                                        '',
                                                        manager=manager,
                                                        container=self.get_container(),
                                                        parent_element=self,
                                                        object_id='#home_button')

        self.remaining_window_size = (self.get_container().rect.width - (2 * self.window_border[0]),
                                      self.get_container().rect.height - self.menu_bar.rect.height - (
                                              3 * self.window_border[1]) - self.search_box.rect.height)

        self.pages = {}
        page_path = 'data/guiopedia/'
        file_paths = [join(page_path, f) for f in listdir(page_path) if isfile(join(page_path, f))]
        for file_path in file_paths:
            with open(file_path, 'r') as page_file:
                file_id = splitext(basename(file_path))[0]
                file_data = ""
                for line in page_file:
                    line = line.rstrip(linesep).lstrip()
                    # kind of hacky way to add back spaces at the end of new lines that are removed by the pyCharm HTML
                    # editor. perhaps our HTML parser needs to handle this case (turning new lines into spaces
                    # but removing spaces at the start of rendered lines?)
                    if len(line) > 0:
                        if line[-1] != '>':
                            line += ' '
                        file_data += line
                self.pages[file_id] = file_data

        index_page = self.pages['index']
        self.page_y_start_pos = (2 * self.window_border[1]) + self.search_box.rect.height + self.menu_bar.rect.height
        self.page_display = pygame_gui.elements.UITextBox(index_page, pygame.Rect((self.window_border[0],
                                                                                   self.page_y_start_pos),
                                                                                  self.remaining_window_size),
                                                          manager=manager,
                                                          container=self.get_container(),
                                                          parent_element=self)

    def process_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == 'ui_text_box_link_clicked':
                self.open_new_page(event.link_target)

            if event.user_type == 'ui_text_entry_finished':
                if event.ui_element == self.search_box:
                    results = self.search_pages(event.text)
                    self.create_search_results_page(results)
                    self.open_new_page('results')

            if event.user_type == 'ui_button_pressed':
                if event.ui_object_id == '#home_button':
                    self.open_new_page('index')

    def search_pages(self, search_string: str):
        results = {}
        words = search_string.split()

        for page in self.pages.keys():
            total_occurances_of_search_words = 0
            for word in words:
                word_occurances = self.search_text_for_occurrences_of_word(word, self.pages[page])
                total_occurances_of_search_words += word_occurances
            if total_occurances_of_search_words > 0:
                results[page] = total_occurances_of_search_words

        sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
        return OrderedDict(sorted_results)

    @staticmethod
    def search_text_for_occurrences_of_word(word_to_search_for: str, text_to_search: str) -> int:
        count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word_to_search_for),
                                           text_to_search,
                                           flags=re.IGNORECASE))
        return count

    def open_new_page(self, page_link: str):
        self.page_display.kill()
        self.page_display = None
        if page_link in self.pages:
            text = self.pages[page_link]

            self.page_display = pygame_gui.elements.UITextBox(text, pygame.Rect((self.window_border[0],
                                                                                 self.page_y_start_pos),
                                                                                self.remaining_window_size),
                                                              manager=self.ui_manager,
                                                              container=self.get_container(),
                                                              parent_element=self)

    def create_search_results_page(self, results):
        results_text = '<font size=5>Search results</font>'
        if len(results) == 0:
            results_text += '<br><br> No Results Found.'
        else:
            results_text += '<br><br>' + str(len(results)) + ' results found:'
            for result in results.keys():
                results_text += '<br><br> - <a href=\"' + result + '\">' + result + '</a>'

        self.pages['results'] = results_text

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

            if self.close_window_button.check_pressed():
                self.kill()

        super().update(time_delta)


class GUIopediaApp:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('GUIopedia App')
        self.window_surface = pygame.display.set_mode((800, 600))

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('#707070'))

        self.manager = pygame_gui.UIManager((800, 600), "data/themes/guiopedia_theme.json")
        self.manager.preload_fonts([{'name': 'fira_code', 'point_size': 24, 'style': 'bold'},
                                    {'name': 'fira_code', 'point_size': 24, 'style': 'bold_italic'},
                                    {'name': 'fira_code', 'point_size': 18, 'style': 'bold'},
                                    {'name': 'fira_code', 'point_size': 18, 'style': 'regular'},
                                    {'name': 'fira_code', 'point_size': 18, 'style': 'bold_italic'},
                                    {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
                                    ])

        self.guiopedia_window = GUIopediaWindow(manager=self.manager)

        self.clock = pygame.time.Clock()
        self.is_running = True

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        if not self.guiopedia_window.alive():
                            self.guiopedia_window = GUIopediaWindow(manager=self.manager)

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()


if __name__ == '__main__':
    app = GUIopediaApp()
    app.run()
