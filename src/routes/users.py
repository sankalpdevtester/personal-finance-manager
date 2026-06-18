from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from src.models.user import User
from src.utils.helpers import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

@router.post("/register")
async def create_user(user: User, db: Session = Depends(get_db)):
    try:
        hashed_password = pwd_context.hash(user.password)
        db_user = User(username=user.username, email=user.email, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User created successfully"}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/me")
async def get_current_user(db: Session = Depends(get_db), username: str = Depends()):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username, "email": user.email}