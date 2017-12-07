#!/usr/bin/env python  # start line
# module doc
# imported modules
import sys
from socket import *

# variable definitions
# class definition
# function definition
class Simple:
    def __init__(self, name):
        self.name = name

    def hello(self):
        print self.name+" says hi."

class Simple2(Simple):
    def goodbye(self):
        print self.name+" says goodbye."
 
me = Simple2("Tim")
me.hello()
me.goodbye()
