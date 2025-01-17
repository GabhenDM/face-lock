

import face_recognition
import pickle
import os
import sys

sys.path.append(".")
from facelock.models import Usuario
from facelock import db

def encode():
    all_face_encodings = {}
    print("[+] Starting Encoding of files...")
    print("[+] Files Found: ", os.listdir('./training_images'))
    for file in os.listdir('./training_images'):
        img = face_recognition.load_image_file('./training_images/'+file)
        usuario = Usuario.query.filter_by(nome=file[:-4]).first()
        if(usuario and usuario.encoding is None):
            print("[+] Encoding Face -  " + file[:-4])
            encodings = face_recognition.face_encodings(img)
            if encodings:
                all_face_encodings[file[:-4]] = encodings[0]
                face_pickled_data = pickle.dumps(encodings[0])
                usuario.encoding = face_pickled_data
                db.session.commit()
    with open('./encoded_files/dataset_faces.dat', 'wb') as f:
        pickle.dump(all_face_encodings, f)


if __name__ == '__main__':
    encode()
