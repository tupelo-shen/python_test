import httplib  
conn = httplib.HTTPSConnection("www.baidu.com")
conn.request("GET", "/")  
r1 = conn.getresponse()  
print r1.status, r1.reason  
  
data1 = r1.read()  
conn.request("GET", "/parrot.spam")  
r2 = conn.getresponse()  
print r2.status, r2.reason  
  
data2 = r2.read()  
conn.close()  