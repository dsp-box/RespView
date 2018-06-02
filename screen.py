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

class Screen(Gtk.Window):
    def __init__(self, title, width, height):
        super(Screen, self).__init__(title=title)

        self.height = int(height)
        if self.height <= 0:
            raise ValueError("height")
        
        self.width = int(width)
        if self.width <= 0:
            raise ValueError("width")
        
        fix = Gtk.Fixed()
        self.add(fix)
        
        ebox = Gtk.EventBox()
        ebox.connect ('button-press-event',
                      self.on_clicked_mouse)
        fix.put(ebox, 0,0)
        
        self.img = Gtk.Image()
        ebox.add(self.img)
        self.show_all()

    def screen_refresh(self, screen):
        tmp = GLib.Bytes.new(screen)
        rgbf = Gpb.Colorspace.RGB
        
        w = self.width 
        h = self.height
        w3 = 3 * self.width
        args = tmp, rgbf, False, 8, w, h, w3
        
        pbuf = Gpb.Pixbuf.new_from_bytes(*args)
        self.img.set_from_pixbuf(pbuf)

    def on_clicked_mouse (self, box, event):        
        x, y = int(event.x), int(event.y)
        print("XY: {} {}".format(x, y))
