

import sys
import threading
from time import sleep
import datetime
import os
import pickle
import requests
import time
import numpy as np
import cv2
import face_recognition
import logging
from logging.handlers import TimedRotatingFileHandler

import os

# Just to check for the existing of DEMO_MODE environment variable,
# but you could also compare its value, pass it forward and so on
DEV_MODE = os.environ.get("DEV_MODE", None)

if DEV_MODE:
    import FakeRPi.GPIO as GPIO
else:
    import RPi.GPIO as GPIO
sys.path.append(".")

from facelock import db
from facelock.models import Usuario


# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create handlers
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
logname = "./logs/recog.log"
f_handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
f_handler.setLevel(logging.INFO)
f_handler.suffix = "%Y%m%d"
f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
c_handler.setFormatter(f_format)
logger.addHandler(f_handler)
logger.addHandler(c_handler)

channel = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)


def relay_off():
    GPIO.output(channel, GPIO.HIGH)


def relay_on():
    GPIO.output(channel, GPIO.LOW)


video_capture = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


all_face_encodings = {}


# Carrega Encodings do Banco
encodings = Usuario.query.with_entities(Usuario.nome, Usuario.encoding).all()


reconhecido = False
ja_tirou_foto = False

# Converte encondings de binario para valores, adiciona em dict
for el in encodings:
    t = pickle.loads(el[1])
    all_face_encodings.update({el[0]: t})

# Divide encondings e nomes
known_face_names = list(all_face_encodings.keys())
known_face_encodings = np.array(list(all_face_encodings.values()))


face_locations = []
face_encodings = []
face_names = []
rects = []


def onOffFunction(command):
    if command == "on":
        print("Abrindo a Porta...")
        relay_on()
        time.sleep(1)
        relay_off()
        time.sleep(15)
        global reconhecido
        reconhecido = False

    elif command == "off":
        print("Fechando a Porta...")
        time.sleep(1)
        relay_off()
    elif command == "bye":
        print("Adeus!...")
        time.sleep(1)


def salvar_snapshot(frame):
    img_name = "./snapshots/snapshot_{}.png".format(datetime.datetime.now())
    cv2.imwrite(img_name, frame)
    logger.warning("{} written!".format(img_name))
    time.sleep(60)
    global ja_tirou_foto
    ja_tirou_foto = False


def reconhecer(rgb, boxes):
    face_encodings = face_recognition.face_encodings(rgb, boxes)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(
            known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            global reconhecido
            controller = threading.Thread(name="Controller Fechadura",
                                          target=onOffFunction, args=('on',))
            logger.info("[+] Reconhecido - %s", known_face_names[best_match_index])
            controller.start()
            reconhecido = True
            name = known_face_names[best_match_index]
        face_names.append(name)

    # Display de resultado
    for (top, right, bottom, left), name in zip(boxes, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35),
                      (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    font, 1.0, (255, 255, 255), 1)
        global ja_tirou_foto
        if not ja_tirou_foto and not reconhecido:
            ja_tirou_foto = True
            salvarSnap = threading.Thread(
                name="Salvar Snapshot", target=salvar_snapshot, args=(frame,))
            salvarSnap.start()


if __name__ == '__main__':
    while True:
        ret, frame = video_capture.read()
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # convert the input frame from (1) BGR to grayscale (for face
        # detection) and (2) from BGR to RGB (for face recognition)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect faces in the grayscale frame
        rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30))
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        #face_locations = face_recognition.face_locations(rgb_small_frame)
        cv2.imshow('Video', frame)
        # print(type(rects))
        # Hit 'q' on the keyboard to quit!
        # if :
        if type(rects) is not tuple and not reconhecido:
            reconhecer(rgb, boxes)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
