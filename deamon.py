# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
""" 
import threading
import numpy as np
import time

def randnumgen():
    for a in range(30):
        print(a)
        time.sleep(1)
        
        
thr2=threading.Thread(target=randnumgen)
thr2.daemon=True
thr2.start()


def greetings():
    for i in range(10):
        print("Hello")
        time.sleep(1)

greetings()
