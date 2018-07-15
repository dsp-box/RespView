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
from gi.repository import Gdk

from threading import Thread

from respViewer import RespViewer
from respSource import RespSource

from respTools import randomRGB
from respTools import drawPixBuf
from respTools import ExtOrderedDict
from collections import OrderedDict

from respHammingFilter import RespHammingFilter
from respIntegrateFilter import RespIntegrateFilter
                                

class MonoViewer(RespViewer):
    title = "Mono Viewer"
    white = (255, 255, 255)        
    gray = (160, 160, 160)        
        
    
    def __init__(self, width, height, latency, srcpath, sensor=1, column=0):
        super(MonoViewer, self).__init__(self.title, width, height)
        self.latency = float(latency)
        self.counter = 0

        self.axis = 3 * int(self.height / 2)
        self.sample = 0.0
        self.set_center()
        self.reset_factor()
        
        self.key_register(102, self.reset_factor)
        self.key_register(99, self.set_center)
        
        self.inbuf = OrderedDict()        
        self.images = ExtOrderedDict()        
        for n in range(self.width):
            stamp = time.time()
            self.images[stamp] = self.init_image()
            self.fix.put(self.images[stamp], n, 0)
        
        ebox = Gtk.EventBox()
        ebox.connect('scroll-event', self.on_scroll)
        ebox.connect('button-press-event', self.on_mouse)
        ebox.add_events(Gdk.EventMask.SCROLL_MASK|Gdk.EventMask.SMOOTH_SCROLL_MASK)
        
        self.fix.put(ebox, 0,0)
        
        active = Gtk.Image()
        active.set_size_request(width, height)
        ebox.add(active)
                
        GObject.timeout_add(50, self.on_timeout)
        self.show_all()

        self.source = RespSource(srcpath, sensor, column)
        # self.preproc = RespHammingFilter(180)
        self.preproc = RespIntegrateFilter(220, False)
        
        self.flow = Thread(target=self.source.fill, daemon=True)
        self.flow.start()

    def on_scroll(self, box, event):
        if event.delta_y > 0:
            self.factor /= 1.2
        else:
            self.factor *= 1.8            
        print("factor: %.8f" % self.factor)
                
    def refresh(self):
        for stamp in self.inbuf.keys():
            sample = self.inbuf[stamp]
            
            if sample < 0:
                sample = 0
            elif sample >= self.height:
                sample = self.height - 1
                
            data = []            
            data.extend(self.white * sample)                
            data.extend(self.gray * (self.height - sample))
            data[-self.axis:-self.axis-2] = (0, 0, 0)
            
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
            t, s = self.source.pop(0)
            self.sample = self.preproc.process(s)
            
            sample = self.sample + self.const            
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
    
    def on_mouse (self, box, event):        
        x, y = int(event.x), int(event.y)
        t = list(self.images.keys())[x]        
        tstruct = time.localtime(t)

        ms = int(round(t * 1000))
        ms %= 1000
        
        s = tstruct.tm_sec
        m = tstruct.tm_min
        h = tstruct.tm_hour

        Y = tstruct.tm_year
        M = tstruct.tm_mon
        D = tstruct.tm_mday

        d = "{}-{}-{}".format(D, M, Y)
        T = "{:02d}:{:02d}:{:02d}.{:03d}".format(h, m, s, ms)
        print("XY: {} {}, time {}, date {}".format(x, y, T, d))

    def reset_factor(self):
        self.factor = 0.0001
        print("factor:", self.factor)
        
    def set_center(self):
        self.const = -self.sample
        print("const:", self.const)
try:
    cmdargs = {}
    try:
        cmdargs["srcpath"] = str(sys.argv[1])
        print("source: " + sys.argv[1])
        
        cmdargs["sensor"] = int(sys.argv[2])
        print("sensor: " + sys.argv[2])
        
        cmdargs["column"] = int(sys.argv[3])
        print("column: " + sys.argv[3])
        
    except IndexError:
        cmdargs["srcpath"] = "/dev/urandom"
        print("source: /dev/urandom")
        
    GObject.threads_init()
    print("threads init..")

    width = 600
    height = 600
    latency = 5
    
    winargs = width, height, latency
    win = MonoViewer(*winargs, **cmdargs)
    print("window init..")
    
    Gtk.main()    
    print("end..")
    
except KeyboardInterrupt:
    print("break..")
