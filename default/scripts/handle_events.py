#!/usr/bin/env python
# -*- coding: utf-8 -*-

#You can add all the args you want to import from the connect script returned vars
def key_input(mapping_keys,arg1,arg2):
    print "Handling events, type exit to quit"
    while True:
        #here the input stuff
        something=raw_input("> ").upper()
        #condition to break the loop
        if something=="EXIT":break
    #return vars
    return arg1,arg2
