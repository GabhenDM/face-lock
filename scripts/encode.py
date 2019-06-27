import face_recognition
import pickle
import os


def encode():
    all_face_encodings = {}

    for file in os.listdir('./training_images'):
        print("[+] Encoding Face -  " + file[:-4])
        img = face_recognition.load_image_file('./training_images/'+file)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            all_face_encodings[file[:-4]] = encodings[0]


    with open('./encoded_files/dataset_faces.dat', 'wb') as f:
        pickle.dump(all_face_encodings, f)
