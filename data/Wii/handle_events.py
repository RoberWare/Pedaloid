#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wiiuse
import pyautogui

import sys
import time
import os

def handle_event(wmp,i,mapping_keys):
    wm = wmp[0]
    if wm.btns:
        for name, b in wiiuse.button.items():
            if wiiuse.is_pressed(wm, b):
                if name == "Home":
                    return True
                elif mapping_keys.has_key(str(i)) and mapping_keys[str(i)].has_key(name):
                    print "click",i,name,'pressed'
                    pyautogui.click(mapping_keys[str(i)][name])
                else:
                    print "fail",i,name,'pressed'

def key_input(mapping_keys,wiimotes,nmotes):
    print "RECEIVING DATA\nPress the Home button when you're finished."
    print mapping_keys
    stop=0
    while True:
        r = wiiuse.poll(wiimotes, nmotes)
        if r != 0:
            for i in range(nmotes):
                if handle_event(wiimotes[i],i,mapping_keys):stop=1
        if stop == 1:break
