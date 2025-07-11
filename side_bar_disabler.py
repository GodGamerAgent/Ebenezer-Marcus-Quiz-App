import streamlit as st

def hide_sidebar():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    st.markdown("""
        <style>
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)