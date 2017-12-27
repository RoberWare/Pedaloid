#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wiiuse

import sys
import time
import os
import json

nmotes = 2

def connect():
    if os.name != 'nt': print 'Press 1&2'

    wiimotes = wiiuse.init(nmotes)

    found = wiiuse.find(wiimotes, nmotes, 5)
    if not found:
        st='not found'
        print st
        return st
    connected = wiiuse.connect(wiimotes, nmotes)
    if connected:
        print 'Connected to %i wiimotes (of %i found).' % (connected, found)
    else:
        print 'failed to connect to any wiimote.'
        sys.exit(1)

    for i in range(nmotes):
        wiiuse.set_leds(wiimotes[i], wiiuse.LED[i])
        wiiuse.status(wiimotes[0])
        wiiuse.set_ir(wiimotes[0], 1)
        wiiuse.set_ir_vres(wiimotes[i], 1000, 1000)
    
    return wiimotes,nmotes


