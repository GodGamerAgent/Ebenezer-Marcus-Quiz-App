import streamlit as st
import base64
import os
import side_bar_disabler
from firebase_ini import get_ref


if "teacher_logged_in" not in st.session_state:
    st.session_state.teacher_logged_in = False

if st.session_state.teacher_logged_in:
    st.switch_page("pages/teacher_dashboard.py")

def login_page(heading,stat):
    # Inject CSS styling
    st.markdown("""
        <style>
            .login-title {
                font-size: 24px;
                font-weight: 600;
                text-align: center;
                margin-bottom: 1.5rem;
                color: white;
            }
            stTextInput, .stPasswordInput, .stCheckbox {
                padding-top: 0.5rem;
                padding-bottom: 0.5rem;
            }
        </style>
        """, unsafe_allow_html=True)
    
    left_col, center_col, right_col = st.columns([3, 2, 3]) 

    # Start login card container
    
    st.markdown(f'<div class="login-title">{heading}</div>', unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    st.write("")
    st.write("")

    register_button = st.button("🔐Login", use_container_width=True)
    
    if register_button:
        if not username or not password:
            st.error("Please fill in both username and password.")
        else:
            try:
                user_ref = get_ref(f"users/{username}")
                user_data = user_ref.get()
                
                if user_data is None:
                    st.error("❌ User not found.")
                elif user_data["password"] == password and user_data["status"] == stat:
                    st.success("✅ Login successful!")
                    st.session_state.teacher_logged_in = True
                    st.session_state.username = username
                    st.switch_page(f"pages/{stat}_dashboard.py")
                
                else:
                    st.error("❌ Incorrect credentials")

            except Exception as e:
                st.error(f"🔥 Error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def starter():
    # Load logo
    logo_path = os.path.join(os.getcwd(), "statics", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <img src="data:image/png;base64,{encoded}" width="50">
        """, unsafe_allow_html=True)
    else:
        st.warning("Logo not found at statics/logo.png")
    st.markdown("<b style='font-size: 54px;'>Welcome to🏫Teacher Login page</b>", unsafe_allow_html=True)
    st.divider()
    login_page("Login 👇","Teacher")

side_bar_disabler.hide_sidebar()

starter()