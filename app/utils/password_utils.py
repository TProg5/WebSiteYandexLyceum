from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)


def set_password(password: str) -> str:
    hashed_password = generate_password_hash(password)
    return hashed_password

def check_password(password: str, hashed_password: str) -> bool:
    return check_password_hash(hashed_password, password)