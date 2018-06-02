#! /usr/bin/python3

# application: SCREEN
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# brief: displays for signal presentation
# opensource licence: LGPL-2.1

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Screen(Gtk.Window):
    def __init__(self, title, width, height):
        super(TestScreen, self).__init__(title=title)

