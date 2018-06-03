#! /usr/bin/python3

# application: RespView
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# brief: viewers for respiration signal
# opensource licence: LGPL-2.1

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class RespViewer(Gtk.Window):
    def __init__(self, title, width, height):
        super(RespViewer, self).__init__(title=title)
        self.connect("delete-event", Gtk.main_quit)

        self.height = int(height)
        if self.height <= 0:
            raise ValueError("height")
        
        self.width = int(width)
        if self.width <= 0:
            raise ValueError("width")
        
        self.fix = Gtk.Fixed()
        self.add(self.fix)
        
    def on_clicked_mouse (self, box, event):        
        x, y = int(event.x), int(event.y)
        print("XY: {} {}".format(x, y))

