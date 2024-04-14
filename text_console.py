import time

import pygame
import pygame_gui

import subprocess
import threading
import os


class Output:
    def __init__(self):
        self.text = ''


pygame.init()


pygame.display.set_caption('Pygame GUI - Console example')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'data/themes/console_theme.json')

background = pygame.Surface((800, 600))
background.fill(manager.ui_theme.get_colour('dark_bg'))

console_window = pygame_gui.windows.UIConsoleWindow(rect=pygame.rect.Rect((50, 50), (700, 500)),
                                                    manager=manager)

clock = pygame.time.Clock()
is_running = True

python_process = None

output_str = None
data_lock = None

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if (event.type == pygame_gui.UI_CONSOLE_COMMAND_ENTERED and
                event.ui_element == console_window):
            command = event.command

            if python_process is not None and output_str is not None:
                bytes_command = (command + '\n').encode()
                python_process.stdin.write(bytes_command)
                python_process.stdin.flush()

            else:
                if command == 'python':
                    console_window.set_log_prefix(" ")
                    python_process = subprocess.Popen(['python', '-i'],
                                                      stdin=subprocess.PIPE,
                                                      stdout=subprocess.PIPE,
                                                      stderr=subprocess.STDOUT, shell=False)
                    output_str = Output()
                    data_lock = threading.Lock()

                    def write_all(process, output, lock):
                        while True:
                            data = process.stdout.read(1).decode("utf-8")
                            if not data:
                                break
                            with lock:
                                output.text += data


                    writer = threading.Thread(target=write_all, args=(python_process,
                                                                      output_str,
                                                                      data_lock))
                    writer.start()

                elif command == 'clear':
                    console_window.clear_log()

        manager.process_events(event)

    if python_process is not None:
        if "\n" in output_str.text:
            split_output = output_str.text.split('\n', 1)
            with data_lock:
                output_str.text = split_output[1]
            output_line_to_print = split_output[0].strip()
            console_window.add_output_line_to_log(output_line_to_print)
        elif len(output_str.text) > 0:
            output_line_to_print = output_str.text.strip()
            with data_lock:
                output_str.text = ""
            console_window.add_output_line_to_log(output_line_to_print, remove_line_break=True)

        if python_process.poll() is not None:
            print('Python finished')
            python_process = None

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

if python_process is not None:
    python_process.kill()