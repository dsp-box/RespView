#! /usr/bin/python3

# application: RespView
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# brief: viewers for respiration signal
# opensource licence: LGPL-2.1

import gi, sys, time
gi.require_version('Gtk', '3.0')
from gi.repository import GObject
from gi.repository import Gtk

from respViewer import RespViewer
from respSource import RespSource

from respTools import ExtOrderedDict
from respTools import drawPixBuf
from respTools import randomRGB


class MonoViewer(RespViewer):
    title = "Mono Viewer"
    
    def __init__(self, width, height, srcpath, factor):
        super(MonoViewer, self).__init__(self.title, width, height)
        self.source = RespSource(srcpath)
        self.factor = float(factor)
        
        self.images = ExtOrderedDict()
        for n in range(self.width):
            stamp = time.time()
            self.images[stamp] = self.init_image()
            self.fix.put(self.images[stamp], n, 0)

        ebox = Gtk.EventBox()
        ebox.connect('button-press-event',
                     self.on_clicked_mouse)
        self.fix.put(ebox, 0,0)
        
        active = Gtk.Image()
        active.set_size_request(width, height)
        ebox.add(active)
        
        GObject.timeout_add(1, self.on_timeout)
        self.show_all()

    def refresh(self, data):
        key, img = self.images.first_item()
        pbuf = drawPixBuf(data, 1, self.height)
        img.set_from_pixbuf(pbuf)
        self.images.pop(key)
        
        stamp = time.time()
        self.images[stamp] = img
        
        for n, k in enumerate(self.images.keys()):
            self.fix.move(self.images[k], n, 0)

        while Gtk.events_pending():
            Gtk.main_iteration()
        
    def on_timeout(self, data=None):
        val = self.factor * self.source.get()
        nr = self.height * (val + 0.5)
        white = (255, 255, 255)        
        gray = (100, 100, 100)        
        
        data = []
        for n in range(self.height):
            rgb = white if n >= nr else gray
            data.extend(rgb)                
        
        self.refresh(data)
        return True
    
    def init_image(self):
        rgb = randomRGB()        
        data = [c for index in range(self.height) for c in rgb]

        img = Gtk.Image()
        pbuf = drawPixBuf(data, 1, self.height)
        img.set_from_pixbuf(pbuf)

        return img 

    def on_clicked_mouse (self, box, event):        
        x, y = int(event.x), int(event.y)
        t = list(self.images.keys())[x]        
        tstruct = time.localtime(t)
        
        s = tstruct.tm_sec
        m = tstruct.tm_min
        h = tstruct.tm_hour

        Y = tstruct.tm_year
        M = tstruct.tm_mon
        D = tstruct.tm_mday

        d = "{}-{}-{}".format(D, M, Y)
        t = "{}:{}:{}".format(h, m, s)
        print("XY: {} {}, time {}, date {}".format(x, y, t, d))

try:
    try:
        source = str(sys.argv[1])
        factor = float(sys.argv[2])
        
    except IndexError:
        source = "/dev/urandom"
        factor = 0.01
        
    args = 1200, 200, source, factor
    win = MonoViewer(*args)    
    Gtk.main()
    
    print("end..")
except KeyboardInterrupt:
    print("break..")
