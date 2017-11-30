#!/usr/bin/env python  # start line
# module doc
# imported modules
import sys,getopt
from socket import *

# variable definitions
HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024

# class definition
# function definition
def usage():
    print 'Usage: python argv.py [-s <xyz>] arg1[,arg2..]'
    print 'Options:'
    print '    -h, --help       show this help message and exit'
    print '    -i, --ip         server ip'
    print '    -p, --port       server port'
    
def proc_cmd_args():
    try:
        options,args = getopt.getopt(sys.argv[1:],"hp:i:",["help","ip=","port="])
    except getopt.GetoptError:
        sys.exit()

    for name,value in options:
        if name in ("-h","--help"):
            usage()
            sys.exit()
        if name in ("-i","--ip"):
            global HOST 
            HOST = value

        if name in ("-p","--port"):
            global PORT 
            PORT = int(value)

def client_proc():
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    addr = (HOST, PORT)
    print addr
    tcpCliSock.connect(addr)

    while True:
        data = raw_input('>')
        if not data:
            break
        tcpCliSock.send(data)
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        print data

    tcpCliSock.close()

# main program
def main():
    socket.getservbyname.__doc__
    proc_cmd_args()
    client_proc()

if __name__ == '__main__':
    main()