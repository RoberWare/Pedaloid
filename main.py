# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 21:08:01 2017

@author: roberto
"""

import os,sys,time
import json
from inputs import get_gamepad, get_mouse
import pyautogui
from Xlib import display
import threading
from threading import Thread


class GuitarLooper():
    def __init__(self):
        #global variables
        self.testing=0
        
        self.pedal_mode = 0
        self.mapping = 0
        self.stop=0
        
        pyautogui.FAILSAFE = False        
        
        #ASCII ART FROM http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
        self.title= """
                     ▄▄▄·▄▄▄ .·▄▄▄▄   ▄▄▄· ▄▄▌        ▪  ·▄▄▄▄  
                    ▐█ ▄█▀▄.▀·██▪ ██ ▐█ ▀█ ██•  ▪     ██ ██▪ ██ 
                     ██▀·▐▀▀▪▄▐█· ▐█▌▄█▀▀█ ██▪   ▄█▀▄ ▐█·▐█· ▐█▌
                    ▐█▪·•▐█▄▄▌██. ██ ▐█ ▪▐▌▐█▌▐▌▐█▌.▐▌▐█▌██. ██ 
                    .▀    ▀▀▀ ▀▀▀▀▀•  ▀  ▀ .▀▀▀  ▀█▄▀▪▀▀▀▀▀▀▀▀• 
                    """        
        
        #Main threads
        self.output_thread=Thread()
        self.pad_input_thread=Thread()  
        
        #click pedal variables
        self.button={}
        self.button[0]=0
        self.button[1]=0        
        
        self.btn0_X=0
        self.btn0_Y=0
        self.btn1_X=0
        self.btn1_Y=0
        
        #slide pedal variables
        self.pedal = 128
        
        self.state0_X=100
        self.state0_Y=100
        
        self.state1_X=100
        self.state1_Y=100

        self.state_1_X=100
        self.state_1_Y=100    
    
    def tester(self):
        code=""
        state=0
        while 1:
            try:
                events = get_gamepad()
            except Exception as e:
                print e
                break
            olddata=(0,0)
            for event in events:
                code=event.code
                state=event.state
                print "Event: ",(event.ev_type, code, state)
                print "Mouse position: ",self.get_mouse_pos()

            if self.testing==0:break
        return code,state
    
    def holdingbtn(self,t,btn):
        time.sleep(t)
        if self.button[btn]==1:
            self.button[btn]=2
        return
    
    def get_mouse_pos(self):
        events = data = display.Display().screen().root.query_pointer()._data
        X=data["root_x"]
        Y=data["root_y"]
        return X,Y

    def slide_output(self):
        pyautogui.moveTo(self.state0_X, self.state0_Y, .5)
        while 1:
            print (self.pedal*100)/255
            if self.pedal == 128:
                pyautogui.dragTo(self.state0_X, self.state0_Y, button='left')
            if self.pedal != 128:
                pyautogui.dragTo(self.state0_X, self.state0_Y+self.pedal-128, button='left')
            if self.stop == 1:
                self.stop=2
                break
    def slide_pad_input(self):
        while 1:
            try:
                events = get_gamepad()
            except Exception as e:
                print e
                break
            for event in events:
                if event.code == 'ABS_RZ':
                    self.pedal = event.state
                    #print self.pedal
                if event.code == 'BTN_TL2' and event.state == 1:
                    self.stop=1
                    break
    
    def click_output(self):
        btn0=0
        btn1=0
        while 1:
            if self.button[0]==1 and btn0 == 0:
                pyautogui.click(self.btn0_X, self.btn0_Y+80)
                print "btn0"
                btn0  = 1
            elif self.button[0]==2 and btn0 == 0:
                pyautogui.click(self.btn0_X, self.btn0_Y)
                print "btn0"
                btn0  = 1
            elif self.button[0]==0:
                btn0=0
    
            if self.button[1]==1 and btn1 == 0:
                pyautogui.click(self.btn1_X, self.btn1_Y)
                print "btn1"
                btn1 =1
            elif self.button[1]==0:
                btn1=0
            
            if self.stop==1:
                self.stop=2
                break
    def click_pad_input(self):
        code=""
        state=0
        while 1:
            try:
                events = get_gamepad()
            except Exception as e:
                code="NOGAMEPADFOUND"
                state=e
                break
            for event in events:
                code=event.code
                state=event.state
                if code == 'ABS_RZ' and state == 128:
                    self.button[0]=0
                elif code == 'ABS_RZ' and state > 128:
                    self.button[0]=1
                    """
                    holding = Thread(target=self.holdingbtn, args=(1,0,))
                    holding.start()
                    """
                    
                if code == 'ABS_RZ' and state == 128:
                    self.button[1]=0
                elif event.code == 'ABS_RZ' and event.state < 128:
                    self.button[1]=1
                    
                if code == 'ABS_RZ' and state == 128:
                    self.button[1]=0
                elif code == 'ABS_RZ' and state < 128:
                    self.button[1]=1
                
                if code == 'BTN_Z' and state == 1:
                    self.button["undo"]=1
                elif code == 'BTN_Z' and state == 0:
                    self.button["undo"]=0

                if code == 'BTN_WEST' and state == 1:
                    self.button["redo"]=1
                elif code == 'BTN_WEST' and state == 0:
                    self.button["redo"]=0                                        
                    
                    
                if code == 'BTN_TL2' and state == 1:
                    self.stop=1
                    break
                #print self.button
            if self.mapping==1:break
        return code,state
        
    def slide_mapping(self):
        self.mapping=1
        print "Press the pedal to asociate the initial mouse position to the place position.\nPress START button when you finish." 
        while 1:
            ans=self.click_pad_input()
            mouse_pos=self.get_mouse_pos()
            if ans[0]=='ABS_RZ':
                self.state0_X = mouse_pos[0]
                self.state0_Y = mouse_pos[1]
                print "Position: "+str(mouse_pos)
            if ans[0] == 'BTN_TR2' and ans[1] == 1:
                break
        print "Press the pedal to asociate the MAX mouse position to the position.\nPress START button when you finish." 
        while 1:
            ans=self.click_pad_input()
            mouse_pos=self.get_mouse_pos()
            if ans[0]=='ABS_RZ':
                self.state1_X = mouse_pos[0]
                self.state1_Y = mouse_pos[1]
                print "Position: "+str(mouse_pos)
            if ans[0] == 'BTN_TR2' and ans[1] == 1:
                break
        print "Press the pedal to asociate the MIN mouse position to the place position.\nPress START button when you finish." 
        while 1:
            ans=self.click_pad_input()
            mouse_pos=self.get_mouse_pos()
            if ans[0]=='ABS_RZ':
                self.state_1_X = mouse_pos[0]
                self.state_1_Y = mouse_pos[1]
                print "Position: "+str(mouse_pos)
            if ans[0] == 'BTN_TR2' and ans[1] == 1:
                break
        self.mapping=0
        return
        
    def click_mapping(self):
        self.mapping=1
        print "Press the pedal that you want to associate to your mouse position.\nPress START button when you finish."
        while 1:
            ans=self.click_pad_input()
            mouse_pos=self.get_mouse_pos()
            if ans[0]=='ABS_RZ' and ans[1]>128:
                self.btn0_X=mouse_pos[0]
                self.btn0_Y=mouse_pos[1]
                print "Button 0:\n\tx:%s\n\ty:%s"%(self.btn0_X,self.btn0_Y)
            if ans[0]=='ABS_RZ' and ans[1]<128:
                self.btn1_X=mouse_pos[0]
                self.btn1_Y=mouse_pos[1]
                print "Button 1:\n\tx:%s\n\ty:%s"%(self.btn1_X,self.btn1_Y)
            if ans[0] == 'BTN_TR2' and ans[1] == 1:
                break
        self.mapping=0
        return
    
    def open_gamepad(self):
        while True:
            gpads=os.listdir("./data")
            y=1
            mygpads={}
            for x in gpads:
                print "\t\t[%d]"%(y),x
                mygpads[y]=x
                y+=1
            print "\t\t[%s] Back"%(y)
            ans=raw_input("> ")
            if int(ans) in mygpads.keys():
                try:
                    with open("data/%s"%(mygpads[int(ans)])) as json_file:
                        self.gamepad_mapping = json.load(json_file)
                    print ">>>",self.gamepad_mapping
                except Exception as e:
                    print "[!]",e
                    break
                
            else:break
        
    def create_gamepad(self):
        gpadname=raw_input("Gamepad Name> ")
        print "Press ENTER when you finish associating."
        while True:
            ans=self.click_pad_input()
            if ans[0] == "NOGAMEPADFOUND":
                print "[!]",ans[1]
                break
            else:
                sys.stdout.write(str(ans[1])+" \r")
                sys.stdout.flush()
        with open('data/%s'%(gpadname), 'w') as json_file:
            json.dump(self.gamepad_mapping, json_file)
    
    def run(self):
        while True:
            print self.title+"\n\t\t[1] Open a gamepad conf.\n\t\t[2] New gamepad conf.\n\t\t[3] Exit.\n"
            ans=raw_input("> ")
            if ans == "1":
                self.open_gamepad()
            if ans == "2":
                self.create_gamepad()
            if ans == "3":
                sys.exit()


        if self.pedal_mode == 0: 
            self.output_thread = Thread(target=self.click_output)
            self.pad_input_thread = Thread(target=self.click_pad_input)
        if self.pedal_mode == 1: 
            self.output_thread = Thread(target=self.slide_output)
            self.pad_input_thread = Thread(target=self.slide_pad_input)
        
        print "\nPEDALOID STARTED\nPress SELECT button to exit.\n"
        self.output_thread.start()
        self.pad_input_thread.start()
        
    def main(self):
        while True:
            if self.stop == 2:
                self.output_thread.signal=0
                self.pad_input_thread.signal=0
                self.stop=0
                self.run()
        
    def start(self):
        if self.testing==1:
            self.tester()
        else:
            self.run()
            self.mainthread = Thread(target=self.main())
            self.mainthread.start()
        
if __name__ == '__main__':
    GuitarLooper().start()