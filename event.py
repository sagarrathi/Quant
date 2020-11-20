#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 13:16:08 2020

@author: boo
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
""" 
import threading
import time


def randnumgen():
    for a in range(30):
        if event.is_set():
            break
        else:
            print(a)
            time.sleep(1)
                
event=threading.Event()
        
thr2=threading.Thread(target=randnumgen)
thr2.start()


def greetings():
    for i in range(10):
        print("Hello")
        time.sleep(1)
    
greetings()
event.set()