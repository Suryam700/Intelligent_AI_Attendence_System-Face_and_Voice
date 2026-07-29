import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_result import show_attendance_results    

@st.dialog("Voice Attendance")
def voice_attendance_dialog(sub_id):
    st.write("Record Audio of Student Say: I'm Present. Then A.I. will recognize the Student's.")

    audio_data = None
    audio_data = st.audio_input('Record Classrom Audio')

    if st.button('Analyze Video', width='stretch', type='primary', icon=':material/frame_inspect:'):
        with st.spinner('Processing Audio Data'):

            enrolled_res = supabase.table('subject_students').select('*, students(*)').eq('subject_id', sub_id).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning('No Student enrolled in this Course')
                return

            candidate_dict = {
                stud['students']['student_id']: stud['students']['voice_embedding'] for stud in enrolled_students if stud['students'].get('voice_embedding')
            }

            if not candidate_dict:
                st.error('No enrolled students have voice Profile registerd')
                return

            audio_bytes = audio_data.read()

            detected_score = process_bulk_audio(audio_bytes, candidate_dict)

            results, attendance_to_log = [], []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node['students']
                score = detected_score.get(student['student_id'], 0.0)
                is_present = bool(score>0)

                results.append({
                    "Name": student['student_name'],
                    "ID": student['student_id'],
                    "score": score if is_present else "-",
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })

                attendance_to_log.append({
                    "student_id": student['student_id'],
                    "subject_id": sub_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present)
                })

            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results

        show_attendance_results(df_results, logs)
