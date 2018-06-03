#! /usr/bin/python3

# application: RespView
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# brief: viewers for respiration signal
# opensource licence: LGPL-2.1

from collections import OrderedDict
from random import randint


class ExtOrderedDict(OrderedDict):
    def first_item(self):
        return next(iter(self.items()))


def randomRGB():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return r,g,b
