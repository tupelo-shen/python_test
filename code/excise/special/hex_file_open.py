import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8") 

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

matrix = [[0 for i in range(17)] for i in range(100)]
bin_file = open("32.bin", 'rb')
print bin_file.readline()
#print matrix
#bin_file.seek(24, 0)
for i in range(0, 17):
    for j in range(0, 99):
        #bin_file.seek(24+i*16+j*2, 0)
        matrix[j][i], = struct.unpack('c', bin_file.read(1))
        #matrix[j][i] = bin_file.read(1)
        #print matrix[j][i]

print matrix        