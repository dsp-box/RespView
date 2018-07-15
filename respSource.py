#! /usr/bin/python3

# application: RespView
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# brief: loader for respiration signal
# opensource licence: LGPL-2.1

import os
import time

    
class RespSource(list):
    def __init__(self, srcpath, sensor=1, column=0):
        
        if not os.path.exists(srcpath):
            raise ValueError("no file")
        self.srcpath = str(srcpath)
        
        if self.srcpath == "/dev/urandom":
            self.fill = self.fill_from_urandom
            
        elif "/dev/ttyACM" in self.srcpath:
            self.fill = self.fill_from_serial
        
        else:
            info = "not supported source"
            raise ValueError(info)
        
        self.sensor = int(sensor)
        self.column = int(column)
        
        # for urandom only
        self.divider = 10.0
        self.counter = 0
        self.temp = 0.0
        
        
    def fill_from_urandom(self):
        kwargs = {"byteorder":"big", "signed":True}
        
        print("open source...")
        with open(self.srcpath, 'rb') as f:
            while True:               
                bytesVal = f.read(1)            
                value = int.from_bytes(bytesVal, **kwargs)
                
                self.temp += value                
                self.temp /= self.divider
                
                self.stamp = time.time()
                self.append((self.stamp, self.temp))

                if  self.counter % 50 == 0:
                    time.sleep(0.002)
                
        print("urandom reading end...")
        
    def fill_from_serial(self):
        print("open source...")
        unicodeError = 0
        with open(self.srcpath, 'rt') as f:
            while True:               
                try:
                    self.counter += 1
                    line = f.readline()
                    vec = str(line).split(",")
                    
                except UnicodeDecodeError:
                    info = "no line ({})".format(unicodeError)
                    print("UnicodeDecodeError:", info)
                    unicodeError += 1
                    continue
                
                if len(vec) != 9:
                    print("LengthError: " + line, end="")
                    continue

                try:
                    sen, item = vec[0].split(":")
                    vec[0] = item
                
                    item, end = vec[-1].split("#")
                    vec[-1] = item
                    
                except ValueError:
                    print("ValueError: " + line, end="")
                    continue

                try:
                    if self.sensor != int(sen[1]):
                        print("WrongSensorError: " + line, end="")
                        continue
                    
                except IndexError:
                    print("SensorError: " + line, end="")
                    continue
                
                self.stamp = time.time()
                val = int(vec[self.column])
                self.append((self.stamp, val))
                
        print("serial reading end...")

    def get_rate(self):
        try:
            td = self.stamp - self.tlast
            cd = self.counter - self.clast
            return float(cd) / td
            
        except AttributeError:
            return 0
        except ZeroDivisionError:
            return 0

        finally:
            try:
                self.clast = self.counter
                self.tlast = self.stamp
            except AttributeError:
                pass            
