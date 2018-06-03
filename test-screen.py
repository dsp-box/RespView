#! /usr/bin/python3

# application: SCREEN
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# brief: displays for signal presentation
# opensource licence: LGPL-2.1

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import GObject
from gi.repository import Gtk

from screen import Screen
from random import randint


class TestScreen(Screen):
    def __init__(self, title, width, height):
        super(TestScreen, self).__init__(title, width, height)

        self.img = Gtk.Image()        
        GObject.timeout_add(100, self.on_timeout)
        
        ebox = Gtk.EventBox()
        ebox.connect('button-press-event',
                     self.on_clicked_mouse)
        self.fix.put(ebox, 0,0)        
        ebox.add(self.img)
        self.show_all()

    def refresh(self):
        gen = range(3 * self.width * self.height)
        data = [randint(0, 255) for index in gen]
        args = data, self.width, self.height, self.img
        self.img = self.draw(*args)
        
        while Gtk.events_pending():
            Gtk.main_iteration()

    def on_timeout(self, data=None):
        self.refresh()
        return True


try:
    args = "Test Screen", 400, 100
    win = TestScreen(*args)              
    Gtk.main()
    print("end..")
except KeyboardInterrupt:
    print("break..")
