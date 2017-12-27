#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wiiuse

def disconnect(wiimotes,nmotes):
    wmp=wiimotes[0]
    wm=wmp[0]
    print
    for i in range(nmotes):
        wiiuse.set_leds(wiimotes[i], 0)
        wiiuse.rumble(wiimotes[i], 0)
        wiiuse.disconnect(wiimotes[i])
        print 'wiimote id %i disconnected' % wm.unid