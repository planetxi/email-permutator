# app.py
import streamlit as st
from features.email_validator_ui import show_email_validator
from features.email_permutator_ui import show_email_permutator

st.set_page_config(page_title="Email Toolkit", page_icon="📧", layout="wide")

# --- Force Day Mode ---
st.session_state.dark_mode = False  # Override to force day mode

# Apply theme styles based on mode
bg_color = "#f0f2f6"
card_bg = "#ffffff"
text_color = "#000000"
highlight_bg = "#e6f4ff"

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
