import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from app.core.config import get_settings


PBKDF2_ITERATIONS = 120_000


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        algorithm, iterations, salt, expected_hash = hashed_password.split("$", 3)
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    candidate_hash = _pbkdf2_hash(
        password=plain_password,
        salt=salt,
        iterations=int(iterations),
    )
    return hmac.compare_digest(candidate_hash, expected_hash)


def get_password_hash(password: str) -> str:
    salt = base64.urlsafe_b64encode(secrets.token_bytes(16)).decode("ascii")
    password_hash = _pbkdf2_hash(
        password=password,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt}${password_hash}"


def _pbkdf2_hash(password: str, salt: str, iterations: int) -> str:
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    )
    return base64.urlsafe_b64encode(digest).decode("ascii")


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload: dict[str, Any] = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
