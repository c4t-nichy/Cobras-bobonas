import base64
import secrets
from hashlib import pbkdf2_hmac

from cryptography.fernet import Fernet, InvalidToken


ITERATIONS = 480_000


def derive_fernet(password: str, salt: bytes) -> Fernet:
    key = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS, dklen=32)
    return Fernet(base64.urlsafe_b64encode(key))


def encrypt_text(text: str, password: str) -> str:
    if not password:
        raise ValueError("Informe uma senha.")
    salt = secrets.token_bytes(16)
    token = derive_fernet(password, salt).encrypt(text.encode("utf-8"))
    encoded_salt = base64.urlsafe_b64encode(salt).decode("ascii")
    return f"v1${encoded_salt}${token.decode('ascii')}"


def decrypt_text(encrypted_text: str, password: str) -> str:
    if not password:
        raise ValueError("Informe uma senha.")

    try:
        version, encoded_salt, token = encrypted_text.strip().split("$", 2)
        if version != "v1":
            raise ValueError
        salt = base64.urlsafe_b64decode(encoded_salt.encode("ascii"))
        if len(salt) != 16:
            raise ValueError
        return derive_fernet(password, salt).decrypt(token.encode("ascii")).decode("utf-8")
    except (ValueError, UnicodeError, InvalidToken) as error:
        raise ValueError("Senha incorreta ou texto criptografado inválido.") from error