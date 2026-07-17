# src/feature/financial_goals.py

from src.models.user import User
from src.utils.helpers import calculate_savings_progress
from src.main import db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List

# Define the Financial Goal model
class FinancialGoal(BaseModel):
    id: int
    user_id: int
    goal_name: str
    target_amount: float
    current_amount: float
    deadline: str

# Define the Financial Goal router
router = APIRouter()

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Get all financial goals for a user
@router.get("/financial-goals/")
async def get_financial_goals(user: User = Depends()):
    financial_goals = db.query(FinancialGoal).filter(FinancialGoal.user_id == user.id).all()
    return financial_goals

# Create a new financial goal
@router.post("/financial-goals/")
async def create_financial_goal(goal: FinancialGoal, user: User = Depends()):
    new_goal = FinancialGoal(
        user_id=user.id,
        goal_name=goal.goal_name,
        target_amount=goal.target_amount,
        current_amount=0.0,
        deadline=goal.deadline
    )
    db.add(new_goal)
    db.commit()
    return new_goal

# Update a financial goal
@router.put("/financial-goals/{goal_id}")
async def update_financial_goal(goal_id: int, goal: FinancialGoal, user: User = Depends()):
    financial_goal = db.query(FinancialGoal).filter(FinancialGoal.id == goal_id).first()
    if financial_goal is None:
        raise HTTPException(status_code=404, detail="Financial goal not found")
    if financial_goal.user_id != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this financial goal")
    financial_goal.goal_name = goal.goal_name
    financial_goal.target_amount = goal.target_amount
    financial_goal.deadline = goal.deadline
    db.commit()
    return financial_goal

# Delete a financial goal
@router.delete("/financial-goals/{goal_id}")
async def delete_financial_goal(goal_id: int, user: User = Depends()):
    financial_goal = db.query(FinancialGoal).filter(FinancialGoal.id == goal_id).first()
    if financial_goal is None:
        raise HTTPException(status_code=404, detail="Financial goal not found")
    if financial_goal.user_id != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this financial goal")
    db.delete(financial_goal)
    db.commit()
    return {"message": "Financial goal deleted successfully"}

# Get the progress of a financial goal
@router.get("/financial-goals/{goal_id}/progress")
async def get_financial_goal_progress(goal_id: int, user: User = Depends()):
    financial_goal = db.query(FinancialGoal).filter(FinancialGoal.id == goal_id).first()
    if financial_goal is None:
        raise HTTPException(status_code=404, detail="Financial goal not found")
    if financial_goal.user_id != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to view this financial goal")
    progress = calculate_savings_progress(financial_goal.current_amount, financial_goal.target_amount)
    return {"progress": progress}