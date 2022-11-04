import hashlib


def encode_password(password: str):
    return (hashlib.sha256(password.encode())).hexdigest()


