import urllib2
from time import sleep
# Create an OpenerDirector with support for Basic HTTP Authentication...
#auth_handler = urllib2.HTTPBasicAuthHandler()
#auth_handler.add_password(realm='PDQ Application',
#                           uri='https://mahler:8092/site-updates.py',
#                           user='klem',
#                           passwd='kadidd!ehopper')
# opener = urllib2.build_opener(auth_handler)
# # ...and install it globally so it can be used with urlopen.
# urllib2.install_opener(opener)
# urllib2.urlopen('http://www.example.com/login.html')

#url = 'http://www.pythontab.com'
url = 'https://www.baidu.com/'
username = 'shenwanjiang2013@163.com'
password = 'Shen19870314'

password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, url, username, password)

auth_handler = urllib2.HTTPDigestAuthHandler(password_mgr)

opener = urllib2.build_opener(auth_handler)
urllib2.install_opener(opener)
response = urllib2.urlopen(url)

the_page = response.read()
f= open("tmp.html", 'wb')
f.write(the_page)
f.close()

sleep(60)