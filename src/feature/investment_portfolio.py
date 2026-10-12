# src/feature/investment_portfolio.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from src.models import Investment, User
from src.utils.auth import get_current_user
from src.utils.helpers import get_investment_data
from typing import List

router = APIRouter()

@router.get("/investment-portfolio", response_model=List[Investment])
async def get_investment_portfolio(current_user: User = Depends(get_current_user)):
    """
    Get the investment portfolio for the current user.
    
    Returns:
    - A list of Investment objects representing the user's investments.
    """
    investments = await get_investment_data(current_user.id)
    return investments

@router.post("/investment-portfolio", response_model=Investment)
async def add_investment(investment: Investment, current_user: User = Depends(get_current_user)):
    """
    Add a new investment to the user's portfolio.
    
    Args:
    - investment: The Investment object to add.
    
    Returns:
    - The added Investment object.
    """
    # Validate the investment data
    if not investment.name or not investment.type or not investment.amount:
        raise HTTPException(status_code=400, detail="Invalid investment data")
    
    # Add the investment to the database
    investment.user_id = current_user.id
    await investment.save()
    return investment

@router.put("/investment-portfolio/{investment_id}", response_model=Investment)
async def update_investment(investment_id: int, investment: Investment, current_user: User = Depends(get_current_user)):
    """
    Update an existing investment in the user's portfolio.
    
    Args:
    - investment_id: The ID of the investment to update.
    - investment: The updated Investment object.
    
    Returns:
    - The updated Investment object.
    """
    # Get the existing investment
    existing_investment = await Investment.get(investment_id)
    if not existing_investment:
        raise HTTPException(status_code=404, detail="Investment not found")
    
    # Validate the investment data
    if not investment.name or not investment.type or not investment.amount:
        raise HTTPException(status_code=400, detail="Invalid investment data")
    
    # Update the investment
    existing_investment.name = investment.name
    existing_investment.type = investment.type
    existing_investment.amount = investment.amount
    await existing_investment.save()
    return existing_investment

@router.delete("/investment-portfolio/{investment_id}")
async def delete_investment(investment_id: int, current_user: User = Depends(get_current_user)):
    """
    Delete an investment from the user's portfolio.
    
    Args:
    - investment_id: The ID of the investment to delete.
    
    Returns:
    - A JSON response indicating the investment was deleted.
    """
    # Get the existing investment
    existing_investment = await Investment.get(investment_id)
    if not existing_investment:
        raise HTTPException(status_code=404, detail="Investment not found")
    
    # Delete the investment
    await existing_investment.delete()
    return JSONResponse(content={"message": "Investment deleted"}, status_code=200)
