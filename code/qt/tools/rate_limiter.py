#!/usr/bin/env python2
import time


class Rate:
    def __init__(self, rate):
        self.rate = 1.0 / rate
        self.last = 0

    def sleep(self):
        if self.last == 0:
            self.last = time.time()
            time.sleep(self.rate)
        else:
            tmp = time.time()
            diff = tmp - self.last
            self.last = tmp + self.rate - diff
            time.sleep(max(0, self.rate - diff))

    def sleep_cond(self, cond):

        if not cond:  # noting happends
            print "normal"
            if self.last == 0:
                self.last = time.time()
                time.sleep(self.rate)
            else:
                tmp = time.time()
                diff = tmp - self.last
                self.last = tmp + self.rate - diff
                print max(0, self.rate - diff)
                time.sleep(max(0, self.rate - diff))
            print "done"
        else:  # recived command, do not sleep. but update infos
            print "fast_drop"

    def sleep_rate(self, fps):
        rate=1./fps
        if self.last == 0:
            self.last = time.time()
            time.sleep(rate)
        else:
            tmp = time.time()
            diff = tmp - self.last
            self.last = tmp + rate - diff
            time.sleep(max(0, rate - diff))



if __name__ == '__main__':
    tmp = Rate(1)
    while True:
        tmp.sleep()
