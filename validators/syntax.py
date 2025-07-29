import re

def is_valid_syntax(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None
