import cv2
import time
from datetime import datetime

video = cv2.VideoCapture(0) # 0 to use the main camera (integrated to laptop). Otherwise 1
time.sleep(0.1)

first_frame = None
while True:
    check, frame = video.read()
    cv2.imshow("My Webcam - original", frame)

    # Get first image when starting camera using grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    if first_frame is None:
        first_frame = gray_frame_gau
        cv2.imshow("My Webcam - First Image grayed and blured", first_frame)

    # Get delta on picture from current image with gray scale image 
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    cv2.imshow("My Webcam - Delta with First Image", delta_frame)
    
    # Intensify modifed zone to be more white
    tresh_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(tresh_frame, None, iterations=5)
    cv2.imshow("My Webcam - Delta image using threshold", dil_frame)

    # Find coordinate of each "big" zones wit change detected & add a rectangle on the image
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 5000:
            x, y ,w ,h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w, w+h), (0,255,0), 5)
    # Add timestamp to the image
    now = datetime.now()
    cv2.putText(img=frame, text=now.strftime("%A %d/%m/%Y"), org=(30,25),
                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255,0,0),
                thickness=1, lineType=cv2.LINE_AA)
    cv2.putText(img=frame, text=now.strftime("%H:%M:%S"), org=(30,50),
                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0,0,255),
                thickness=1, lineType=cv2.LINE_AA)
    cv2.imshow("My Webcam - With Change Detection", frame)

    # Quit program by pressing "q" on keyboard
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()