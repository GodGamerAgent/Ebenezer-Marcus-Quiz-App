import streamlit as st
import os
import base64
import side_bar_disabler
from firebase_ini import get_ref
from datetime import datetime
import time
import pandas as pd

if "active_page" not in st.session_state:
    st.session_state.active_page = None


side_bar_disabler.hide_sidebar()

if "questions" not in st.session_state:
    st.session_state.questions = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

def clear_edit_mode():
    st.session_state["edit_test_mode"] = False
    st.session_state.pop("edit_subject", None)
    st.session_state.pop("edit_test_name", None)
    st.session_state.pop("edit_test_questions", None)

def create_test():
    
    test_name = st.text_input("Test Name")
    subject = st.selectbox("Subject", ["English", "Tamil", "Physics", "Chemistry", "Maths", "Biology"]).lower()

    # ✅ If editing, pre-fill the form
    editing = st.session_state.edit_index is not None
    edit_data = (
        st.session_state.questions[st.session_state.edit_index]
        if editing
        else {"question": "", "options": {"A": "", "B": "", "C": "", "D": ""}, "answer": "A", "mark":""}
    )

    # ✅ Form for adding/editing
    with st.form("question_form", clear_on_submit=not editing):
        question = st.text_input("Enter Question", value=edit_data["question"])
        col1, col2 = st.columns(2)
        with col1:
            option_a = st.text_input("Option A", value=edit_data["options"]["A"])
            option_b = st.text_input("Option B", value=edit_data["options"]["B"])
        with col2:
            option_c = st.text_input("Option C", value=edit_data["options"]["C"])
            option_d = st.text_input("Option D", value=edit_data["options"]["D"])
        answer = st.selectbox("Correct Answer", ["A", "B", "C", "D"], index=["A", "B", "C", "D"].index(edit_data["answer"]))
        marks = st.slider("📑Marks")

        submitted = st.form_submit_button("💾 Update" if editing else "➕ Add Question")

    # ✅ Add or update logic
    if submitted:
        new_question = {
            "question": question,
            "options": {
                "A": option_a,
                "B": option_b,
                "C": option_c,
                "D": option_d,
            },
            "answer": answer,
            "marks": marks
        }

        if editing:
            st.session_state.questions[st.session_state.edit_index] = new_question
            st.success(f"✅ Question {st.session_state.edit_index + 1} updated!")
            st.session_state.edit_index = None  # exit edit mode
        else:
            st.session_state.questions.append(new_question)
            st.success("✅ Question added!")

    # ✅ Show questions with Edit buttons
    st.markdown("### 📋 Questions Preview")

    if st.session_state.questions:
        for i, q in enumerate(st.session_state.questions):
            st.markdown(f"**{i+1}. {q['question']}**")
            for key, val in q["options"].items():
                st.markdown(f"- {key}) {val}")
            st.markdown(f"✅ Correct Answer: **{q['answer']}**")
            st.markdown(f"📑Marks: **{q["marks"]}**")

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"✏️ Edit", key=f"edit_{i}"):
                    st.session_state.edit_index = i
                    st.rerun()
            with col2:
                if st.button(f"🗑️ Delete", key=f"delete_btn_{i}"):
                    st.session_state.questions.pop(i)
                    st.session_state.edit_index = None
                    st.success(f"❌ Question {i+1} deleted.")
                    st.rerun()
    
            st.markdown("---")
    else:
        st.info("No questions added yet.")
    
    # ✅ Clear all button
    if st.button("🔄 Clear All Questions"):
        st.session_state.questions = []
        st.session_state.edit_index = None
        st.warning("All questions cleared.")

    #submit button + database handling
    if st.button("✅ Submit"):
        qq = st.session_state.questions
        for i in range(len(qq)):
            if qq[i]["question"] == "":
                st.error(f"Question field is empty for question No: {i+1}")
            options = qq[i]["options"]
            if "" in [options["A"], options["B"], options["C"], options["D"]]:
                st.error(f"check if all the options are filled for question No: {i+1}")
            answer = qq[i]["answer"]
            if answer not in ["A", "B", "C", "D"]:
                st.error(f"Invalid Answer has been selected for question No: {i+1}")
        if test_name == "":
            st.error("Please Fill the Test Name")
        elif st.session_state.questions == []:
            st.error("Please Add the questions")
        else:
            try:
                ref = get_ref(f"Tests/{subject}")
                ref.child(test_name).set(
                    st.session_state.questions
                )
                st.session_state.questions = []
                st.session_state.edit_index = None
                sucs = st.success("✅Test Created Succesfull")
                time.sleep(1)
                sucs.empty()
                st.rerun()

            except Exception as e:
                st.error(f"error: {e}")

def edit_test_page(subject, test_name, questions):
    # --- Normalize ---
    if isinstance(questions, dict):
        questions = [q for q in questions.values() if isinstance(q, dict) and "question" in q]
    elif isinstance(questions, list):
        questions = [q for q in questions if isinstance(q, dict) and "question" in q]
    else:
        questions = []
    
    st.title(f"✏️ Editing Test: {test_name.capitalize()} ({subject.capitalize()})")
    st.markdown("---")
    edited_questions = []

    with st.form("edit_whole_test_form"):
        for i, q in enumerate(questions):
            st.markdown(f"**Question {i+1}**")
            question = st.text_input(f"Question {i+1}", value=q["question"], key=f"edit_q_{i}")
            option_a = st.text_input(f"Option A ({i+1})", value=q["options"]["A"], key=f"edit_a_{i}")
            option_b = st.text_input(f"Option B ({i+1})", value=q["options"]["B"], key=f"edit_b_{i}")
            option_c = st.text_input(f"Option C ({i+1})", value=q["options"]["C"], key=f"edit_c_{i}")
            option_d = st.text_input(f"Option D ({i+1})", value=q["options"]["D"], key=f"edit_d_{i}")
            answer = st.selectbox(
                f"Correct Answer ({i+1})", ["A", "B", "C", "D"], 
                index=["A", "B", "C", "D"].index(q["answer"]),
                key=f"edit_ans_{i}"
            )
            marks = st.slider(f"Marks {i+1}", value=q["marks"], key=f"edit_mark{i}")
            st.markdown("---")
            edited_questions.append({
                "question": question,
                "options": {
                    "A": option_a,
                    "B": option_b,
                    "C": option_c,
                    "D": option_d,
                },
                "answer": answer,
                "marks": marks
            })
        save = st.form_submit_button("💾 Save Changes")
    if save:
        # Save edited questions to database
        try:
            ref = get_ref(f"Tests/{subject}")
            ref.child(test_name).set(edited_questions)
            st.success("✅ Test updated successfully!")
            time.sleep(1)
            clear_edit_mode()
            st.session_state.active_page = "view"
            st.rerun()
        except Exception as e:
            st.error(f"Failed to update test: {e}")

    st.markdown("### Danger Zone")
    if st.button("🗑️ Delete This Test"):
        try:
            ref = get_ref(f"Tests/{subject}")
            ref.child(test_name).delete()
            st.warning("❌ Test deleted successfully!")
            time.sleep(1)
            clear_edit_mode()
            st.session_state.active_page = "view"
            st.rerun()
        except Exception as e:
            st.error(f"Failed to delete test: {e}")

    if st.button("⬅️ Cancel"):
        clear_edit_mode()
        st.session_state.active_page = "view"
        st.rerun()


def view_test():
    st.title("📚 Subject Selector")
    subjects = ["ENGLISH", "MATHS", "COMPUTER SCIENCE", "PHYSICS", "CHEMISTRY"]
    subject = st.selectbox("Select the Subject", subjects, label_visibility="hidden").lower()

    # For edit mode
    if st.session_state.get("edit_test_mode", False):
        edit_test_page(
            st.session_state["edit_subject"], 
            st.session_state["edit_test_name"], 
            st.session_state["edit_test_questions"]
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
                form_key = f"sub{i}"
                with st.form(form_key):
                    st.write(f"Test Name: {test_name}")
                    col1, col2 = st.columns(2)
                    with col1:
                        edit = st.form_submit_button("✏️Edit")
                    with col2:
                        get_result = st.form_submit_button("📥 Get Result")

                    if edit:
                        st.session_state["edit_test_mode"] = True
                        st.session_state["edit_subject"] = subject
                        st.session_state["edit_test_name"] = test_name
                        st.session_state["edit_test_questions"] = tests_dict[test_name]
                        st.rerun()
                    if get_result:
                        st.session_state['result_submitted'] = True
                        st.session_state['result_subject'] = subject
                        st.session_state['result_test_name'] = test_name
                        st.rerun()

                # OUTSIDE the form:
                if (
                    st.session_state.get('result_submitted', False) and 
                    st.session_state.get('result_subject') == subject and 
                    st.session_state.get('result_test_name') == test_name
                ):
                    try:
                        ref = get_ref(f"Tests/{subject}/{test_name}/result")
                        result = ref.get()
                        if not result:
                            st.warning("No result available for this test.")
                        else:
                            # result is probably a dict of uuid -> [dict(name, marks)]
                            records = []
                            if isinstance(result, dict):
                                for v in result.values():
                                    # v is a list of dicts (as per your result = [{...}] in Student_dashboard.py)
                                    if isinstance(v, list):
                                        for entry in v:
                                            records.append(entry)
                                    elif isinstance(v, dict):
                                        records.append(v)
                            elif isinstance(result, list):
                                records = result
                            else:
                                st.error("Unexpected result data format.")
                                records = []

                            if records:
                                df = pd.DataFrame(records)
                                csv = df.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label="Download result as CSV",
                                    data=csv,
                                    file_name=f"{test_name}_results.csv",
                                    mime="text/csv"
                                )
                            else:
                                st.warning("No valid results to download.")
                            # Clear session state after showing download
                            st.session_state['result_submitted'] = False
                            st.session_state['result_subject'] = None
                            st.session_state['result_test_name'] = None
                    except Exception as e:
                        st.error(f"Failed to get result: {e}")
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


    # Safely get the username, fallback to "Guest"
    username = st.session_state.get("username") or st.session_state.get("Guest")

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
    col1, col2 = st.columns(2)
    with col1:
        if st.button("View available Test📝"):
            st.session_state.active_page = "view"

    with col2:
        if st.button("Create Test⚡"):
            st.session_state.active_page = "create"
    
    if st.session_state.active_page == "create":
        create_test()
    elif st.session_state.active_page == "view":
        view_test()
        #st.info("🔍 Test viewing functionality coming soon...")



main_page()