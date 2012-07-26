#!/usr/bin/env python

import struct, sys

offset = 0

with open('bytes','r') as f:
    bytestr = f.read()

bytestr = bytestr[offset:]
print "Parsing:", bytestr

simple = False
if simple:
    for (i,b) in enumerate(bytestr[:]):
        s = struct.unpack('B',b)[0]
        print "%03i : %i" % (i, s)
    print ""

    for (i,b) in enumerate(bytestr[:]):
        s = struct.unpack('B',b)[0]
        s = hex(s)
        if i % 25 == 24:
            print s
        else:
            print s,
    print
    sys.exit(0)

state = 0

# data is bcd so
#   0b0101 = 5
#   0b0010 = 2, etc
# look at 4 bit chunks
def print_temp(sid, pid, tb1, tb2, tb3, tb0):
    print "S %2i at %3i:" % (sid,pid),
    if sid == 2:
        print "\t\t\t\t\t",
    #print tb1, tb2, tb4
    #up = lambda x: struct.unpack('B',x)[0]
    #print up(tb1), up(tb2), up(tb4)
    #i = (struct.unpack('i','\x00'+tb1+tb2+'\x00')[0] << 4)
    #f = struct.unpack('H','\x00'+tb4)[0]
    #print i, f
    #print struct.unpack('f',tb1+tb2+'\x00'+tb4)[0]
    # 4 is really 1
    #ti = struct.unpack('B',tb1)[0]
    #ti = (ti & 0b11110000)
    #tb1 = chr(ti)
    #i = (struct.unpack('H',tb2+tb1)[0] >> 4)
    #f = struct.unpack('H',tb1+tb4)[0]
    #print i, f
    i1 = struct.unpack('B',tb1)[0]
    i2 = struct.unpack('B',tb2)[0]
    i3 = struct.unpack('B',tb3)[0]
    i0 = struct.unpack('B',tb0)[0]
    

    i = (i1 & 0b11110000) >> 4
    i += (i2 & 0b00001111) * 10
    i += ((i2 & 0b11110000) >> 4) * 100
    i += (i3 & 0b00001111) * 1000

    f0 = (i1 & 0b11110000) >> 4
    f1 = (i1 & 0b00001111)
    f2 = (i0 & 0b11110000) >> 4
    f3 = (i0 & 0b00001111)
    print i, f0, f1, f2, f3
    #i = ((i1 & 0b11110000) >> 4) + (i2 << 4) + ((i3 & 0b00001111) << 12)
    #f = (i1 << 8) + i0
    #i = (((i3 & 0b00001111) << 6) + (i2 << 4) + (i1>> 4))
    #f = i0
    #print i0, i1, i2, i3
    #print i, f
    #bits = lambda x : bin(x)[2:].zfill(8)
    #print bits(i3), bits(i2), bits(i1), bits(i0)

    #print i0, i1, i2, i3
    #print bits(i0), bits(i1), bits(i2), bits(i3)
    
    #print "\t\t",
    #if sid == 2:
    #    print "\t\t\t\t\t",
    #print 
    #print bin(i), bin(f)
    #print i, f


pid = 0
tb1 = 'a'
tb2 = 'a'
#tb3 = 'a'
tb4 = 'a'

for b in bytestr[:]:
    i = struct.unpack('B',b)[0]
    if state == 0:
        if i == 171: state += 1
    elif state == 1:
        if i == 170: state += 1
        else: state = 0
    elif state == 2:
        if i == 177: state += 1
        else: state = 0
    elif state == 3:
        pid = i
        state += 1
    elif state in (4,5,8,17,18,19,20,21,22,23):
        if i == 0: state += 1
        else: state = 0
    elif state == 6:
        if i == 22: state += 1
        else: state = 0
    elif state == 7:
        if i == 1: state += 1
        else: state = 0
    elif state in (9,13):
        # first temp byte?
        tb1 = b
        state += 1
    elif state in (10,14):
        # sensor id
        tb2 = b 
        state += 1
    elif state in (11,15):
        tb3 = b
        state += 1
    elif state in (12,16):
        tb0 = b
        if state == 12:
            sid = 1
        elif state == 16:
            sid = 2
        print_temp(sid, pid, tb1, tb2, tb3, tb0)
        state += 1
    elif state == 24:
        state = 0 # return to start state
    #print state
