import cv2
import time
from mailing import send_mail
import streamlit as st
from time import strftime


st.title("Detektor dementů:")
start = st.button("Zahájit detekci")
stop = st.button("Zastavit detekci")

if start:
    obraz = st.image([])
    video = cv2.VideoCapture(0)
    #time.sleep(1)

    frame1 = None
    mail = True

    while True:
        if stop:
            break

        time = strftime("%w, %d.%m.%Y %H:%M:%S")
        dny = ["Nedele", "Pondeli", "Utery", "Streda", "Ctvrtek", "Patek", "Sobota"]
        time = time.replace(time[:2], dny[int(time[0])] + ",")

        check, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(img=frame, text=time, org=(50, 50), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2,
                    color=(0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gau = cv2.GaussianBlur(gray, (21, 21), 0)
        if frame1 is None:
            frame1 = gau

        diff = cv2.absdiff(frame1, gau)
        thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)[1]
        dilate = cv2.dilate(thresh, None, iterations=2)
        contours, check = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cont in contours:
            if cv2.contourArea(cont) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(cont)
            rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 1)
            if rectangle.any():
                if mail:
                    send_mail("Object was detected!")
                mail = False
        #cv2.imshow("Video", frame)
        obraz.image(frame)
        key = cv2.waitKey(1)

    video.release()