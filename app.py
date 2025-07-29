import streamlit as st
import pandas as pd
from itertools import product
import re

# Common nicknames map (simplified and extendable)
nicknames_map = {
    "john": ["johnny", "jon", "johnathan", "johan"],
    "michael": ["mike", "mic", "micky"],
    "james": ["jim", "jimmy"],
    "william": ["bill", "billy", "will"],
    "robert": ["rob", "bobby"],
    "steven": ["steve"],
    "richard": ["rich", "rick"],
    "daniel": ["dan", "danny"],
    "joseph": ["joe", "joey"],
    # Add more as needed
}

# Utility function to generate permutations
def generate_permutations(first, middle, last, domain, nickname=None):
    first = first.lower()
    middle = middle.lower() if middle else ""
    last = last.lower() if last else ""
    domain = domain.lower()

    parts = [first, middle, last]
    initials = [first[0] if first else "", middle[0] if middle else "", last[0] if last else ""]

    all_firsts = [first]
    if first in nicknames_map:
        all_firsts += nicknames_map[first]
    if nickname:
        all_firsts.append(nickname.lower())

    patterns = [
        (f, l) for f in all_firsts for l in [last, last[0], ""]
    ] + [
        (f, m + l) for f in all_firsts for m in [middle, middle[0], ""] for l in [last, last[0], ""]
    ] + [
        (f[0] + l, "") for f in all_firsts for l in [last, last[0], ""]
    ]

    emails = set()
    for f, l in patterns:
        if f and l:
            emails.update([
                f"{f}.{l}@{domain}",
                f"{f}_{l}@{domain}",
                f"{f}{l}@{domain}"
            ])
        elif f:
            emails.update([
                f"{f}@{domain}"
            ])

    return sorted(list(emails))

# Streamlit UI
st.set_page_config(page_title="Email Permutator", layout="centered")
st.title("📬 Email Permutator Tool")

st.markdown("""
Easily generate multiple possible professional email addresses using name inputs.

**Features:**
- Accepts optional nickname
- Adds common first name variants (e.g., John → Johnny, Johan)
- Smart combinations using middle & last name
- Output downloadable as CSV
""")

option = st.radio("Choose Input Mode", ["Single Entry", "Bulk Upload (CSV)"])

if option == "Single Entry":
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name", "John")
        middle_name = st.text_input("Middle Name", "")
        last_name = st.text_input("Last Name", "Doe")
    with col2:
        nickname = st.text_input("Nickname (Optional)", "")
        domain = st.text_input("Domain (without @)", "example.com")

    if st.button("🔄 Generate Emails"):
        emails = generate_permutations(first_name, middle_name, last_name, domain, nickname)
        st.success(f"Generated {len(emails)} email combinations")
        st.dataframe(pd.DataFrame(emails, columns=["Email Permutations"]))

        csv = pd.DataFrame(emails, columns=["Email Permutations"]).to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, file_name="email_permutations.csv", mime="text/csv")

else:
    uploaded_file = st.file_uploader("Upload CSV file with columns: first_name, middle_name, last_name, domain, nickname (optional)", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        all_results = []
        for index, row in df.iterrows():
            emails = generate_permutations(
                row.get("first_name", ""),
                row.get("middle_name", ""),
                row.get("last_name", ""),
                row.get("domain", ""),
                row.get("nickname", None)
            )
            all_results.extend([(row.get("first_name", ""), email) for email in emails])

        df_result = pd.DataFrame(all_results, columns=["Name", "Email Permutations"])
        st.success(f"Generated {len(df_result)} total email combinations.")
        st.dataframe(df_result)

        csv = df_result.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, file_name="bulk_email_permutations.csv", mime="text/csv")
