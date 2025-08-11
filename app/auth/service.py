from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User

from app.auth.security import verify_password

def get_user(db: Session, user_email: str):
    return db.execute(select(User).where(User.email == user_email)).scalars().one_or_none()

def auth_user(db: Session, user_email: str, user_password: str):
    user = get_user(db, user_email)

    if not user:
        return False
    if not verify_password(user_password, user.password):
        return False
    
    return user