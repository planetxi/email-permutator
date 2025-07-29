# Regenerating the full project code with:
# - Email Permutator
# - Optional nickname
# - Inline email verification
# - CSV upload and download support

import itertools
import pandas as pd
import re
import smtplib
import dns.resolver
from email_validator import validate_email, EmailNotValidError

# Define nickname mapping
NICKNAME_MAP = {
    "johnathan": "john",
    "jonathan": "jon",
    "michael": "mike",
    "johannes": "johan",
    "william": "bill",
    "richard": "rich",
    "robert": "rob",
    "steven": "steve",
    "thomas": "tom",
    "joseph": "joe",
    "nicholas": "nick",
    "patrick": "pat"
}

# Generate permutations
def generate_permutations(first_name, middle_name, last_name, domain, nickname=""):
    firsts = {first_name.lower()}
    if first_name.lower() in NICKNAME_MAP:
        firsts.add(NICKNAME_MAP[first_name.lower()])
    if nickname:
        firsts.add(nickname.lower())

    middles = [middle_name.lower(), middle_name[:1].lower()] if middle_name else [""]
    lasts = [last_name.lower(), last_name[:1].lower()] if last_name else [""]

    formats = set()
    for f, m, l in itertools.product(firsts, middles, lasts):
        parts = list(filter(None, [f, m, l]))
        if not parts:
            continue
        formats.update({
            ".".join(parts),
            "_".join(parts),
            "".join(parts),
            f"{f}{l}",
            f"{f}.{l}",
            f"{f}_{l}",
            f"{f}{m}{l}"
        })

    return sorted({f"{fmt}@{domain}" for fmt in formats})

# Validate email format + MX + SMTP
def verify_email(email):
    try:
        # Syntax + domain check
        validate_email(email, check_deliverability=True)
        
        domain = email.split('@')[1]
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)

        # SMTP check
        server = smtplib.SMTP(timeout=5)
        server.connect(mx_record)
        server.helo()
        server.mail('test@example.com')
        code, _ = server.rcpt(email)
        server.quit()

        return code == 250
    except Exception:
        return False

