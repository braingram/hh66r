#!/usr/bin/env python

import serial, struct, sys

port = '/dev/tty.usbserial-ftDXLOO2'

p = serial.Serial(port, 19200)

totalbytes = 200

rawbytes = p.read(totalbytes)
p.close()

with open('bytes','w') as f:
    f.write(rawbytes)
sys.exit(0)

intline = ""
rawline = ""
uintline = ""
for i in xrange(totalbytes):
    b = p.read(1)
    uintline += " %3i" % struct.unpack('B',b)[0]
    intline += "%+4i" % struct.unpack('b',b)[0]
    rawline += "   %s" % b
    if i % 25 == 24:
        print rawline
        print intline
        print uintline
        print
        rawline = ""
        intline = ""
        uintline = ""

p.close()
