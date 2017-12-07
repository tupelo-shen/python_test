#!/usr/bin/env python

import SocketServer
 
class hwRequestHandler( SocketServer.StreamRequestHandler ):
  def handle( self ):
    self.wfile.write("Hello World!\n")
 
 
server = SocketServer.TCPServer(("", 2525), hwRequestHandler)
server.serve_forever()