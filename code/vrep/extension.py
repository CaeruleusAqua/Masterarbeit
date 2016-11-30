#!/usr/bin/env python
import json

from pprint import pprint

with open('resources/scenario.sce') as data_file:
    data = json.load(data_file)

pprint(data)