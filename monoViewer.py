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

from threading import Thread

from respViewer import RespViewer
from respSource import RespSource

from collections import OrderedDict
from respTools import ExtOrderedDict
from respTools import drawPixBuf
from respTools import randomRGB


class MonoViewer(RespViewer):
    title = "Mono Viewer"
    white = (255, 255, 255)        
    gray = (100, 100, 100)        
        
    
    def __init__(self, width, height, latency, srcpath, sensor=1, column=0, factor=1):
        super(MonoViewer, self).__init__(self.title, width, height)
        self.latency = float(latency)
        self.factor = float(factor)
        self.counter = 0
        
        self.inbuf = OrderedDict()        
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
                
        GObject.timeout_add(50, self.on_timeout)
        self.show_all()

        self.source = RespSource(srcpath, sensor, column)
        self.flow = Thread(target=self.source.fill, daemon=True)
        self.flow.start()
        
    def refresh(self):        
        for stamp in self.inbuf.keys():
            sample = self.inbuf[stamp]
            
            data = []            
            data.extend(self.white * sample)                
            data.extend(self.gray * (self.height - sample))

            key, img = self.images.first_item()
            pbuf = drawPixBuf(data, 1, self.height)
            img.set_from_pixbuf(pbuf)
            self.images.pop(key)
        
            self.images[stamp] = img        
            for n, k in enumerate(self.images.keys()):
                self.fix.move(self.images[k], n, 0)

        self.inbuf = OrderedDict()
        while Gtk.events_pending():
            Gtk.main_iteration()
        
    def on_timeout(self, data=None):
        self.counter += 1
        while self.source:
            t, sample = self.source.pop(0)
            val = self.factor * float(sample)            
            nr = self.height * (0.5 + val)
            self.inbuf[t] = int(nr)
            
        if len(self.inbuf) > self.latency:
            self.refresh()


        if self.counter % 100 == 0:
            print("rate: {}".format(self.source.get_rate()))
        
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
        print("source: " + sys.argv[1])
        
        sensor = int(sys.argv[2])
        print("sensor: " + sys.argv[2])
        
        column = int(sys.argv[3])
        print("column: " + sys.argv[3])
        
        factor = float(sys.argv[4])
        print("factor: " + sys.argv[4])
        
    except IndexError:
        source = "/dev/urandom"
        factor = 0.01
        
    GObject.threads_init()
    print("threads init..")

    width = 600
    height = 600
    latency = 5
    
    args = width, height, latency, source, sensor, column, factor
    win = MonoViewer(*args)
    print("window init..")
    
    Gtk.main()    
    print("end..")
    
except KeyboardInterrupt:
    print("break..")
