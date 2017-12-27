#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Xlib import display
import wiiuse

mapping_keys={}

def get_mouse_pos():
    events = data = display.Display().screen().root.query_pointer()._data
    X=data["root_x"]
    Y=data["root_y"]
    return X,Y

def handle_event(wmp):
    wm = wmp[0]
    if wm.btns:
        for name, b in wiiuse.button.items():
            if wiiuse.is_pressed(wm, b):
                return name

def mapping(wiimotes,nmotes):
    mapping_keys={}
    stop=0
    text="Press a wiimote button to associate it to a mouse position.\nPress the Home button when you're finished."
    print text
    while True:
        r = wiiuse.poll(wiimotes, nmotes)
        if r != 0:
            for i in range(nmotes):
                if not mapping_keys.has_key(i):mapping_keys[i]={}
                exec("button%i=handle_event(wiimotes[%i])"%(i,i))
                pos=get_mouse_pos()
                exec("if button%i == 'Home': stop=1\nelif not button%i == None: \n\tmapping_keys[%i][button%i]=pos \n\tprint i,button%i,pos"%(i,i,i,i,i))
                #print mapping_keys
        if stop == 1:
            break
    return mapping_keys

