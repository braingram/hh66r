#!/usr/bin/env python
# Example hh66r display for Pixelpulse
#
# you must install pixelpulse (and it's dependencies to run this demo)
# see: https://github.com/nonolith/pixelpulse
#
# after you've done that, just run
# python pixelpulsegui.py <port>
#   where port is the optional name of the port to use
# a web browser should open up showing the temperatures

import pixelpulse
import hh66r

import glob
import sys

def get_port():
    """
    use this function to assign the default port
    """
    return glob.glob('/dev/tty.usbserial*')[0]

class HH66RDevice(pixelpulse.Device):
    def __init__(self, port=None):
        self.temp1 = pixelpulse.AnalogChannel(
                name='Temp1',
                unit='C',
                min=0,
                max=40,
                showGraph=True
        )

        self.temp2 = pixelpulse.AnalogChannel(
                name='Temp2',
                unit='C',
                min=0,
                max=40,
                showGraph=True
        )
        if port is None: port = get_port()
        self.thermometer = hh66r.HH66R(port)
        # pixelpulse reads this property to determine which channels to show
        self.channels = [self.temp1, self.temp2]
    
    def start(self, server):
        """ This method is called by Pixelpulse once the server is started """
        server.poll(self.update) # ask the server to poll our update() method at its default sample rate
		
    def update(self):
        """ Polled to update the data as configured in start(). Returns a list of (channel. value) pairs """
        temps = None
        while temps is None:
            #print "fetching temp..."
            temps = self.thermometer.read_temps()
        #print "temp:", temps 
        return [(self.temp1, temps[0]), (self.temp2, temps[1])]
		
if __name__ == '__main__':
    port = None
    if len(sys.argv) > 1: port = sys.argv[1]
    dev = HH66RDevice(port)
    server = pixelpulse.DataServer(dev, poll_tick=0.5)
    server.start(openWebBrowser=True)
