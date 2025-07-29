import streamlit as st
import pandas as pd
from itertools import product

NICKNAME_MAP = {
    "johnathan": ["john", "jon"],
    "michael": ["mike"],
    "william": ["will", "bill"],
    "robert": ["rob", "bob"],
    "alexander": ["alex"],
    "james": ["jim"],
    "steven": ["steve"],
    "rahul": ["raj"]
    # Add more as needed
}

def generate_permutations(first, middle, last, domain, use_nickname=True):
    names = [first]
    if middle:
        names.append(middle)
    if last:
        names.append(last)

    nicknames = NICKNAME_MAP.get(first.lower(), []) if use_nickname else []
    parts = [first, middle, last] if middle else [first, last]
    parts = [p.lower() for p in parts if p]

    base_combos = list({
        f"{f}.{l}" for f, l in product([first] + nicknames, [last])
    } | {
        f"{f}{l}" for f, l in product([first] + nicknames, [last])
    } | {
        f"{f[0]}{l}" for f, l in product([first] + nicknames, [last])
    } | {
        f"{f}" for f in [first] + nicknames
    })

    return [f"{combo}@{domain}" for combo in base_combos]

def show_email_permutator():
    st.subheader("📬 Email Permutator Tool")
    st.write("Generate possible email combinations from a person's name and domain.")

    col1, col2 = st.columns(2)
    with col1:
        first = st.text_input("First Name")
        middle = st.text_input("Middle Name (optional)")
        last = st.text_input("Last Name")

    with col2:
        domain = st.text_input("Domain (example.com)")
        use_nick = st.checkbox("Include Nickname Variations", value=True)

    if st.button("Generate Emails"):
        if not first or not last or not domain:
            st.warning("Please enter at least first name, last name, and domain.")
        else:
            emails = generate_permutations(first, middle, last, domain, use_nick)
            st.success(f"Generated {len(emails)} combinations.")
            df = pd.DataFrame(emails, columns=["Email"])
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", data=csv, file_name="permutations.csv", mime="text/csv")
