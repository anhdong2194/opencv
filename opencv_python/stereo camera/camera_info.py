#!/usr/bin/env python
import cv2
import numpy as np
import rospy
from sensor_msgs.msg import CameraInfo
import time
import yaml


def imput_yaml(calib_file):
    with file(calib_file, 'r') as f:
        params = yaml.load(f)

    cam_info = CameraInfo()
    cam_info.height = params['size']['height']
    cam_info.width = params['size']['width']
    cam_info.distortion_model = 'plumb_bob'
    cam_info.K = params['cameraMatrix']['data']
    cam_info.D = params['distortionCoefficients']['data']
    cam_info.R = params['rotation']['data']
    cam_info.P = params['projection']['data']
    return cam_info

def publisher(cam_info,cam_pub):
    stamp = rospy.Time.from_sec(time.time())
    cam_info.header.stamp = stamp
    cam_pub.publish(cam_info)

if __name__ == '__main__':
    rospy.init_node('tester')
    cam_info = imput_yaml('test.yaml')
    cam_pub = rospy.Publisher('testing', CameraInfo)

    try:
        while not rospy.is_shutdown():
            publisher(cam_info,cam_pub)
            rospy.sleep(1.0)

    except rospy.ROSInterruptException:
        pass
