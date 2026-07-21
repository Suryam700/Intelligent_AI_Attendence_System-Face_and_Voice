import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer
from src.UI.base_layout import style_background_dashboard, style_base_layout
import numpy as np
from PIL import Image
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
import time
from src.database.db import get_all_students, create_student


def student_dashboard():
    style_background_dashboard()
    style_base_layout()
    st.header("Dashboard Here!")

def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    col1, col2 = st.columns(2, gap='xxlarge', vertical_alignment='center')
    
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to Home", key="loginBackBtn", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login using FaceID", text_alignment="center")
    st.space(); st.space()

    show_registration = False
    photo_source = st.camera_input("Position your Face in the center")
    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning..."):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("No face found!")
            elif num_faces > 1:
                st.warning("Multiple faces Found!")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((student for student in all_students if student['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back! {student['name']}")
                        time.sleep(1); st.rerun()
                else:
                    st.info("Face not recognized! You might be a new student!")
                    show_registration = True

    if show_registration:
        with st.container(border=True):
            st.header("Register new Profile")
            new_name = st.text_input("Enter your name: ", placeholder="E.g. Suryam Gahoi")
            
            st.subheader("Optinal: Voice Enrollment")
            st.info("Enroll your voice for voice-only attendance.")
             
            audio_data = None

            try:
                audio_data = st.audio_input("Record a short phrase like 'I'm present, My name is Suryam Gahoi.'")
            except Exception as e:
                st.error("Audio not fetch!")

            if st.button("Create Account", type="primary"):
                if new_name:
                    with st.spinner("Creating Profile..."):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()    
                            voice_emb = None
                            if audio_data: 
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_embedding=face_emb , voice_embedding=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile Created! Hi, {new_name}")
                                time.sleep(1); st.rerun()
                        else:
                            st.error("Couldn't Capture your facial features for registration")
                    
                else:
                    st.warning("Please enter your name!")
            

    footer("#000")