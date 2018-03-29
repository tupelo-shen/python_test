import urllib2
import cookielib
from time import sleep

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open('http://sysdevgts.gbl.ykgw.net/eps/home.cfm')
print cookie
# for item in cookie:
#     if item.name == 'some_cookie_item_name':
#         print item.value
sleep(60)