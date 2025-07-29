# app.py
import streamlit as st
from features.email_validator_ui import show_email_validator
from features.email_permutator_ui import show_email_permutator

st.set_page_config(page_title="Email Toolkit", page_icon="📧", layout="wide")

# --- Top Nav-like Section ---
st.markdown("""
    <style>
    .nav-container {
        display: flex;
        justify-content: space-around;
        background-color: #f0f2f6;
        padding: 1rem 0;
        border-bottom: 1px solid #d3d3d3;
        margin-bottom: 2rem;
    }
    .nav-box {
        text-align: center;
        padding: 1rem;
        width: 45%;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: 0.2s;
    }
    .nav-box:hover {
        background-color: #e6f4ff;
    }
    </style>

    <div class="nav-container">
        <div class="nav-box">
            <strong>📧 Email Validator</strong><br>
            Paste emails to check syntax, MX records, SMTP status, etc.
        </div>
        <div class="nav-box">
            <strong>🧪 Email Permutator</strong><br>
            Generate combinations from names + domains & validate deliverability.
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("🧰 Email Toolkit")
tool = st.sidebar.radio(
    "Select a Tool",
    ["📧 Email Validator", "🧪 Email Permutator"]
)

# --- Main Tool Execution ---
if tool == "📧 Email Validator":
    show_email_validator()
elif tool == "🧪 Email Permutator":
    show_email_permutator()
