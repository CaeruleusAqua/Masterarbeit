#!/usr/bin/env python2

import json

from cv_gui.handler import Handler
from objects import *

if __name__ == '__main__':
    tmp = Handler([800, 600],'test.json')
    tmp.start()
