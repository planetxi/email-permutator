# app.py
import streamlit as st
from features.email_validator_ui import show_email_validator
from features.email_permutator_ui import show_email_permutator

st.set_page_config(page_title="Email Toolkit", page_icon="📧", layout="wide")

# --- Minimal Tab Navigation ---
tool_option = st.radio(
    "Choose Tool",
    ["Email Validator", "Email Permutator"],
    horizontal=True
)

# --- Main Content Switch ---
if tool_option == "Email Validator":
    show_email_validator()
else:
    show_email_permutator()
