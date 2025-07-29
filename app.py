# app.py
import streamlit as st
from features.email_validator_ui import show_email_validator
from features.email_permutator_ui import show_email_permutator

st.set_page_config(page_title="Email Toolkit", page_icon="📧", layout="wide")

# --- Session State for Dark Mode ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# --- Theme Colors Based on Mode ---
bg_color = "#0e1117" if st.session_state.dark_mode else "#f0f2f6"
card_bg = "#1e1e1e" if st.session_state.dark_mode else "#ffffff"
text_color = "#f1f1f1" if st.session_state.dark_mode else "#000000"
highlight_bg = "#2a2a2a" if st.session_state.dark_mode else "#e6f4ff"

# --- Top Bar with Dark Mode Toggle ---
st.markdown(f"""
    <style>
    .top-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: {bg_color};
        padding: 0.5rem 1rem;
        border-bottom: 1px solid #ccc;
    }}
    .nav-container {{
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        justify-content: center;
    }}
    .nav-box {{
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        background-color: {card_bg};
        color: {text_color};
        width: 300px;
        cursor: pointer;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        text-decoration: none;
    }}
    .nav-box:hover {{
        background-color: {highlight_bg};
    }}
    </style>
""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("### 📬 Email Toolkit")
    with col2:
        st.toggle("🌙 Dark Mode", key="dark_mode")

# --- Navigation UI ---
st.markdown(f"""
<div class="nav-container">
    <a href="?tool=validator" class="nav-box">
        <strong>📧 Email Validator</strong><br>
        Check syntax, MX records & SMTP validity.
    </a>
    <a href="?tool=permutator" class="nav-box">
        <strong>🧪 Email Permutator</strong><br>
        Create and verify email combinations.
    </a>
</div>
""", unsafe_allow_html=True)

# --- Detect URL Param ---
query_params = st.query_params  # Updated from deprecated function
tool = query_params.get("tool", ["validator"])[0]

# --- Load Corresponding Module ---
if tool == "validator":
    show_email_validator()
elif tool == "permutator":
    show_email_permutator()
