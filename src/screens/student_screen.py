import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer
from src.UI.base_layout import style_background_dashboard, style_base_layout
import numpy as np
from PIL import Image

def student_screen():
    style_background_dashboard()
    style_base_layout()

    col1, col2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to Home", key="loginBackBtn", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login using FaceID", text_alignment="center")
    st.space(); st.space()

    photo_source = st.camera_input("Position your Face in the center")
    if photo_source:
        np.array(Image.open(photo_source))

    footer("#000")