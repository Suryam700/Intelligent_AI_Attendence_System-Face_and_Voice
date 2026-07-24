import streamlit as st
from src.database.config import supabase
from src.components.dialog_enroll import enroll_student_to_subject
import time

@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.student_data['student_id']

    response = supabase.table('subjects').select('subject_id, subject_name').eq('subject_code', subject_code).execute()

    if not response:
        st.error("Subject Code not Found! ❌")
        if st.button('Close'):
            st.query_params.clear(); st.rerun()
        return
    else:
        subject = response.data[0]

        check = (supabase.table("subject_students").select("*").eq("subject_id", subject["subject_id"]).eq("student_id", student_id).execute())

        if check.data:
            st.info("You are already Enrolled!")
            if st.button('Got it!'):
                st.query_params.clear(); st.rerun()
            return
        else:
            st.markdown(f"Would You like to enroll in **{subject['subject_name']}**?")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("No Thanks"):
                    st.query_params.clear(); st.rerun()

            with col2:
                if st.button("Yes, Enroll NOW!", type="primary", width="stretch"):
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success("Joined Successfully!")
                    st.query_params.clear()
                    time.sleep(2); st.rerun()

