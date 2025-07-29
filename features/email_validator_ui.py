import streamlit as st

def show_email_validator():
    st.header("📧 Email Validator")
    st.write("Paste email addresses below to validate.")
    emails = st.text_area("Enter emails (one per line)")
    if st.button("Validate"):
        st.success("Validation results will appear here.")
