import streamlit as st
import re
import dns.resolver
import socket

# --- Nickname Mapping ---
nickname_dict = {
    "johnathan": ["john", "jon", "johnny", "johan"],
    "michael": ["mike", "micky"],
    "william": ["will", "bill", "willy"],
    "james": ["jim", "jimmy"],
    "robert": ["rob", "bob", "bobby"],
    "richard": ["rich", "rick", "ricky", "dick"],
    "joseph": ["joe", "joey"],
    "charles": ["charlie", "chuck"],
    "daniel": ["dan", "danny"],
    "steven": ["steve"],
}


# --- Email Permutation Logic ---
def generate_permutations(first, middle, last, domain, nickname=None):
    permutations = set()
    separators = ["", ".", "-", "_"]

    first = first.lower().strip()
    middle = middle.lower().strip() if middle else ""
    last = last.lower().strip() if last else ""
    domain = domain.lower().strip()

    all_firsts = [first, first[0]]
    if nickname:
        all_firsts.append(nickname.lower().strip())
    if first in nickname_dict:
        all_firsts.extend(nickname_dict[first])

    middles = [middle, middle[0]] if middle else [""]
    lasts = [last, last[0]] if last else [""]

    for f in all_firsts:
        for m in middles:
            for l in lasts:
                for sep1 in separators:
                    for sep2 in separators:
                        username_parts = list(filter(None, [f, m, l]))
                        if len(username_parts) == 1:
                            username = username_parts[0]
                        elif len(username_parts) == 2:
                            username = f"{username_parts[0]}{sep1}{username_parts[1]}"
                        else:
                            username = f"{username_parts[0]}{sep1}{username_parts[1]}{sep2}{username_parts[2]}"
                        permutations.add(f"{username}@{domain}")
    return sorted(permutations)


# --- Email Validator ---
def is_valid_email_format(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email)

def validate_mx_record(domain):
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except Exception:
        return False

def validate_email(email):
    if not is_valid_email_format(email):
        return "❌ Invalid format"
    domain = email.split('@')[-1]
    if not validate_mx_record(domain):
        return "⚠️ No MX record"
    return "✅ Looks valid"


# --- Streamlit UI ---
st.set_page_config(page_title="Email Tool", layout="centered")

st.title("📧 Email Tools")
mode = st.radio("Choose what you want to do:", ["Email Permutator", "Email Validator"], horizontal=True)
st.markdown("---")

# --- Email Permutator UI ---
if mode == "Email Permutator":
    st.subheader("🔄 Generate Email Permutations")

    with st.form("perm_form"):
        first_name = st.text_input("First Name*", placeholder="e.g., John", max_chars=30)
        middle_name = st.text_input("Middle Name", placeholder="Optional", max_chars=30)
        last_name = st.text_input("Last Name", placeholder="e.g., Smith", max_chars=30)
        nickname = st.text_input("Nickname", placeholder="e.g., Mike (optional)", max_chars=30)
        domain = st.text_input("Company Domain*", placeholder="e.g., example.com", max_chars=60)

        submitted = st.form_submit_button("🔍 Generate")

    if submitted:
        if not first_name or not domain:
            st.warning("First Name and Domain are required.")
        else:
            emails = generate_permutations(first_name, middle_name, last_name, domain, nickname)
            st.success(f"Generated {len(emails)} permutations.")
            st.download_button("📥 Download as .txt", data="\n".join(emails), file_name="emails.txt")
            st.code("\n".join(emails[:50]), language="text")

# --- Email Validator UI ---
elif mode == "Email Validator":
    st.subheader("✅ Check Email Validity")

    with st.form("val_form"):
        emails_text = st.text_area("Enter email(s), one per line:", height=200)
        val_submitted = st.form_submit_button("🚦 Validate Emails")

    if val_submitted:
        if not emails_text.strip():
            st.warning("Please enter at least one email.")
        else:
            emails = emails_text.strip().splitlines()
            st.markdown("### Results")
            for email in emails:
                status = validate_email(email.strip())
                st.write(f"- `{email.strip()}` → {status}")
