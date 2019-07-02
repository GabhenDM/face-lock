import sys
import threading
import serial
from time import sleep
import datetime
import os
import pickle
import requests
import time
import numpy as np
import cv2
import face_recognition
sys.path.append(".")

from facelock.models import Usuario
from facelock import db
#arduino = serial.Serial('/dev/ttyACM0', 9600)



video_capture = cv2.VideoCapture(0)


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


def onOffFunction(command):
    if command == "on":
        print("Abrindo a Porta...")
        time.sleep(60)
        global reconhecido
        reconhecido = False
        # arduino.write(b'H')
    elif command == "off":
        print("Fechando a Porta...")
        time.sleep(1)
        # arduino.write(b'L')
    elif command == "bye":
        print("Adeus!...")
        time.sleep(1)
        # arduino.close()


def salvar_snapshot(frame):
    img_name = "./snapshots/snapshot_{}.png".format(datetime.datetime.now())
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))
    time.sleep(60)
    global ja_tirou_foto
    ja_tirou_foto = False


def reconhecer(rgb_small_frame):
    face_encodings = face_recognition.face_encodings(
        rgb_small_frame, face_locations)

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
            controller.start()
            reconhecido = True
            name = known_face_names[best_match_index]
        face_names.append(name)

    # Display de resultado
    for (top, right, bottom, left), name in zip(face_locations, face_names):
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
            ja_tirou_foto= True
            salvarSnap = threading.Thread(
                    name="Salvar Snapshot", target=salvar_snapshot, args=(frame,))
            salvarSnap.start()


if __name__ == '__main__':
    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        cv2.imshow('Video', frame)
        # Hit 'q' on the keyboard to quit!
        if face_locations and not reconhecido:
            reconhecer(rgb_small_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
