import streamlit as st

# Optional nickname mapping
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


def generate_permutations(first, middle, last, domain, nickname=None):
    permutations = set()
    separators = ["", ".", "-", "_"]

    # Normalize input
    first = first.lower().strip()
    middle = middle.lower().strip() if middle else ""
    last = last.lower().strip() if last else ""
    domain = domain.lower().strip()

    # Nickname variations
    all_firsts = [first, first[0]]
    if nickname:
        all_firsts.append(nickname.lower().strip())
    if first in nickname_dict:
        all_firsts.extend(nickname_dict[first])

    # Middle and last variations
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


# --- Streamlit UI ---
st.set_page_config(page_title="Email Permutator", layout="centered")
st.title("📧 Email Permutator Tool")
st.caption("Generate email combinations using name + domain — built with ❤️ by Rahul")

with st.form("email_form"):
    first_name = st.text_input("First Name*", placeholder="e.g., John", max_chars=30)
    middle_name = st.text_input("Middle Name", placeholder="Optional", max_chars=30)
    last_name = st.text_input("Last Name", placeholder="e.g., Smith", max_chars=30)
    nickname = st.text_input("Nickname", placeholder="e.g., Mike (optional)", max_chars=30)
    domain = st.text_input("Company Domain*", placeholder="e.g., example.com", max_chars=60)

    submitted = st.form_submit_button("🔍 Generate Emails")

if submitted:
    if not first_name or not domain:
        st.warning("Please fill in at least First Name and Domain.")
    else:
        emails = generate_permutations(first_name, middle_name, last_name, domain, nickname)
        st.success(f"{len(emails)} email permutations generated.")
        st.download_button("📥 Download as .txt", data="\n".join(emails), file_name="emails.txt")
        st.code("\n".join(emails[:50]), language="text")
