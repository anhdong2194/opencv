#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 14:25:15 2017

@author: dongho
"""

import cv2
import numpy as np
import os
#from camera_calibrate import StereoCalibration


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

#path = '/home/dongho/Desktop/stereo_camera/stereo_capture'
while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame,0)
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
            if radius > 0.5:
                cv2.circle(frame, (int(x_l), int(y_l)), int(radius), colors[key], 2)
                cv2.putText(left_img,key , (int(x_l-radius),int(y_l-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
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
            
            if radius > 0.5:
                cv2.circle(right_img, (int(x_r), int(y_r)), int(radius), colors[key], 2)
                cv2.putText(right_img,key , (int(x_r-radius),int(y_r-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)   
    disparity = center_l[0] - center_r[0]
    if disparity == 0:
        pass
    else:
        Dis = (base * f)/disparity
    print "distance = ",Dis,"disparity = ",disparity
    #print "center_left = ",center_l
    #print "center_right = ",center_r
    cv2.imshow("test", frame)
    #cv2.imshow("left",left_img)
    #cv2.imshow("right",right_img)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        print("Escape hit, closing...")
        break
    """
    elif k%256 == 32:
        left_name = "LEFT_{}.png".format(img_counter)
        right_name = "RIGHT_{}.png".format(img_counter)
        cv2.imwrite(os.path.join(path,left_name), left_img)
        cv2.imwrite(os.path.join(path , right_name), right_img)
        print("{} written!".format(left_name))
        print("{} written!".format(right_name))
        img_counter += 1
    elif k%256 == 13:
        cal = StereoCalibration('/home/dongho/Desktop/stereo_camera/stereo_capture')
        print cal.camera_model
        print " Done , break now"
        break
    """
cam.release()

cv2.destroyAllWindows()