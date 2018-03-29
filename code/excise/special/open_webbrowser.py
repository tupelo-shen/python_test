#!/usr/bin/env python

import webbrowser
from time import sleep

# webbrowser.open(url, new=0, autoraise=True)
# if not resigter the webbrowser, use default webbrowser.
# new   = 0,    open in the same as current webbrowser window;
#       = 1,    open in a new webbrowser window;
#       = 2,    open in a new webbrowser tab window;
webbrowser.open("http://sysdevgts.gbl.ykgw.net/eps/home.cfm", new=1,autoraise=True)

sleep(10)