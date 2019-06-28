import face_recognition
import cv2
import numpy as np
import time
import requests
import pickle
import os
import datetime
from time import sleep
import serial 
import threading
import sys

sys.path.append(".")
arduino = serial.Serial('/dev/ttyACM0', 9600)


from facelock.models import Usuario
from facelock import db

URL_CONTROLLER = "http://127.0.0.1:5000/controller"


video_capture = cv2.VideoCapture(0)


all_face_encodings = {}
# Load face encodings

with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','encoded_files','dataset_faces.dat')), 'rb') as f:
    all_face_encodings = pickle.load(f)

# Grab the list of names and the list of encodings
known_face_names = list(all_face_encodings.keys())
known_face_encodings = np.array(list(all_face_encodings.values()))


face_locations = []
face_encodings = []
face_names = []


def main():
    sleep(2)
    reconhecimento()


def salvar_snapshot(frame):
    img_name = "./snapshots/snapshot_{}.png".format(datetime.datetime.now())
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))



def onOffFunction(command):
	if command =="on":
		print("Abrindo a Porta...")
		time.sleep(1) 
		arduino.write(b'H') 
	elif command =="off":
		print("Fechando a Porta...")
		time.sleep(1) 
		arduino.write(b'L')
	elif command =="bye":
		print("Adeus!...")
		time.sleep(1) 
		arduino.close()

# Funcao Reconhecimento Facial
def reconhecimento():
    print("[+] Tirando Foto...")

    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
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
            name = known_face_names[best_match_index]
            print("[+] Rosto Reconhecido ! - " + name)
            x = threading.Thread(target=onOffFunction,args=('on',))
            x.start()
            #r = requests.get(url = URL_CONTROLLER, params = {'command': "on"})
            #if(r.status_code == 200):
            #    return
        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
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
    salvar_snapshot(frame)
    #cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #    return


main()
#   r = requests.get(url = URL_CONTROLLER, params = {'command': "off"})
#   time.sleep(5)
video_capture.release()
cv2.destroyAllWindows()
