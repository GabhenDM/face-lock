import face_recognition
import cv2
import numpy as np
import time
import requests
import pickle
import serial 
import threading
import datetime
#arduino = serial.Serial('/dev/ttyACM0', 9600)



URL_CONTROLLER = "http://127.0.0.1:5000/"


video_capture = cv2.VideoCapture(0)

all_face_encodings = {}
# Load face encodings
with open('./encoded_files/dataset_faces.dat', 'rb') as f:
    all_face_encodings = pickle.load(f)

# Grab the list of names and the list of encodings
known_face_names = list(all_face_encodings.keys())
known_face_encodings = np.array(list(all_face_encodings.values()))


face_locations = []
face_encodings = []
face_names = []


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

def salvar_snapshot(frame):
    img_name = "./snapshots/snapshot_{}.png".format(datetime.datetime.now())
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))

def reconhecer(rgb_small_frame):
    face_encodings = face_recognition.face_encodings(
        rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(
            known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            print(name)
            # x = threading.Thread(target=onOffFunction,args=('on',))
            # x.start()
            # TODO get request para API controller
            # r = requests.get(url = URL_CONTROLLER, params = {'command': "on"})
            # if(r.status_code == 200):
            #    return
        face_names.append(name)
        


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35),
                      (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    font, 1.0, (255, 255, 255), 1)
        
        salvar_snapshot(frame)
    
while True:

    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    if face_locations:
        reconhecer(rgb_small_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
