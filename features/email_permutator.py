import streamlit as st
import pandas as pd
from itertools import product
from services.email_check import validate_email

# 👥 Common name-to-nickname mapping
NICKNAME_MAP = {
    "johnathan": ["john", "jon"],
    "michael": ["mike"],
    "william": ["will", "bill"],
    "robert": ["rob", "bob"],
    "alexander": ["alex"],
    "james": ["jim"],
    "steven": ["steve"],
    "rahul": ["raj"],
    "suresh": ["surya"],
    "deepak": ["dp"]
    # You can expand this list
}

def generate_permutations(first, middle, last, domain, use_nickname=True):
    names = [first, last]
    if middle:
        names.insert(1, middle)

    # Clean inputs
    first = first.lower().strip()
    middle = middle.lower().strip() if middle else ""
    last = last.lower().strip()
    domain = domain.strip().lower()

    first_nicks = [first] + NICKNAME_MAP.get(first.lower(), []) if use_nickname else [first]

    combos = set()

    for fn in first_nicks:
        for pattern in [
            f"{fn}.{last}",
            f"{fn}{last}",
            f"{fn[0]}{last}",
            f"{fn}",
            f"{last}.{fn}",
            f"{last}{fn}",
            f"{fn[0]}.{last[0]}" if fn and last else "",
        ]:
            if pattern:
                combos.add(f"{pattern}@{domain}")

    return sorted(combos)

def show_email_permutator():
    st.subheader("📬 Email Permutator & Validator")

    with st.form("perm_form"):
        col1, col2 = st.columns(2)
        with col1:
            first = st.text_input("First Name*", placeholder="e.g. Johnathan")
            middle = st.text_input("Middle Name (optional)")
            last = st.text_input("Last Name*", placeholder="e.g. Doe")
        with col2:
            domain = st.text_input("Company Domain*", placeholder="e.g. example.com")
            use_nick = st.checkbox("Include Nicknames", value=True)

        submitted = st.form_submit_button("🔄 Generate & Validate")

    if submitted:
        if not first or not last or not domain:
            st.warning("⚠️ Please fill out First Name, Last Name, and Domain.")
            return

        with st.spinner("Generating permutations..."):
            email_combos = generate_permutations(first, middle, last, domain, use_nick)

        with st.spinner("Validating email deliverability..."):
            results = [validate_email(email) for email in email_combos]

        st.success(f"🎉 Generated & validated {len(results)} emails")

        # Display results in a table
        df = pd.DataFrame(results)
        verdict_color = df["Verdict"].map(lambda v: "🟢" if "✅" in v else "🔴")
        df.insert(0, "Status", verdict_color)

        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", data=csv, file_name="validated_emails.csv", mime="text/csv")