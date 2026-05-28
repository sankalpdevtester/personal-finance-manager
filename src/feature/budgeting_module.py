# src/feature/budgeting_module.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from src.utils.helpers import get_db
from src.models import Budget, Category

# Define the budgeting module router
budgeting_router = APIRouter()

# Define the budget model
class BudgetModel(BaseModel):
    id: int
    name: str
    amount: float
    categories: List[str]

# Define the category model
class CategoryModel(BaseModel):
    id: int
    name: str
    budget_id: int

# Define the budgeting endpoint
@budgeting_router.post("/budgets/")
async def create_budget(budget: BudgetModel, db = Depends(get_db)):
    # Create a new budget
    new_budget = Budget(name=budget.name, amount=budget.amount)
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    # Create categories for the budget
    for category in budget.categories:
        new_category = Category(name=category, budget_id=new_budget.id)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)

    return JSONResponse(content={"message": "Budget created successfully"}, status_code=201)

# Define the endpoint to get all budgets
@budgeting_router.get("/budgets/")
async def get_budgets(db = Depends(get_db)):
    budgets = db.query(Budget).all()
    return JSONResponse(content=[{"id": budget.id, "name": budget.name, "amount": budget.amount} for budget in budgets], status_code=200)

# Define the endpoint to get a specific budget
@budgeting_router.get("/budgets/{budget_id}")
async def get_budget(budget_id: int, db = Depends(get_db)):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return JSONResponse(content={"id": budget.id, "name": budget.name, "amount": budget.amount}, status_code=200)

# Define the endpoint to update a budget
@budgeting_router.put("/budgets/{budget_id}")
async def update_budget(budget_id: int, budget: BudgetModel, db = Depends(get_db)):
    existing_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if existing_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    existing_budget.name = budget.name
    existing_budget.amount = budget.amount
    db.commit()
    db.refresh(existing_budget)
    return JSONResponse(content={"message": "Budget updated successfully"}, status_code=200)

# Define the endpoint to delete a budget
@budgeting_router.delete("/budgets/{budget_id}")
async def delete_budget(budget_id: int, db = Depends(get_db)):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    db.delete(budget)
    db.commit()
    return JSONResponse(content={"message": "Budget deleted successfully"}, status_code=200)

# Define the endpoint to get all categories for a budget
@budgeting_router.get("/budgets/{budget_id}/categories")
async def get_categories(budget_id: int, db = Depends(get_db)):
    categories = db.query(Category).filter(Category.budget_id == budget_id).all()
    return JSONResponse(content=[{"id": category.id, "name": category.name} for category in categories], status_code=200)

# Define the endpoint to create a new category for a budget
@budgeting_router.post("/budgets/{budget_id}/categories")
async def create_category(budget_id: int, category: CategoryModel, db = Depends(get_db)):
    # Check if the budget exists
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")

    # Create a new category
    new_category = Category(name=category.name, budget_id=budget_id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return JSONResponse(content={"message": "Category created successfully"}, status_code=201)

# Define the endpoint to get a specific category for a budget
@budgeting_router.get("/budgets/{budget_id}/categories/{category_id}")
async def get_category(budget_id: int, category_id: int, db = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).filter(Category.budget_id == budget_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return JSONResponse(content={"id": category.id, "name": category.name}, status_code=200)

# Define the endpoint to update a category for a budget
@budgeting_router.put("/budgets/{budget_id}/categories/{category_id}")
async def update_category(budget_id: int, category_id: int, category: CategoryModel, db = Depends(get_db)):
    existing_category = db.query(Category).filter(Category.id == category_id).filter(Category.budget_id == budget_id).first()
    if existing_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    existing_category.name = category.name
    db.commit()
    db.refresh(existing_category)
    return JSONResponse(content={"message": "Category updated successfully"}, status_code=200)

# Define the endpoint to delete a category for a budget
@budgeting_router.delete("/budgets/{budget_id}/categories/{category_id}")
async def delete_category(budget_id: int, category_id: int, db = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).filter(Category.budget_id == budget_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return JSONResponse(content={"message": "Category deleted successfully"}, status_code=200)