import re

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    if not phone:
        return True # Optional
    # Allow numbers, spaces, plus, dashes, parens
    pattern = r'^[\d\s\+\-\(\)]+$'
    return re.match(pattern, phone) is not None

def is_strong_password(password):
    return len(password) >= 6
