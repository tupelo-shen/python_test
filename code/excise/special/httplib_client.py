#!/usr/bin/python3
# coding:utf-8
# imported modules
import httplib

httpconn = httplib.HTTPSConnection("www.ibm.com")
httpconn.request("GET", "/developerworks/index.html")
resp = httpconn.getresponse()

if resp.reason == "OK":
    resp_data = resp.read()
    print resp_data
    
httpconn.close()
# conn = httplib.HTTPSConnection("www.baidu.com")
# conn.request('get', '/')
# print conn.getresponse().status
# print conn.getresponse().read()
# conn.close()
