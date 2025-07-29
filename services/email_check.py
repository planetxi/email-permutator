from validators.syntax import is_valid_syntax
from validators.domain import is_disposable, is_role_based, has_mx_record
from validators.smtp import verify_smtp

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
