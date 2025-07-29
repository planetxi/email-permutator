# app.py
import streamlit as st
from features.email_validator_ui import show_email_validator
from features.email_permutator_ui import show_email_permutator

st.set_page_config(page_title="Email Toolkit", page_icon="📧", layout="wide")

# --- Session Defaults ---
if "tool" not in st.session_state:
    st.session_state.tool = "validator"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# --- Dark Mode Styles ---
dark_mode = st.session_state.dark_mode
bg_color = "#0e1117" if dark_mode else "#f0f2f6"
card_bg = "#1e1e1e" if dark_mode else "#ffffff"
text_color = "#f1f1f1" if dark_mode else "#000000"
highlight_bg = "#2a2a2a" if dark_mode else "#e6f4ff"

# --- Dark Mode Toggle + Nav on Top ---
st.markdown(f"""
    <style>
    .top-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background-color: {bg_color};
        border-bottom: 1px solid #ccc;
        margin-bottom: 2rem;
    }}
    .nav-buttons {{
        display: flex;
        gap: 1rem;
    }}
    .nav-btn {{
        padding: 0.75rem 1.5rem;
        background-color: {card_bg};
        color: {text_color};
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: 0.2s;
        font-weight: bold;
    }}
    .nav-btn:hover {{
        background-color: {highlight_bg};
    }}
    </style>

    <div class="top-bar">
        <div class="nav-buttons">
            <form action="" method="post">
                <button name="tool" value="validator" class="nav-btn">📧 Email Validator</button>
                <button name="tool" value="permutator" class="nav-btn">🧪 Email Permutator</button>
            </form>
        </div>
        <form action="" method="post">
            <button name="toggle_dark" class="nav-btn">🌙 { "Light Mode" if dark_mode else "Dark Mode" }</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# --- Handle Form Inputs (POST buttons) ---
if st.experimental_get_query_params().get("tool"):
    st.session_state.tool = st.experimental_get_query_params()["tool"][0]

if "toggle_dark" in st.experimental_get_query_params():
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.experimental_set_query_params()  # Clean up URL after toggle

# --- Show Tool ---
if st.session_state.tool == "validator":
    show_email_va
