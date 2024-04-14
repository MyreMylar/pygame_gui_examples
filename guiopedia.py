import re
from collections import OrderedDict
from os import listdir, linesep
from os.path import isfile, join, basename, splitext

import pygame
import pygame_gui

from pygame_gui.elements import UITextBox


class GUIopediaWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager):
        super().__init__(pygame.Rect((200, 50), (420, 520)),
                         manager,
                         window_display_title='GUIopedia!',
                         object_id="#guiopedia_window")

        search_bar_top_margin = 2
        search_bar_bottom_margin = 2
        self.search_box = pygame_gui.elements.UITextEntryLine(pygame.Rect((150,
                                                                           search_bar_top_margin),
                                                                          (230, 30)),
                                                              manager=manager,
                                                              container=self,
                                                              parent_element=self)

        self.search_label = pygame_gui.elements.UILabel(pygame.Rect((90,
                                                                     search_bar_top_margin),
                                                                    (56,
                                                                     self.search_box.rect.height)),
                                                        "Search:",
                                                        manager=manager,
                                                        container=self,
                                                        parent_element=self)

        self.home_button = pygame_gui.elements.UIButton(pygame.Rect((20, search_bar_top_margin),
                                                                    (29, 29)),
                                                        '',
                                                        manager=manager,
                                                        container=self,
                                                        parent_element=self,
                                                        object_id='#home_button')

        self.remaining_window_size = (self.get_container().get_size()[0],
                                      (self.get_container().get_size()[1] -
                                       (self.search_box.rect.height +
                                        search_bar_top_margin +
                                        search_bar_bottom_margin)))

        self.pages = {}
        page_path = 'data/guiopedia/'
        file_paths = [join(page_path, f) for f in listdir(page_path) if isfile(join(page_path, f))]
        for file_path in file_paths:
            with open(file_path, 'r') as page_file:
                file_id = splitext(basename(file_path))[0]
                file_data = ""
                for line in page_file:
                    line = line.rstrip(linesep).lstrip()
                    # kind of hacky way to add back spaces at the end of new lines that
                    # are removed by the pyCharm HTML
                    # editor. perhaps our HTML parser needs to handle this case
                    # (turning new lines into spaces
                    # but removing spaces at the start of rendered lines?)
                    if len(line) > 0:
                        if line[-1] != '>':
                            line += ' '
                        file_data += line
                self.pages[file_id] = file_data

        index_page = self.pages['index']
        self.page_y_start_pos = (self.search_box.rect.height +
                                 search_bar_top_margin +
                                 search_bar_bottom_margin)
        self.page_display = UITextBox(index_page,
                                      pygame.Rect((0, self.page_y_start_pos),
                                                  self.remaining_window_size),
                                      manager=manager,
                                      container=self,
                                      parent_element=self)

    def process_event(self, event):
        handled = super().process_event(event)

        if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
            self.open_new_page(event.link_target)
            handled = True

        if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_element == self.search_box):
            results = self.search_pages(event.text)
            self.create_search_results_page(results)
            self.open_new_page('results')
            handled = True

        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_object_id == '#guiopedia_window.#home_button'):
            self.open_new_page('index')
            handled = True

        return handled

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
        return sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word_to_search_for),
                                          text_to_search,
                                          flags=re.IGNORECASE))

    def open_new_page(self, page_link: str):
        self.page_display.kill()
        self.page_display = None
        if page_link in self.pages:
            text = self.pages[page_link]

            self.page_display = UITextBox(text,
                                          pygame.Rect((0,
                                                       self.page_y_start_pos),
                                                      self.remaining_window_size),
                                          manager=self.ui_manager,
                                          container=self,
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


class GUIopediaApp:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('GUIopedia App')
        self.window_surface = pygame.display.set_mode((800, 600))

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('#707070'))

        self.manager = pygame_gui.UIManager((800, 600), "data/themes/guiopedia_theme.json")
        self.manager.preload_fonts([{'name': 'noto_sans', 'point_size': 24, 'style': 'bold'},
                                    {'name': 'noto_sans', 'point_size': 24, 'style': 'bold_italic'},
                                    {'name': 'noto_sans', 'point_size': 18, 'style': 'bold'},
                                    {'name': 'noto_sans', 'point_size': 18, 'style': 'regular'},
                                    {'name': 'noto_sans', 'point_size': 18, 'style': 'bold_italic'},
                                    {'name': 'noto_sans', 'point_size': 14, 'style': 'bold'}
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

                if (event.type == pygame.KEYDOWN and
                        event.key == pygame.K_F1 and
                        not self.guiopedia_window.alive()):
                    self.guiopedia_window = GUIopediaWindow(manager=self.manager)

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()


if __name__ == '__main__':
    app = GUIopediaApp()
    app.run()
