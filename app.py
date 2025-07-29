# app.py
import streamlit as st
from features.email_validator_ui import show_email_validator
from features.email_permutator_ui import show_email_permutator

st.set_page_config(page_title="Email Toolkit", page_icon="📧", layout="wide")

# --- Dark/Light Mode Toggle ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Theme toggle button
mode_toggle = st.toggle("🌗 Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = mode_toggle

# Apply theme styles based on mode
bg_color = "#0e1117" if st.session_state.dark_mode else "#f0f2f6"
card_bg = "#1e1e1e" if st.session_state.dark_mode else "#ffffff"
text_color = "#f1f1f1" if st.session_state.dark_mode else "#000000"
highlight_bg = "#2a2a2a" if st.session_state.dark_mode else "#e6f4ff"

# --- Simple Tab Toggle ---
tool_option = st.radio(
    "Select Tool:",
    ["Email Validator", "Email Permutator"],
    horizontal=True,
    index=0 if st.query_params.get("tool", "validator") == "validator" else 1
)

selected_tool = "validator" if tool_option == "Email Validator" else "permutator"
st.query_params["tool"] = selected_tool

# --- Main Tool Execution ---
st.markdown(f"""
    <style>
    body {{ background-color: {bg_color}; color: {text_color}; }}
    .stApp {{ background-color: {bg_color}; }}
    </style>
""", unsafe_allow_html=True)

if selected_tool == "validator":
    show_email_validator()
elif selected_tool == "permutator":
    show_email_permutator()
