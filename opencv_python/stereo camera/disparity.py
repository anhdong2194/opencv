#!/usr/bin/env python


from __future__ import print_function

import numpy as np
import cv2 as cv

img_counter = 0
img_width = 640
img_height = 720

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


if __name__ == '__main__':
    cam = cv.VideoCapture(1)
    while True:
        ret, frame = cam.read()
        frame = cv.flip(frame,0)
        imgL = frame[0:img_height/2,0:img_width/2]
        imgR  = frame[0:img_height/2,img_width/2:img_width]
        # disparity range is tuned for 'aloe' image pair
        window_size = 3
        min_disp = 16
        num_disp = 112-min_disp
        stereo = cv.StereoSGBM_create(minDisparity = min_disp,
            numDisparities = num_disp,
            blockSize = 16,
            P1 = 8*3*window_size**2,
            P2 = 32*3*window_size**2,
            disp12MaxDiff = 1,
            uniquenessRatio = 10,
            speckleWindowSize = 100,
            speckleRange = 32
        )
    
        #print('computing disparity...')
        disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0
    
        #print('generating 3d point cloud...',)
        h, w = imgL.shape[:2]
        f = 0.8*w                          # guess for focal length
        Q = np.float32([[1, 0, 0, -0.5*w],
                        [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis,
                        [0, 0, 0,     -f], # so that y-axis looks up
                        [0, 0, 1,      0]])
        points = cv.reprojectImageTo3D(disp, Q)
        colors = cv.cvtColor(imgL, cv.COLOR_BGR2RGB)
        mask = disp > disp.min()
        out_points = points[mask]
        out_colors = colors[mask]
        print ("out_points = ",out_points)
        cv.imshow('left', imgL)
        cv.imshow('disparity', (disp-min_disp)/num_disp)
        k = cv.waitKey(1)

        if k%256 == 27:
            print("Escape hit, closing...")
            break
    cam.release()
    cv.destroyAllWindows()

