#!/usr/bin/env python
from parser.parser import Parser

parser = Parser()
parser.parseSCN("resources/scenario.scn")
parser.saveSCN("resources/scenario_new.scn")
