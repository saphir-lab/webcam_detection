import cv2
import time

video = cv2.VideoCapture(0) # 0 to use the main camera (integrated to laptop). Otherwise 1
time.sleep(0.1)

first_frame = None
while True:
    check, frame = video.read()
    cv2.imshow("My Webcam - original", frame)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    cv2.imshow("My Webcam - Gray and Blur", gray_frame_gau)

    if first_frame is None:
        first_frame = gray_frame_gau
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    cv2.imshow("My Webcam - Delta with first image", delta_frame)
    
    tresh_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(tresh_frame, None, iterations=2)
    cv2.imshow("My Webcam - Delta image using threshold", dil_frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()