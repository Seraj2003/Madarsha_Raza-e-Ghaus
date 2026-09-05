
import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings

def hash_password(password: str)-> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password=password_bytes,salt=salt)
    return hashed.decode("utf-8")

def verify_password (plain_pass: str,hashed_pass: str) -> bool:
    print(plain_pass+hashed_pass)
    return bcrypt.checkpw(
        plain_pass.encode("utf-8"),
        hashed_pass.encode("utf-8")
    )

def create_access_token(donor_id: int)-> str:
    now = datetime.now(timezone.utc)
    payload ={
        "sub": str(donor_id),
        "type":"access",
        "iat": now,
        "exp":now + timedelta(
            minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        ),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )