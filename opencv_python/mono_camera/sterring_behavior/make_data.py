#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 14:14:56 2018

@author: dongho
"""

import numpy as np
import cv2
import serial
import pygame
from pygame.locals import *
import socket
import time
import os


class CollectTrainingData(object):
    
    def __init__(self):
        """
        self.server_socket = socket.socket()
        self.server_socket.bind(('192.168.1.100', 8000))
        self.server_socket.listen(0)

        # accept a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')
        """
        # connect to a seral port
        self.ser = serial.Serial('/dev/tty.usbmodem1421', 115200, timeout=1)
        self.send_inst = True

        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')

        pygame.init()
        self.collect_image()

    def collect_image(self):

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print 'Start collecting images...'
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 4), 'float')
        cap=cv2.VideoCapture(1)
        cap.set(3,320)
        cap.set(4,240)
        # stream video frames one by one
        while True:
            ret,frame=cap.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # select lower half of the image
            roi = image[120:240, :]
                    
            # save streamed images
            cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)
            #cv2.imshow('roi_image', roi)
            cv2.imshow('image', image)
                    
            # reshape the roi image into one row array
            temp_array = roi.reshape(1, 38400).astype(np.float32)
            
            frame += 1
            total_frame += 1
            # get input from human driver
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()
                    
                    # complex orders
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, self.k[1]))
                        saved_frame += 1
                        self.ser.write(chr(6))
                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, self.k[0]))
                        saved_frame += 1
                        self.ser.write(chr(7))
                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")
                        self.ser.write(chr(8))
                            
                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")
                        self.ser.write(chr(9))
                    # simple orders
                    elif key_input[pygame.K_UP]:
                        print("Forward")
                        saved_frame += 1
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, self.k[2]))
                        self.ser.write(chr(1))

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        saved_frame += 1
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, self.k[3]))
                        self.ser.write(chr(2))
                            
                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, self.k[1]))
                        saved_frame += 1
                        self.ser.write(chr(3))

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, self.k[0]))
                        saved_frame += 1
                        self.ser.write(chr(4))

                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print 'exit'
                        self.send_inst = False
                        self.ser.write(chr(0))
                        break
                                    
                elif event.type == pygame.KEYUP:
                    self.ser.write(chr(0))
            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # save training data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:    
                np.savez(directory + '/' + file_name + '.npz', train=train, train_labels=train_labels)
            except IOError as e:
                print(e)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print 'Streaming duration:', time0

            print(train.shape)
            print(train_labels.shape)
            print 'Total frame:', total_frame
            print 'Saved frame:', saved_frame
            print 'Dropped frame', total_frame - saved_frame


if __name__ == '__main__':
    CollectTrainingData()