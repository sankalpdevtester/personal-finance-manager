from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from src.models.user import User
from src.utils.helpers import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        return False
    return user

def get_current_user(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        return None
    user = db.query(User).filter(User.username == token).first()
    if not user:
        return None
    return user

def get_current_active_user(request: Request, db: Session):
    user = get_current_user(request, db)
    if not user:
        return None
    return user