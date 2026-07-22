import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of new subjects")
    sub_id = st.text_input("Subject Code", placeholder="CS201")
    sub_name = st.text_input("Subject Name", placeholder="introduction to M.L.")
    sub_section = st.text_input("Subject Section", placeholder="A")

    if st.button("Create subject Now", type="primary", width="stretch"):
        if sub_id and sub_name and sub_section:
            try:
                st.toast("Subject Create Successfully!")
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill all the feilds!")
        
