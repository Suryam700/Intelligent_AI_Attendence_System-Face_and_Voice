import numpy as np
import dlib
from sklearn.svm import SVC
import face_recognition_models
from src.database.db import get_all_students
import streamlit as st

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    face_recog = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, face_recog

def get_face_embeddings(np_image):
    detector, sp, face_recog = load_dlib_models()

    faces = detector(np_image, 1)
    encodings = []

    for face in faces:
        shape = sp(np_image, face)
        face_descriptor = face_recog.compute_face_descriptor(np_image, shape, 1) # => 128D embedding's

        encodings.append(np.array(face_descriptor))

    return encodings

@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None
    else:
        for student in student_db:
            embedding = student.get('face_emedding')
            if embedding:
                X.append(np.array(embedding))
                y.append(student.get('student_id'))
    if len(X) == 0: 
        return 0

    clf = SVC(kernel="linear", probability=True, class_weight="balanced")

    try:
        clf.fit(X, y)
    except ValueError:
        pass

    return {
        'clf': clf,
        'X': X,
        'y': y
    }

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(np_cls_image):
    encodings = get_face_embeddings(np_cls_image)
    
    detected_students = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_students, [], len(encodings)
    
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        student_embedding = X_train(y_train.index(predicted_id))

        best_match_score = np.linalg.norm(student_embedding - encoding)

        resemblance_score = 0.6

        if best_match_score < resemblance_score:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)


