import streamlit as st
from services.email_check import validate_email
from features.email_permutator import show_email_permutator
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Sidebar Navigation
st.set_page_config(page_title="Email Toolkit", page_icon="📧", layout="centered")
st.sidebar.title("📚 Tool Selector")
tool = st.sidebar.radio("Choose a Tool:", ["Email Validator", "Email Permutator"])

# --- Email Validator UI ---
def show_email_validator():
    st.subheader("📧 Email Validator Tool")
    st.write("Enter a list of email addresses separated by commas or newlines:")

    user_input = st.text_area("Emails", height=200)

    if st.button("Validate"):
        emails = [e.strip() for e in user_input.replace(',', '\n').split('\n') if e.strip()]
        if not emails:
            st.warning("Please enter at least one email address.")
        else:
            with st.spinner("Validating emails..."):
                with ThreadPoolExecutor(max_workers=10) as executor:
                    results = list(executor.map(validate_email, emails))
                df = pd.DataFrame(results)
                st.success("Validation complete!")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download CSV", data=csv, file_name="results.csv", mime="text/csv")

# Route based on selection
if tool == "Email Validator":
    show_email_validator()
elif tool == "Email Permutator":
    show_email_permutator()
