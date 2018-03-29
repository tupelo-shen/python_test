#! /usr/bin/env python
# -*- coding: UTF-8 -*-


'''
Example 20.1 HTTP Auth Client (urlopenAuth.py)
This script uses both techniques described above for basic authentication.

'''
import urllib2

LOGIN_USER = 'username'
LOGIN_PASSWD = 'password'
URL = 'http://localhost'

def handler_version(url):
    from urlparse import urlparse as up
    hdlr = urllib2.HTTPBasicAuthHandler()
    hdlr.add_password('Archives', up(url)[1], LOGIN_USER, LOGIN_PASSWD)
    opener = urllib2.build_opener(hdlr)
    urllib2.install_opener(opener)
    return url

def request_version(url):
    from base64 import encodestring
    req = urllib2.Request(url)
    b64str = encodestring('%s:%s' % (LOGIN, PASSWD))[:-1]
    req.add_header("Authorization", "Basic %s" % b64str)
    return req

for funcType in ('handler', 'request'):
    print '*** Using %s:' % funcType.upper()
    url = eval('%s_version')(URL)
    f = urllib2.urlopen(url)
    print f.readline()
    f.close()