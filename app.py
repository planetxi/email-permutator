# Email Permutator + Verifier using Streamlit
# Requirements: streamlit, validate_email_address (or py3dns, dnspython), smtplib, pandas

import streamlit as st
import pandas as pd
import re
import smtplib
import dns.resolver
from validate_email_address import validate_email

st.set_page_config(page_title="Email Permutator + Verifier", layout="wide")
st.title("📧 Email Permutator + Verifier")

# --- Sidebar ---
st.sidebar.header("Input")
first_name = st.sidebar.text_input("First Name", "John")
middle_name = st.sidebar.text_input("Middle Name (optional)", "")
last_name = st.sidebar.text_input("Last Name", "Doe")
nickname = st.sidebar.text_input("Nickname (optional)", "")
domain = st.sidebar.text_input("Company Domain", "example.com")

# Helper: Nickname mapping
NICKNAME_MAP = {
    "johnathan": "john",
    "michael": "mike",
    "robert": "rob",
    "william": "will",
    "richard": "rich",
    "joseph": "joe",
    "thomas": "tom",
    "james": "jim",
    "daniel": "dan",
    "steven": "steve",
    "andrew": "andy",
}

# --- Permutation Logic ---
def generate_permutations(first, middle, last, domain, nickname=None):
    all_firsts = [first.lower()]
    if first.lower() in NICKNAME_MAP:
        all_firsts.append(NICKNAME_MAP[first.lower()])
    if nickname:
        all_firsts.append(nickname.lower())

    middle = middle.lower() if middle else ""
    last = last.lower()

    patterns = set()
    for f in all_firsts:
        for m in [middle, middle[:1], ""]:
            for l in [last, last[:1], ""]:
                combos = [
                    f"{f}{l}", f"{f}.{l}", f"{f}_{l}", f"{f}{m}{l}", f"{f}.{m}.{l}",
                    f"{l}{f}", f"{l}.{f}", f"{f}{m}", f"{f}{l}{m}", f"{f}{m}{l}"
                ]
                for email in combos:
                    email = re.sub("\.+", ".", email).strip(".")
                    if email:
                        patterns.add(f"{email}@{domain}")

    return sorted(patterns)

# --- Email Verification Logic ---
def verify_email_smtp(email):
    try:
        is_valid = validate_email(email, verify=True)
        return "✅ Valid" if is_valid else "❌ Invalid"
    except:
        return "⚠️ Unknown"

# --- Run ---
if st.sidebar.button("Generate Emails"):
    st.subheader("Generated Email Permutations with Verification")
    emails = generate_permutations(first_name, middle_name, last_name, domain, nickname)

    results = []
    with st.spinner("Verifying emails..."):
        for email in emails:
            status = verify_email_smtp(email)
            results.append({"Email": email, "Status": status})

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)

    # Export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Results as CSV", csv, "verified_emails.csv", "text/csv")
