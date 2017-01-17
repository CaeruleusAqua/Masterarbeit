#!/usr/bin/env python2
from parser import Parser

parser = Parser()
parser.parseSCN("resources/scenario.scn")
parser.saveSCN("resources/scenario_new.scn")
