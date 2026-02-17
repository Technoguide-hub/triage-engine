from sqlalchemy.orm import Session
from app.auth.models import User
from app.core.security import verify_password, create_access_token


def authenticate(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None

    token = create_access_token({
        "sub": user.id,
        "role": user.role
    })
    return token