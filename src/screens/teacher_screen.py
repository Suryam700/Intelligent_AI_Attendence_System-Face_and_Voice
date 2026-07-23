import streamlit as st
import time
from src.components.header import header_dashboard
from src.components.footer import footer
from src.UI.base_layout import style_background_dashboard, style_base_layout
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()
    
    footer("#000")

def teacher_dashboard():
    style_background_dashboard()
    style_base_layout()
    teacher_data = st.session_state.teacher_data

    col1, col2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    
    with col1:
        header_dashboard()
    with col2:
        st.subheader(f"Welcome, {teacher_data['name']}")
        if st.button("Logout", key="loginBackBtn", shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendence"
    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendence' else "tertiary"
        if st.button('Take Attendence', width="stretch", icon=':material/ar_on_you:', type=type1):
            st.session_state.current_teacher_tab = 'take_attendence'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', width="stretch", icon=':material/book_ribbon:', type=type2):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendence_records' else "tertiary"
        if st.button('Attendence Records', width="stretch", icon=':material/cards_stack:', type=type3):
            st.session_state.current_teacher_tab = 'attendence_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendence":
        teacher_tab_take_attendence()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
        pass
    elif st.session_state.current_teacher_tab == "attendence_records":
        teacher_tab_attendence_report()
        
def teacher_tab_take_attendence():
    st.header("Take Attendence")


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns(2)

    with col1:
        st.header("Manage Subjects")
    with col2:
        if st.button("Create New Subjects", width="stretch"):
            create_subject_dialog(teacher_id)

    # list all subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes'])
            ]
        
            def share_btn():
                if st.button(f"Share code: {sub['subject_name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(sub['subject_name'], sub['subject_code'])
                st.space()

            subject_card(
                name=sub['subject_name'],
                code=sub['subject_code'],
                section=sub['subject_section'],
                stats=stats,
                footer_callback=share_btn
            )

    else:
        st.info("NO SUBJECT FOUND! CREATE ONE ABOVE.")

def teacher_tab_attendence_report():
    st.header("Attendence Record")

def login_teacher(username, password):
    if not username or not password:
        return False
    else:
        teacher = teacher_login(username, password)
        if teacher:
            st.session_state.user_role = "teacher"
            st.session_state.teacher_data = teacher
            st.session_state.is_logged_in = True
            return True
        else:
            return False


def teacher_screen_login():
    col1, col2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to Home", key="loginBackBtn", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login with Password", text_alignment="center")
    st.space(); st.space()

    teacher_username = st.text_input("Enter username", placeholder="@suryam")
    teacher_password = st.text_input("Enter password", type="password", placeholder="Enter password")

    st.divider()

    btn1, btn2 = st.columns(2, gap="small")

    with btn1:
        if st.button("Login", shortcut="control+Enter", icon=":material/passkey:", width="stretch"):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome back!", icon="👋"); time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Username and Password combo :(")

    with btn2:
        if st.button("Register Instead", icon=":material/passkey:", width="stretch", type="primary"):
            st.session_state.teacher_login_type = "register"
            st.rerun()

def register_teacher(teacher_username, teacher_name, teacher_password, teacher_confirm_password):
    if not teacher_username or not teacher_name or not teacher_password or not teacher_confirm_password:
        return False, "All detailed's are Required!"
    elif check_teacher_exists(teacher_username):
        return False, "Username already exists"
    elif teacher_password != teacher_confirm_password:
        return False, "Passwords do NOT match!"
    else:
        try:
            create_teacher(teacher_username, teacher_password, teacher_name)
            return True, "✅ Successfully Created! Login Now"
        except Exception as e:
            return False, "Unexpected Error!, Try again."


def teacher_screen_register():
    col1, col2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    
    with col1:
        header_dashboard()
    with col2:
        if st.button("Go back to Home", key="loginBackBtn", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Register your teacher profile")
    st.space(); st.space()

    teacher_username = st.text_input("Enter username", placeholder="@suryam")
    teacher_name = st.text_input("Enter name", placeholder="Suryam Gahoi")
    teacher_password = st.text_input("Enter password", type="password", placeholder="Enter password")
    teacher_confirm_password = st.text_input("Confirm password", type="password", placeholder="Confirm your password")

    st.divider()

    btn1, btn2 = st.columns(2, gap="small")

    with btn1:
        if st.button("Register Now", shortcut="control+Enter", icon=":material/passkey:", width="stretch", type="primary"):
            success, message = register_teacher(teacher_username, teacher_name, teacher_password, teacher_confirm_password)
            if success:
                st.success(message); time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with btn2:
        if st.button("Login Instead", icon=":material/passkey:", width="stretch"):    
            st.session_state.teacher_login_type = "login"
            st.rerun()