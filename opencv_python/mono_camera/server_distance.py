#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 11:13:36 2018

@author: dongho
"""

#!/usr/bin/env python

import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new

HOST=''
PORT=8089

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print 'Socket created'

s.bind((HOST,PORT))
print 'Socket bind complete'
s.listen(10)
print 'Socket now listening'

conn,addr=s.accept()

### new
data = ""
payload_size = struct.calcsize("L") 

########init variable
center_l = None
center_r = None
base = 6
f = 174.618040#219.337321
#######image process
cam = cv2.VideoCapture(1)

cv2.namedWindow("test")

img_counter = 0
img_width = 640
img_height = 720

#define color space
lower = {'red':(166, 84, 141), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'orange':(0, 50, 80)} #assign new item lower['blue'] = (93, 10, 0)
upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255), 'orange':(20,255,255)}

#colors value
 
colors = {'red':(0,0,255), 'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217), 'orange':(0,140,255)}


def color_pre_process(frame):
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    return hsv


while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    ###

    frame=pickle.loads(frame_data)
    
    ###########################################################################
    left_img = frame[0:img_height/2,0:img_width/2]
    left_img = np.asarray(left_img)
    left_hsv = color_pre_process(left_img)
    right_img = frame[0:img_height/2,img_width/2:img_width]
    right_img = np.asarray(right_img)
    right_hsv = color_pre_process(right_img)
    for key, value in upper.items():
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(left_hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)               
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        
       
        if len(cnts) > 0:
            l = max(cnts, key=cv2.contourArea)
            ((x_l, y_l), radius) = cv2.minEnclosingCircle(l)
            M_L = cv2.moments(l)
            center_l = (int(M_L["m10"] / M_L["m00"]), int(M_L["m01"] / M_L["m00"]))           
            #if radius > 0.5:
            #    cv2.circle(frame, (int(x_l), int(y_l)), int(radius), colors[key], 2)
            #    cv2.putText(left_img,key , (int(x_l-radius),int(y_l-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
    for key, value in upper.items():
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(right_hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
               
        cnts_r = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
       
        if len(cnts_r) > 0:
            R = max(cnts_r, key=cv2.contourArea)
            ((x_r, y_r), radius) = cv2.minEnclosingCircle(R)
            M_R = cv2.moments(R)
            center_r = (int(M_R["m10"] / M_R["m00"]), int(M_R["m01"] / M_R["m00"]))
            
            #if radius > 0.5:
                #cv2.circle(right_img, (int(x_r), int(y_r)), int(radius), colors[key], 2)
                #cv2.putText(right_img,key , (int(x_r-radius),int(y_r-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)   
    disparity = center_l[0] - center_r[0]
    if disparity == 0:
        pass
    else:
        Dis = int(round((base * f)/disparity))
    cv2.putText(right_img,"Distance = " + str(Dis) , (int(x_r-radius + 5),int(y_r-radius + 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
    cv2.putText(left_img,"Distance = " + str(Dis) , (int(x_r-radius),int(y_r-radius + 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
    print "distance = ",Dis,"disparity = ",disparity
    ###########################################################################
    
    
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()