import hashlib
import re
import random


def email_validation(email):
    EMAIL_FORMAT = r'\b[A-Za-z0-9\.\+_-]+@[A-Za-z0-9]+\.[A-Z|a-z]{1,3}\b'
    if re.fullmatch(EMAIL_FORMAT, email):
        return True
    else:
        return False


def encode_link(salted_email: str):
    return (hashlib.sha256(salted_email.encode())).hexdigest()


def get_random_hash():
    return random.getrandbits(256)


