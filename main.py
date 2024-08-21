__version__ = '0.1'
__author__ = 'Habib Ibrahim'

import data
import features
import threading
import time

import imutils
import cv2

# for camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# starter frame
_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)


while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)
    cv2.imshow("Camera", frame)

    if data.alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw
        if threshold.sum() > 100000:
            data.alarm_counter += 1
        else:
            if data.alarm_counter > 0:
                data.alarm_counter -= 1

        cv2.imshow("Sensor", threshold)
    else:
        cv2.imshow("Sensor", frame)

    if data.alarm_counter > 25 and data.detecting:
        if not data.alarm:
            try:
                data.alarm = True
                fam = threading.Thread(target=features.isFamiliar, args=(frame.copy(),))
                fam.start()
                fam.join()
                if data.familiar:
                    threading.Thread(target=features.send_alert, args=("familiar",)).start()
                else:
                    # Define the video writer
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    out = cv2.VideoWriter(data.output_path, fourcc, 20.0, (640, 480))
                    duration = 3
                    start_time = time.time()
                    while (time.time() - start_time) < duration:
                        ret, frame = cap.read()
                        if ret:
                            # Write frame to video file (optional)
                            out.write(frame)
                    out.release()
                    threading.Thread(target=features.send_alert, args=("not familiar",)).start()
                    threading.Thread(target=features.beep_alarm).start()
                    data.detecting = False
                    print("Detecting Stopped")
                    timer = threading.Timer(data.delay_seconds, features.delayDetecting_function).start()
            except ValueError:
                pass

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("e"):
        data.alarm_mode = not data.alarm_mode
        data.alarm_counter = 0
    if key_pressed == ord("d"):
        data.alarm_mode = False
    if key_pressed == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
