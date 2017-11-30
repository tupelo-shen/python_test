#!/usr/bin/env python  # start line
# module doc
# imported modules
import sys,getopt
# variable definitions
# class definition
# function definition
# main program
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
        if name in ("-i","--ip"):
            print 'ip is----',value
        if name in ("-p","--port"):
            print 'port is----',value
            
def main():
    proc_cmd_args()

if __name__ == '__main__':
    main()