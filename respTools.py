#! /usr/bin/python3

# application: RespView
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# brief: viewers for respiration signal
# opensource licence: LGPL-2.1

from collections import OrderedDict
from random import randint

import gi

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf as Gpb

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('GLib', '2.0')
from gi.repository import GLib

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk


class ExtOrderedDict(OrderedDict):
    def first_item(self):
        return next(iter(self.items()))

def randomRGB():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return r,g,b

def drawPixBuf(data, width, height):
    tmp = GLib.Bytes.new(data)
    rgbf = Gpb.Colorspace.RGB
    w3 = 3 * width

    args = tmp, rgbf, False, 8, width, height, w3
    pbuf = Gpb.Pixbuf.new_from_bytes(*args)
    return pbuf

def getKeyName(keyval):
    try: return Gdk.keyval_name(keyval.keyval)
    
    except AttributeError:
        return Gdk.keyval_name(keyval)
