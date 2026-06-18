from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.models import User
from src.utils.helpers import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str, db = next(get_db())):
    user = db.query(User).filter(User.username == token.split("_")[1]).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

def authenticate_user(username: str, password: str, db = next(get_db())):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if user.password != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user

def requires_auth(func):
    async def wrapper(*args, **kwargs):
        token = kwargs.get("token")
        if not token:
            raise HTTPException(status_code=401, detail="Token is required")
        user = get_current_user(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return await func(*args, **kwargs)
    return wrapper