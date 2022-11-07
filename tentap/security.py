import hashlib

from rest_framework_simplejwt.tokens import RefreshToken


def encode_password(password: str):
    return (hashlib.sha256(password.encode())).hexdigest()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
