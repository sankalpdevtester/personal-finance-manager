from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import User
from src.utils.helpers import get_db
from src.utils.cache import cache

router = APIRouter()

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define the User model
class UserRequest(BaseModel):
    username: str
    password: str

# Define the token response model
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Create a new user
@router.post("/users/")
async def create_user(user: UserRequest, db = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create a new user
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

# Login endpoint
@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Get the user from the database
    db = next(get_db())
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Check the password
    if user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate a token
    access_token = "token_" + user.username
    return {"access_token": access_token, "token_type": "bearer"}

# Get the current user
@router.get("/users/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    # Get the user from the database
    user = db.query(User).filter(User.username == token.split("_")[1]).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"username": user.username}