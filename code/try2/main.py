#!/usr/bin/env python2

from cv_gui.draw_handler import DrawHandler
from state_machine import StateHandler

if __name__ == '__main__':
    threads = list()

    tmp = DrawHandler(StateHandler("test.json"))
    tmp.start()
    threads.append(tmp)
    for t in threads:
        t.join()
    print "Exiting Main Thread"

