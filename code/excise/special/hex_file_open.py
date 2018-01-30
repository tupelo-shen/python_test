import sys
import os
reload(sys)
#sys.setdefaultencoding("utf-8") 

import struct

a = 20
b = 400

str = struct.pack("ii", a, b)
print 'length: ', len(str)
print str
print repr(str)

# unpack
str2 = struct.unpack("ii", str)
print 'length: ', len(str2)
print str2
print repr(str2)

print '*** creating test file...'
fobj = open('test', 'w')
fobj.write('foo\n')
fobj.write('bar\n')
fobj.close()
#bin_file = open("32.bin", 'rb')