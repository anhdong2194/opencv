import numpy as np
import cv2
import hikvision.api

hik_camera = hikvision.api.CreateDevice('192.168.1.64', username='admin', password='seldatinc123')
cap = cv2.VideoCapture(hik_camera)

while(True):
     # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',ret)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()