import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.UI.base_layout import style_background_dashboard, style_base_layout

def teacher_screen():
    header_dashboard()

    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        style_background_dashboard()

    with col2:
        if st.button("Go back to Home", type="primary"):
            st.session_state['login_type'] = None
            st.rerun()

    
    style_base_layout()


    footer_dashboard()

