from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.models.user import User
from src.utils.auth import get_current_active_user
from src.utils.helpers import get_db
from src.utils.cache import cache

router = APIRouter()

@router.get("/profile")
async def get_user_profile(db: Session = Depends(get_db), user: User = Depends(get_current_active_user)):
    user_data = cache.get(f"user_{user.username}")
    if not user_data:
        user_data = db.query(User).filter(User.username == user.username).first()
        cache.set(f"user_{user.username}", user_data)
    return JSONResponse(content={"username": user_data.username, "email": user_data.email}, media_type="application/json")

@router.put("/profile")
async def update_user_profile(user_data: dict, db: Session = Depends(get_db), user: User = Depends(get_current_active_user)):
    db.query(User).filter(User.username == user.username).update(user_data)
    db.commit()
    cache.delete(f"user_{user.username}")
    return JSONResponse(content={"message": "User profile updated successfully"}, media_type="application/json")