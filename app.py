# app.py
import streamlit as st
from features.email_validator_ui import show_email_validator
from features.email_permutator_ui import show_email_permutator

st.set_page_config(page_title="Email Toolkit", page_icon="📧", layout="wide")

# --- Dark/Light Mode Toggle ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Theme settings
st.session_state.dark_mode = st.get_option("theme.base") == "dark" if st.get_option("theme.base") else st.session_state.dark_mode

# Apply theme styles based on mode
bg_color = "#0e1117" if st.session_state.dark_mode else "#f0f2f6"
card_bg = "#1e1e1e" if st.session_state.dark_mode else "#ffffff"
text_color = "#f1f1f1" if st.session_state.dark_mode else "#000000"
highlight_bg = "#2a2a2a" if st.session_state.dark_mode else "#e6f4ff"

# --- Top Nav with Tabs ---
st.markdown("""
    <style>
    .tab-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
        border-bottom: 1px solid #ccc;
    }
    .tab {
        margin: 0 1rem;
        padding: 1rem 2rem;
        border-radius: 10px 10px 0 0;
        background-color: """ + card_bg + """;
        color: """ + text_color + """;
        text-align: center;
        cursor: pointer;
        transition: 0.3s;
    }
    .tab:hover {
        background-color: """ + highlight_bg + """;
    }
    .active-tab {
        font-weight: bold;
        border-bottom: 3px solid #1a73e8;
    }
    </style>
""", unsafe_allow_html=True)

query_params = st.query_params
selected_tool = query_params.get("tool", "validator")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("📧 Email Validator", key="validator_btn"):
        st.query_params["tool"] = "validator"
        selected_tool = "validator"
with col2:
    if st.button("🧪 Email Permutator", key="permutator_btn"):
        st.query_params["tool"] = "permutator"
        selected_tool = "permutator"

# --- Main Tool Execution ---
st.markdown("<div style='padding-top: 1rem'></div>", unsafe_allow_html=True)

if selected_tool == "validator":
    show_email_validator()
elif selected_tool == "permutator":
    show_email_permutator()