# app.py
import streamlit as st
from features.email_validator_ui import show_email_validator
from features.email_permutator_ui import show_email_permutator

st.set_page_config(page_title="Email Toolkit", page_icon="📧", layout="wide")

# --- Dark/Light Mode Toggle ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.session_state.dark_mode = st.toggle("🌙 Dark Mode")

# Apply theme styles based on mode
bg_color = "#0e1117" if st.session_state.dark_mode else "#f0f2f6"
card_bg = "#1e1e1e" if st.session_state.dark_mode else "#ffffff"
text_color = "#f1f1f1" if st.session_state.dark_mode else "#000000"
highlight_bg = "#2a2a2a" if st.session_state.dark_mode else "#e6f4ff"

# --- Top Nav-like Section with Clickable Navigation ---
st.markdown(f"""
    <style>
    .nav-container {{
        display: flex;
        justify-content: space-around;
        background-color: {bg_color};
        padding: 1rem 0;
        border-bottom: 1px solid #d3d3d3;
        margin-bottom: 2rem;
    }}
    .nav-box {{
        text-align: center;
        padding: 1rem;
        width: 45%;
        border-radius: 10px;
        background-color: {card_bg};
        color: {text_color};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: 0.2s;
        cursor: pointer;
    }}
    .nav-box:hover {{
        background-color: {highlight_bg};
    }}
    </style>

    <div class="nav-container">
        <a href="?tool=validator" style="text-decoration: none; color: inherit;">
            <div class="nav-box">
                <strong>📧 Email Validator</strong><br>
                Paste emails to check syntax, MX records, SMTP status, etc.
            </div>
        </a>
        <a href="?tool=permutator" style="text-decoration: none; color: inherit;">
            <div class="nav-box">
                <strong>🧪 Email Permutator</strong><br>
                Generate combinations from names + domains & validate deliverability.
            </div>
        </a>
    </div>
""", unsafe_allow_html=True)

# --- Determine Tool via URL Parameter ---
query_params = st.experimental_get_query_params()
tool = query_params.get("tool", ["validator"])[0]

# --- Main Tool Execution ---
if tool == "validator":
    show_email_validator()
elif tool == "permutator":
    show_email_permutator()