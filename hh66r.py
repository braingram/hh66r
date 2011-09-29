#!/usr/bin/env python

import glob, serial, struct, sys

class HH66R(object):
    _start0 = chr(170)
    _start1 = chr(177)
    _end = chr(171)
    def __init__(self, port):
        self._port = port
        self._serial = serial.Serial(port)

    def _read_packet(self):
        b = chr(0)
        while b != self._start0:
            b = self._serial.read(1)
        if self._serial.read(1) != self._start1:
            # bad packet
            return None
        packet = self._serial.read(23)
        return packet
    
    def _parse_temp(self, tempstr):
        """
        tempstr = F1,F2,F3,F0
        """
        i1 = struct.unpack('B',tempstr[0])[0]
        i2 = struct.unpack('B',tempstr[1])[0]
        i3 = struct.unpack('B',tempstr[2])[0]
        i0 = struct.unpack('B',tempstr[3])[0]
        
        s = (i3 & 0b00010000) >> 4
        s = (s * -2) + 1

        i = (i1 & 0b11110000) >> 4
        i += (i2 & 0b00001111) * 10
        i += ((i2 & 0b11110000) >> 4) * 100
        i += (i3 & 0b00001111) * 1000
        
        # not sure about f for now
        #f0 = (i1 & 0b11110000) >> 4
        f1 = (i1 & 0b00001111)
        f2 = (i0 & 0b11110000) >> 4
        f3 = (i0 & 0b00001111)
        f = i + f1 * 0.1 + f2 * 0.01 + f3 * 0.001
        return f * s
    
    def _parse_packet(self, packet):
        """
        packet is a 23 byte length string
        00 :    : packet id (increments)
        01 :  0 : ?
        02 :  0 : ?
        03 : 22 : (related to time?)
        04 :  1 : (interval in seconds?)
        05 :  0 : ?
        06 :    : T1_F1
        07 :    : T1_F2
        08 :    : T1_F3
        09 :    : T1_F0
        10 :    : T2_F1
        11 :    : T2_F2
        12 :    : T2_F3
        13 :    : T2_F0
        14 :    : 0
        ...
        22 : 171 : self._end
        """
        # check end bit of packet
        if packet[22] != self._end: return None
        t1 = self._parse_temp(packet[6:10])
        t2 = self._parse_temp(packet[10:14])
        return t1, t2
        

    def read_temps(self):
        packet = self._read_packet()
        if packet is None: return None
        temps = self._parse_packet(packet)
        return temps
    
    def __del__(self):
        self._serial.close()
        del self._serial

if __name__ == '__main__':
    # guess port
    pp = glob.glob('/dev/tty.usbserial*')
    if len(pp) > 0:
        port = pp[0]
    else:
        port = None
    
    N = 10
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    if len(sys.argv) > 2:
        port = sys.argv[2]

    thermometer = HH66R(port)
    nt = 0
    fails = 0
    while (nt < N) and (fails < N * 0.1):
        temps = thermometer.read_temps()
        if temps == None:
            fails += 1
            continue
        nt += 1
        print "%.3f, %.3f" % temps
