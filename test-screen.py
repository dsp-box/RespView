#! /usr/bin/python3

# application: SCREEN
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# brief: displays for signal presentation
# opensource licence: LGPL-2.1


import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('GLib', '2.0')
from gi.repository import GLib

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf as Gpb

from random import randint


class TestScreen(Gtk.Window):
    def __init__(self, title, width, height):
        super(TestScreen, self).__init__(title=title)

        fix = Gtk.Fixed()
        self.add(fix)
        
        ebox = Gtk.EventBox()
        ebox.connect ('button-press-event',
                      self.on_clicked_mouse)
        fix.put(ebox, 0,0)
        
        self.img = Gtk.Image()
        ebox.add(self.img)

        gen = range(3 * width * height)
        screen = [randint(0, 255) for n in gen]        
        self.screen_refresh(screen, width, height)
        self.show_all()

    def screen_refresh(self, screen, width, height):
        tmp = GLib.Bytes.new(screen)
        rgbcode = Gpb.Colorspace.RGB
        args = tmp, rgbcode, False, 8, width, height, 3*width
        pbuf = Gpb.Pixbuf.new_from_bytes(*args)
        self.img.set_from_pixbuf(pbuf)
        
    def on_clicked_mouse (self, box, event):        
        x = int(event.x)
        y = int(event.y)
        print("xy: %d %d" % (x, y))


win = TestScreen("Test Screen", 400, 300)              
win.connect("delete-event", Gtk.main_quit)


try:
    Gtk.main()
    print("end..")
except KeyboardInterrupt:
    print("break..")
