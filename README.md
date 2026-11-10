# SnapClass — AI Attendance with Face and Voice

SnapClass is a classroom attendance app built with Streamlit. Teachers can create subjects, share a class code or join link, and take attendance from classroom photos or a voice recording. Students can sign in with their face, join subjects, and check their attendance history.

**Try the deployed app:** [snapclass-attendance-system-face-and-voice.streamlit.app](https://snapclass-attendance-system-face-and-voice.streamlit.app)

## What you can do

### Teachers

- Create an account with a username, name, and password, then sign in.
- Create subjects with a code, name, and section.
- Share a subject code, QR code, or link so students can enroll.
- Take attendance by capturing or uploading classroom photos. The app detects faces and matches them against saved student profiles, then reports attendance for the selected subject's roster.
- Take attendance from a classroom audio recording when students have enrolled voice profiles.
- Review the proposed attendance before saving it, and view attendance records grouped by class session.

### Students

- Create a profile by capturing a face photo. A short voice recording can also be added for voice attendance.
- Sign in by taking a camera photo.
- Enroll in a subject with its code, or open a teacher's join link and accept the enrollment.
- See enrolled subjects and attendance totals, and unenroll from a subject.

Attendance results are shown for review before they are saved. Face and voice matching depend on the quality of the captured image or audio and the student's enrolled profile.

## How the project is organized

```text
.
├── app.py                          # Streamlit entry point and portal routing
├── requirements.txt                # Python dependencies
└── src/
    ├── UI/                          # Shared page styling
    ├── components/                  # Headers, subject cards, and dialogs
    ├── database/                    # Supabase client and database operations
    ├── pipelines/                   # Face and voice recognition
    └── screens/                     # Home, teacher, and student screens
```

The app stores teacher accounts, student profiles, subjects, enrollments, and attendance logs in Supabase. Face profiles are stored as face embeddings; optional voice profiles are stored as voice embeddings. Teacher passwords are hashed with `bcrypt` before they are saved.

## Run it locally

### Requirements

- Python 3.10 or newer is recommended.
- A Supabase project with the tables and relationships described below.
- A webcam and microphone for the camera and audio features. Browser permission is required when prompted.

The face-recognition packages include native components, so installation can take longer than a typical Streamlit app. `dlib-bin` is included in the requirements to provide a prebuilt dlib package where supported.

### 1. Get the code and install dependencies

```bash
git clone https://github.com/Suryam700/Intelligent_AI_Attendence_System-Face_and_Voice.git
cd Intelligent_AI_Attendence_System-Face_and_Voice
python -m venv .venv
```

Activate the virtual environment, then install the packages:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure Supabase

Create a Supabase project and add the following values to `.streamlit/secrets.toml` in the project root:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-api-key"
```

The app reads these values using Streamlit secrets. Keep the file private; it should not be committed to source control. For a Streamlit Community Cloud deployment, add the same two values in the app's **Settings → Secrets** page.

The database needs these tables and fields. Use integer identity/primary-key columns for the `*_id` fields that identify teachers, students, and subjects, and add foreign keys for the relationships so Supabase can return the related records used by the app.

| Table | Fields used by the app |
| --- | --- |
| `teachers` | `teacher_id`, `username`, `password`, `teacher_name` |
| `students` | `student_id`, `student_name`, `face_embedding` (JSON/array), `voice_embedding` (JSON/array, nullable) |
| `subjects` | `subject_id`, `subject_code`, `subject_name`, `subject_section`, `teacher_id` |
| `subject_students` | `student_id`, `subject_id` |
| `attendance_logs` | `student_id`, `subject_id`, `timestamp`, `is_present` (boolean) |

Set up foreign keys from `subjects.teacher_id` to `teachers.teacher_id`, from `subject_students` to both `students` and `subjects`, and from `attendance_logs` to both `students` and `subjects`. The app uses these relationships for its nested Supabase queries. The source repository does not include a database migration or SQL schema, so create the tables and constraints in your Supabase project before running the app.

### 3. Start the app

```bash
streamlit run app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`). Open it in a browser. The camera and microphone controls work through browser permissions; use a secure deployed URL or localhost for device access.

## Typical first-time flow

1. A teacher opens **Teacher Portal**, registers, and signs in.
2. The teacher creates a subject and shares its code or join link.
3. A student opens **Student Portal**, captures a face photo, and creates a profile. They can optionally record a voice sample during registration.
4. The student enrolls using the subject code, or follows the shared link and accepts the prompt.
5. The teacher selects the subject, captures/uploads photos or records classroom audio, and reviews the attendance results.
6. The teacher confirms the results to save them. Students can then see their attendance totals in their portal.

## Main dependencies

- **Streamlit** for the web interface
- **Supabase** for application data
- **dlib**, `face_recognition_models`, **NumPy**, and **scikit-learn** for face embeddings and matching
- **Resemblyzer** and **librosa** for voice embeddings and audio processing
- **Pandas** for attendance summaries

The full package list is in [`requirements.txt`](requirements.txt).

## Notes

- This is an attendance aid, and recognition can make mistakes. Review the proposed attendance before confirming it.
- Voice attendance is available only for students who have a saved voice profile.
- Protect the Supabase credentials and the face and voice profile data. Configure database access policies to suit your deployment and intended users.
- Some recognition packages rely on platform-specific native binaries. If installation fails, check that your Python version and operating system are supported by the `dlib-bin` and other packages in `requirements.txt`.
