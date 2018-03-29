#!/usr/bin/env python
#coding=utf-8
import requests
from time import sleep


r = requests.get(url='http://www.baidu.com')    # 最基本的GET请求

print(r.status_code)    # 获取返回状态
r = requests.get(url='http://dict.baidu.com/s', params={'wd':'python'})   #带参数的GET请求
print(r.url)
print(r.text)   #打印解码后的返回数据

sleep(60)