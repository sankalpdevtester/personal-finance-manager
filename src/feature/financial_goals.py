# src/feature/financial_goals.py
from typing import List
from src.models import User, FinancialGoal
from src.utils.auth import get_current_user
from src.api import auth
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel

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

@router.post("/financial-goals/")
async def create_financial_goal(request: FinancialGoalRequest, current_user: User = Depends(get_current_user)):
    financial_goal = FinancialGoal(
        name=request.name,
        target_amount=request.target_amount,
        deadline=request.deadline,
        user_id=current_user.id
    )
    financial_goal.save()
    return JSONResponse(content={"message": "Financial goal created successfully"}, status_code=201)

@router.get("/financial-goals/")
async def get_financial_goals(current_user: User = Depends(get_current_user)):
    financial_goals = FinancialGoal.filter(user_id=current_user.id)
    response = []
    for goal in financial_goals:
        response.append({
            "id": goal.id,
            "name": goal.name,
            "target_amount": goal.target_amount,
            "deadline": goal.deadline,
            "progress": goal.progress
        })
    return JSONResponse(content=response, status_code=200)

@router.get("/financial-goals/{goal_id}")
async def get_financial_goal(goal_id: int, current_user: User = Depends(get_current_user)):
    financial_goal = FinancialGoal.get(id=goal_id)
    if financial_goal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to access this financial goal")
    return JSONResponse(content={
        "id": financial_goal.id,
        "name": financial_goal.name,
        "target_amount": financial_goal.target_amount,
        "deadline": financial_goal.deadline,
        "progress": financial_goal.progress
    }, status_code=200)

@router.put("/financial-goals/{goal_id}")
async def update_financial_goal(goal_id: int, request: FinancialGoalRequest, current_user: User = Depends(get_current_user)):
    financial_goal = FinancialGoal.get(id=goal_id)
    if financial_goal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this financial goal")
    financial_goal.name = request.name
    financial_goal.target_amount = request.target_amount
    financial_goal.deadline = request.deadline
    financial_goal.save()
    return JSONResponse(content={"message": "Financial goal updated successfully"}, status_code=200)

@router.delete("/financial-goals/{goal_id}")
async def delete_financial_goal(goal_id: int, current_user: User = Depends(get_current_user)):
    financial_goal = FinancialGoal.get(id=goal_id)
    if financial_goal.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this financial goal")
    financial_goal.delete_instance()
    return JSONResponse(content={"message": "Financial goal deleted successfully"}, status_code=200)
```
To integrate this new feature with the existing files, you would need to add the following code to the `src/main.py` file:
```python
from src.feature.financial_goals import router as financial_goals_router

app.include_router(financial_goals_router)
```
And add the following code to the `src/models.py` file:
```python
from peewee import Model, IntegerField, CharField, FloatField, DateTimeField, ForeignKey

class FinancialGoal(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    target_amount = FloatField()
    deadline = DateTimeField()
    user = ForeignKey(User, related_name="financial_goals")
    progress = FloatField(default=0.0)

    class Meta:
        database = db
```
You would also need to add the following code to the `src/feature/financial_insights.py` file to calculate the progress of the financial goals:
```python
from src.feature.financial_goals import FinancialGoal

def calculate_financial_goal_progress(financial_goal: FinancialGoal):
    # Calculate the progress of the financial goal based on the user's transactions
    progress = 0.0
    # ...
    return progress
```
And finally, you would need to add the following code to the `src/routes/users.py` file to display the financial goals in the user's dashboard:
```python
from src.feature.financial_goals import FinancialGoal

@app.get("/users/{user_id}/dashboard")
async def get_user_dashboard(user_id: int):
    user = User.get(id=user_id)
    financial_goals = FinancialGoal.filter(user_id=user_id)
    # ...
    return JSONResponse(content={"financial_goals": financial_goals}, status_code=200)