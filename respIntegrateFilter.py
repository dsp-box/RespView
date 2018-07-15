#! /usr/bin/python3

# application: RespView
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# brief: filter for respiration signal
# opensource licence: LGPL-2.1

class RespIntegrateFilter(list):    

    def __init__(self, order, absFlag=True):
        super(RespIntegrateFilter, self).__init__()
        self.order = int(order)
        self.curr = 0.0

        if absFlag:
            self.process = self.process_abs
        else:
            self.process = self.process_int
            
    def process_abs(self, sample):
        self.append(sample)
        if len(self) > self.order:
            value = self.pop(0)
            self.curr += abs(value)
            
        self.curr -= abs(sample)
        return self.curr

    def process_int(self, sample):
        self.append(sample)
        if len(self) > self.order:
            value = self.pop(0)
            self.curr -= value
            
        self.curr += sample
        return self.curr
