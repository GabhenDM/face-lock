import face_recognition
import pickle
import os
import sys

sys.path.append(".")


from facelock.models import Usuario
from facelock import db
def encode():
    all_face_encodings = {}
   
    for file in os.listdir('./training_images'):
        print("[+] Encoding Face -  " + file[:-4])
        img = face_recognition.load_image_file('./training_images/'+file)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            all_face_encodings[file[:-4]] = encodings[0]
            face_pickled_data = pickle.dumps(encodings[0])
            usuario = Usuario.query.filter_by(nome=file[:-4]).first()
            if(usuario):
                usuario.encoding = face_pickled_data
                db.session.commit()
    with open('./encoded_files/dataset_faces.dat', 'wb') as f:
        pickle.dump(all_face_encodings, f)

if __name__ == '__main__':
    encode()