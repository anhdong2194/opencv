#!/usr/bin/env python

import cv2
fs = cv2.FileStorage("/home/dongho/Desktop/stereo_camera/left.yaml", cv2.FILE_STORAGE_READ)
fn = fs.getNode("camera_matrix")
print(fn.mat())
