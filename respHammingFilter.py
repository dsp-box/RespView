#! /usr/bin/python3

# application: RespView
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# brief: filter for respiration signal
# opensource licence: LGPL-2.1

import math

class RespHammingFilter(list):    
    alpha = 0.53836
    beta = 0.46164

    def __init__(self, order):
        super(RespHammingFilter, self).__init__()
        self.order = int(order)
        
        self.coeff = []
        for n in range(self.order):
            a = float(2.0 * math.pi * n) / (self.order - 1)
            c = self.alpha - self.beta * math.cos(a) 
            self.coeff.append(c)
            
    def process(self, sample):
        self.append(sample)
        if len(self) > self.order:
            self.pop(0)

        output = 0.0
        for s, c in zip(self, self.coeff):
            output += s * c

        return output
