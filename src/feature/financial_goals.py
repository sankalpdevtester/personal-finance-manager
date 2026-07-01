# src/feature/financial_goals.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel
from typing import List
from src.utils.auth import get_current_user
from src.utils.cache import cache
from src.models import FinancialGoal, User

router = APIRouter()

class FinancialGoalRequest(BaseModel):
    name: str
    target_amount: float
    deadline: str

class FinancialGoalResponse(BaseModel):
    id: int
    name: str
    target_amount: float
    deadline: str
    progress: float

@router.post("/financial-goals", response_model=FinancialGoalResponse)
async def create_financial_goal(request: FinancialGoalRequest, user: User = Depends(get_current_user)):
    financial_goal = FinancialGoal(name=request.name, target_amount=request.target_amount, deadline=request.deadline, user_id=user.id)
    financial_goal.save()
    return financial_goal

@router.get("/financial-goals", response_model=List[FinancialGoalResponse])
async def get_financial_goals(user: User = Depends(get_current_user)):
    financial_goals = FinancialGoal.select().where(FinancialGoal.user_id == user.id)
    return [FinancialGoalResponse(id=goal.id, name=goal.name, target_amount=goal.target_amount, deadline=goal.deadline, progress=goal.progress) for goal in financial_goals]

@router.get("/financial-goals/{goal_id}", response_model=FinancialGoalResponse)
async def get_financial_goal(goal_id: int, user: User = Depends(get_current_user)):
    financial_goal = FinancialGoal.get_or_none(FinancialGoal.id == goal_id, FinancialGoal.user_id == user.id)
    if financial_goal is None:
        raise HTTPException(status_code=404, detail="Financial goal not found")
    return FinancialGoalResponse(id=financial_goal.id, name=financial_goal.name, target_amount=financial_goal.target_amount, deadline=financial_goal.deadline, progress=financial_goal.progress)

@router.put("/financial-goals/{goal_id}", response_model=FinancialGoalResponse)
async def update_financial_goal(goal_id: int, request: FinancialGoalRequest, user: User = Depends(get_current_user)):
    financial_goal = FinancialGoal.get_or_none(FinancialGoal.id == goal_id, FinancialGoal.user_id == user.id)
    if financial_goal is None:
        raise HTTPException(status_code=404, detail="Financial goal not found")
    financial_goal.name = request.name
    financial_goal.target_amount = request.target_amount
    financial_goal.deadline = request.deadline
    financial_goal.save()
    return FinancialGoalResponse(id=financial_goal.id, name=financial_goal.name, target_amount=financial_goal.target_amount, deadline=financial_goal.deadline, progress=financial_goal.progress)

@router.delete("/financial-goals/{goal_id}")
async def delete_financial_goal(goal_id: int, user: User = Depends(get_current_user)):
    financial_goal = FinancialGoal.get_or_none(FinancialGoal.id == goal_id, FinancialGoal.user_id == user.id)
    if financial_goal is None:
        raise HTTPException(status_code=404, detail="Financial goal not found")
    financial_goal.delete_instance()
    return JSONResponse(content={"message": "Financial goal deleted successfully"}, status_code=200)

@router.get("/financial-goals/{goal_id}/progress")
async def get_financial_goal_progress(goal_id: int, user: User = Depends(get_current_user)):
    financial_goal = FinancialGoal.get_or_none(FinancialGoal.id == goal_id, FinancialGoal.user_id == user.id)
    if financial_goal is None:
        raise HTTPException(status_code=404, detail="Financial goal not found")
    progress = financial_goal.progress
    return JSONResponse(content={"progress": progress}, status_code=200)