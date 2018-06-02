#! /usr/bin/python3

# application: SCREEN
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# brief: displays for signal presentation
# opensource licence: LGPL-2.1

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from screen import Screen
from random import randint


class TestScreen(Screen):
    def __init__(self, title, width, height):
        super(TestScreen, self).__init__(title, width, height)

        gen = range(3 * self.width * self.height)
        screen = [randint(0, 255) for n in gen]        
        self.screen_refresh(screen)


win = TestScreen("Test Screen", 400, 300)              
win.connect("delete-event", Gtk.main_quit)


try:
    Gtk.main()
    print("end..")
except KeyboardInterrupt:
    print("break..")
