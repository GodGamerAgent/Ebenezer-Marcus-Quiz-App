import streamlit as st
import os
import base64
import side_bar_disabler
from firebase_ini import get_ref
from datetime import datetime
import time
import uuid

# Check for login/session
if not st.session_state.get("student_logged_in", False):
    st.switch_page("pages/student_login.py")  # or the correct path to your login page

# Only show dashboard if logged in
username = st.session_state.get("username", "NoName")  # NoName is just a fallback, should not show if above check works

if "active_page" not in st.session_state:
    st.session_state.active_page = None

side_bar_disabler.hide_sidebar()

if "questions" not in st.session_state:
    st.session_state.questions = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

def clear_attempt_mode():
    st.session_state["attempt_test_mode"] = False
    st.session_state.pop("attempt_subject", None)
    st.session_state.pop("attempt_test_name", None)
    st.session_state.pop("attempt_test_questions", None)

def attempt_test_page(subject, test_name, questions):
    st.title(f"✏️ Attempting Test: {test_name.capitalize()} ({subject.capitalize()})")
    st.markdown("---")
    total_marks = 0

    # --- FIX: Convert dict to list if necessary, skip non-question keys
    if isinstance(questions, dict):
        # Only keep dict entries that look like questions (have "question" and "options")
        questions = [q for q in questions.values() if isinstance(q, dict) and "question" in q and "options" in q]

    user_answers = []
    with st.form("attempt_whole_test_form"):
        for i, q in enumerate(questions):
            st.markdown(f"**Question {i+1}**")
            st.write(f"{q.get('question','')}, Marks: {q.get('marks','1')}")
            st.write(f"A) {q['options'].get('A','')}")
            st.write(f"B) {q['options'].get('B','')}")
            st.write(f"C) {q['options'].get('C','')}")
            st.write(f"D) {q['options'].get('D','')}")
            answer = st.selectbox(
                f"Answer for Q{i+1}", ["A", "B", "C", "D"], key=f"attempt_answer_{i}"
            )
            user_answers.append(answer)
            st.markdown("---")
        submit = st.form_submit_button("✅ Submit")
    
    if submit:
        for i, q in enumerate(questions):
            correct = q.get("answer", "A")
            marks = int(q.get("marks", 1))
            if user_answers[i] == correct:
                total_marks += marks
        result = [{
            "name": username,
            "marks": total_marks
        }]
        try:
            ref = get_ref(f"Tests/{subject}/{test_name}/result")
            uid = str(uuid.uuid4())
            ref.child(uid).set(result)
            st.success("✅ Test completed successfully!")
            time.sleep(1)
            clear_attempt_mode()
            st.session_state.active_page = "view"
            st.rerun()
        except Exception as e:
            st.error(f"Failed to update test: {e}")

    if st.button("⬅️ Cancel"):
        clear_attempt_mode()
        st.session_state.active_page = "view"
        st.rerun()

def view_test():
    st.title("📚 Subject Selector")
    subjects = ["ENGLISH", "MATHS", "COMPUTER SCIENCE", "PHYSICS", "CHEMISTRY"]
    subject = st.selectbox("Select the Subject", subjects, label_visibility="hidden").lower()

    # For edit mode
    if st.session_state.get("attempt_test_mode", False):
        attempt_test_page(
            st.session_state["attempt_subject"], 
            st.session_state["attempt_test_name"], 
            st.session_state["attempt_test_questions"]
        )
        return

    try:
        ref = get_ref(f"Tests/{subject}")
        tests_dict = ref.get()
        if not tests_dict:
            raise Exception("No tests found")
        test_names = list(tests_dict.keys())
        if subject:
            for i, test_name in enumerate(test_names):
                with st.form(f"sub{i}"):
                    st.write(f"Test Name: {test_name}")
                    edit = st.form_submit_button("✏️Attempt")
                    if edit:
                        st.session_state["attempt_test_mode"] = True
                        st.session_state["attempt_subject"] = subject
                        st.session_state["attempt_test_name"] = test_name
                        st.session_state["attempt_test_questions"] = tests_dict[test_name]
                        st.rerun()
    except Exception:
        with st.form("form"):
            st.header("No Test Available currently")
            reload = st.form_submit_button("Reload")
            if reload:
                st.rerun()
                

def main_page():
    # Get current date and time
    now = datetime.now()
    current_date = now.strftime("%d %B %Y")
    current_time = now.strftime("%I:%M %p")

    # HTML + CSS for top right display
    st.markdown(f"""
        <div style='position: absolute; top: 10px; right: 30px; text-align: right;'>
            <div style="font-weight: 600;">👤 {username}</div>
            <div>{current_date}</div>
            <div>{current_time}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            .block-container {
            margin-left: 0 !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        .stButton>button {
            display: block;
            margin-left: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # Load logo
    logo_path = os.path.join(os.getcwd(), "statics", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <img src="data:image/png;base64,{encoded}" width="200">
        """, unsafe_allow_html=True)
    else:
        st.warning("Logo not found at statics/logo.png")

    st.markdown("<b style='font-size: 54px;'> Welcome to your Dashboard 💻</b>", unsafe_allow_html=True)
    st.markdown("---")
    st.session_state.active_page = "view"
    #st.session_state.active_page = "create"
    
    if st.session_state.active_page == "create":
        #attempt_test()
        pass
    elif st.session_state.active_page == "view":
        view_test()
        #st.info("🔍 Test viewing functionality coming soon...")

main_page()