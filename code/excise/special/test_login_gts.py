#!/usr/bin/env python
#coding=utf-8
from requests import Request, Session
from requests.auth import HTTPDigestAuth
from requests_ntlm import HttpNtlmAuth
from time import sleep

url = 'http://sysdevgts.gbl.ykgw.net/eps/home.cfm'

r = Request('GET', url, auth=HttpNtlmAuth('30032183', 'Y0kogawa!'))
headers = r.headers

s = Session()
#r1 = s.get(url, auth=HttpNtlmAuth('30032183', 'Y0kogawa!'), headers=headers)
r1 = Request('POST',url, auth=HttpNtlmAuth('30032183', 'Y0kogawa!'), headers=headers)
prepared = r1.prepare()
r2 = s.send(prepared)

print r2.status_code, r2.content
#r = requests.get(url, auth=HttpNtlmAuth('30032183', 'Y0kogawa!'))
#print(r.text)    # 获取返回状态
#import requests
#import json
 
#r = requests.post('https://api.github.com/some/endpoint', data=json.dumps({'some': 'data'}))
#print(r.json())