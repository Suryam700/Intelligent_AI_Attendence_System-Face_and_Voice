import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer
from src.UI.base_layout import style_background_dashboard, style_base_layout

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    col1, col2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to Home", key="loginBackBtn", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()


    if "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()
    

    footer("#000")

def teacher_screen_login():
    st.header("Login with Password", text_alignment="center")
    st.space(); st.space()

    teacher_username = st.text_input("Enter username", placeholder="@suryam")
    teacher_password = st.text_input("Enter password", type="password", placeholder="Enter password")

    st.divider()

    btn1, btn2 = st.columns(2, gap="small")

    with btn1:
        st.button("Login", shortcut="control+Enter", icon=":material/passkey:", width="stretch")   
    with btn2:
        if st.button("Register Instead", icon=":material/passkey:", width="stretch", type="primary"):
            st.session_state.teacher_login_type = "register"
            st.rerun()


def teacher_screen_register():
    st.header("Register your teacher profile")
    st.space(); st.space()

    teacher_username = st.text_input("Enter username", placeholder="@suryam")
    teacher_name = st.text_input("Enter name", placeholder="Suryam Gahoi")
    teacher_password = st.text_input("Enter password", type="password", placeholder="Enter password")
    teacher_confirm_password = st.text_input("Confirm password", type="password", placeholder="Confirm your password")

    st.divider()

    btn1, btn2 = st.columns(2, gap="small")

    with btn1:
        st.button("Register Now", shortcut="control+Enter", icon=":material/passkey:", width="stretch", type="primary")
    with btn2:
        if st.button("Login Instead", icon=":material/passkey:", width="stretch"):    
            st.session_state.teacher_login_type = "login"
            st.rerun()