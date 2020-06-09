import os
import cv2
from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = r"C:\Users\oboro\PycharmProjects\Union\proc_img"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Включаем первую камеру
cv2.namedWindow("preview")
cap = cv2.VideoCapture(0)

# "Прогреваем" камеру, чтобы снимок не был тёмным
for i in range(30):
    cap.read()

while cap.isOpened():
    _, frame = cap.read()
    img = frame
    key = cv2.waitKey(100)
    cv2.imshow("preview", img)

    if key == 27:
        # Делаем снимок
        ret, frame = cap.read()
        img = frame
        # Записываем в файл
        cv2.imwrite('cam.png', frame)

        # Отключаем камеру
        cap.release()

cv2.destroyWindow("preview")
