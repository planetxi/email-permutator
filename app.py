import re
import smtplib
import dns.resolver
import streamlit as st
import pandas as pd
from io import StringIO

DISPOSABLE_DOMAINS = {
    "mailinator.com", "10minutemail.com", "guerrillamail.com",
    "trashmail.com", "tempmail.com", "yopmail.com"
}
ROLE_BASED_PREFIXES = {
    "admin", "support", "info", "sales", "contact", "webmaster", "help"
}
FROM_EMAIL = "check@yourdomain.com"

# DNS MX caching
mx_cache = {}

def is_valid_syntax(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

def is_disposable(email):
    domain = email.split('@')[1].lower()
    return domain in DISPOSABLE_DOMAINS

def is_role_based(email):
    prefix = email.split('@')[0].lower()
    return prefix in ROLE_BASED_PREFIXES

def has_mx_record(domain):
    if domain in mx_cache:
        return mx_cache[domain]
    try:
        answers = dns.resolver.resolve(domain, 'MX', lifetime=3)
        mx_cache[domain] = len(answers) > 0
        return mx_cache[domain]
    except:
        mx_cache[domain] = False
        return False

def verify_smtp(email):
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX', lifetime=3)
        mx = str(mx_records[0].exchange)
        server = smtplib.SMTP(mx, timeout=5)
        server.helo("yourdomain.com")
        server.mail(FROM_EMAIL)
        code, _ = server.rcpt(email)
        server.quit()
        return code in [250, 251]
    except:
        return False

def validate_email(email):
    email = email.strip()
    result = {
        "Email": email,
        "Syntax Valid": False,
        "MX Record": False,
        "Disposable": False,
        "Role-based": False,
        "SMTP Valid": False,
        "Verdict": "❌ Invalid"
    }

    if not is_valid_syntax(email):
        return result
    result["Syntax Valid"] = True
    result["Disposable"] = is_disposable(email)
    result["Role-based"] = is_role_based(email)
    domain = email.split('@')[1]
    result["MX Record"] = has_mx_record(domain)
    if result["MX Record"]:
        result["SMTP Valid"] = verify_smtp(email)
    if all([result["Syntax Valid"], result["MX Record"], result["SMTP Valid"]]) and not result["Disposable"]:
        result["Verdict"] = "✅ Valid"
    return result

def generate_permutations(first, middle, last, domain):
    parts = {
        "f": first.lower(),
        "m": middle.lower() if middle else "",
        "l": last.lower(),
        "fi": first[0].lower(),
        "mi": middle[0].lower() if middle else "",
        "li": last[0].lower(),
    }

    patterns = [
        "{f}.{l}", "{f}{l}", "{fi}{l}", "{f}{li}", "{l}{f}", "{l}.{f}",
        "{fi}.{l}", "{f}_{l}", "{f}-{l}", "{l}_{f}", "{f}", "{l}",
        "{fi}{li}", "{f}.{m}.{l}", "{f}{m}{l}", "{fi}{mi}{li}"
    ]

    emails = set()
    for pattern in patterns:
        try:
            email = pattern.format(**parts) + "@" + domain
            if is_valid_syntax(email):
                emails.add(email)
        except:
            continue
    return sorted(emails)

# Streamlit UI
st.title("📧 Email Tools App")
mode = st.radio("Choose Tool", ["Email Validator", "Email Permutator"])

if mode == "Email Validator":
    st.markdown("Paste emails below or upload a CSV file with a column named `Email`.")
    input_method = st.radio("Select input method", ["Paste emails", "Upload CSV"])
    emails = []
    if input_method == "Paste emails":
        raw_input = st.text_area("Enter emails (comma or newline separated)")
        if raw_input:
            emails = [e.strip() for e in raw_input.replace(',', '\n').split('\n') if e.strip()]
    else:
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            if "Email" in df.columns:
                emails = df["Email"].dropna().astype(str).tolist()
            else:
                st.error("CSV must contain a column named 'Email'")

    if emails and st.button("🚀 Validate Emails"):
        results = [validate_email(email) for email in emails]
        df_results = pd.DataFrame(results)
        st.success("✅ Validation Complete")
        st.dataframe(df_results)

        csv = df_results.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Results CSV", data=csv, file_name="validated_emails.csv", mime="text/csv")

elif mode == "Email Permutator":
    st.markdown("Generate possible professional email permutations based on name and domain.")
    first = st.text_input("First Name")
    middle = st.text_input("Middle Name (Optional)")
    last = st.text_input("Last Name")
    domain = st.text_input("Company Domain (e.g. example.com)")

    if st.button("🔄 Generate Permutations"):
        if not all([first, last, domain]):
            st.error("First name, last name, and domain are required.")
        else:
            permutations = generate_permutations(first, middle, last, domain)
            df_perms = pd.DataFrame({"Possible Emails": permutations})
            st.success(f"✅ Generated {len(permutations)} combinations")
            st.dataframe(df_perms)

            csv = df_perms.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Permutations CSV", data=csv, file_name="email_permutations.csv", mime="text/csv")
