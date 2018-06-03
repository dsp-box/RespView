#! /usr/bin/python3

# application: SCREEN
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# brief: displays for signal presentation
# opensource licence: LGPL-2.1

from collections import OrderedDict

class ExtOrderedDict(OrderedDict):
    def first_item(self):
        return next(iter(self.items()))

import os

class Source(list):
    def __init__(self, fname):
        
        if not os.path.exists(fname):
            raise ValueError("no file")
        self.fname = str(fname)
        self.order = 30
        
    def get_from_system(self):
        with open(self.fname, 'rb') as f:
            bytesVal = f.read(1)
            
        kwargs = {"byteorder":"big", "signed":True}
        val = int.from_bytes(bytesVal, **kwargs)
        self.append(val)
        if len(self) > self.order:
            self.pop(0)
        
        return sum(self) / self.order
        
    def get(self):        
        if self.fname == "/dev/urandom":
            return self.get_from_system()
            
        else:
            info = "not supported source"
            raise ValueError(info)
