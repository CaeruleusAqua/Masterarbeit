#!/usr/bin/env python
import numpy as np


original = np.arange(50000)
double = original/500.0
half = double.astype(np.float16)

print (double-half.astype(np.float))

