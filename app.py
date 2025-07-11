import streamlit as st
import base64
import os
import side_bar_disabler

if "student_logged_in" not in st.session_state or "teacher_logged_in" not in st.session_state:
    st.session_state.student_logged_in = False
    st.session_state.Teacher_logged_in = False

elif "student_logged_in" in st.session_state:
    st.switch_page("pages/Student_dashboard.py")



st.set_page_config(page_title="Ebenezer Marcus Quiz Portal")

side_bar_disabler.hide_sidebar()

def main_page():

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

    st.markdown("<b style='font-size: 54px;'> Welcome to Ebenezer Marcus Test Portal</b>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<b style='font-size: 30px;'>Who is this?</b>", unsafe_allow_html=True)

    st.page_link("pages/student_Login.py", label="👨‍🎓 Student", icon="🎓", use_container_width=True)
    st.page_link("pages/teacher_Login.py", label="👩‍🏫 Teacher", icon="📘", use_container_width=True)

main_page()
