from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
import sqlite3
from src.utils.helpers import get_db_connection

# Define the Investment model
class Investment(BaseModel):
    id: int
    user_id: int
    investment_type: str
    amount: float
    purchase_date: str
    current_value: float

# Define the Investment Tracker router
investment_tracker_router = APIRouter()

# Define the database connection
def get_db():
    conn = get_db_connection()
    return conn

# Create a new investment
@investment_tracker_router.post("/investments/")
async def create_investment(investment: Investment, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO investments (user_id, investment_type, amount, purchase_date, current_value)
        VALUES (?, ?, ?, ?, ?)
    """, (investment.user_id, investment.investment_type, investment.amount, investment.purchase_date, investment.current_value))
    db.commit()
    return JSONResponse(content={"message": "Investment created successfully"}, status_code=201)

# Get all investments for a user
@investment_tracker_router.get("/investments/")
async def get_investments(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM investments
        WHERE user_id = ?
    """, (user_id,))
    investments = cursor.fetchall()
    return JSONResponse(content=[{"id": i[0], "user_id": i[1], "investment_type": i[2], "amount": i[3], "purchase_date": i[4], "current_value": i[5]} for i in investments], status_code=200)

# Update an investment
@investment_tracker_router.put("/investments/{investment_id}")
async def update_investment(investment_id: int, investment: Investment, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        UPDATE investments
        SET user_id = ?, investment_type = ?, amount = ?, purchase_date = ?, current_value = ?
        WHERE id = ?
    """, (investment.user_id, investment.investment_type, investment.amount, investment.purchase_date, investment.current_value, investment_id))
    db.commit()
    return JSONResponse(content={"message": "Investment updated successfully"}, status_code=200)

# Delete an investment
@investment_tracker_router.delete("/investments/{investment_id}")
async def delete_investment(investment_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        DELETE FROM investments
        WHERE id = ?
    """, (investment_id,))
    db.commit()
    return JSONResponse(content={"message": "Investment deleted successfully"}, status_code=200)

# Get the portfolio performance
@investment_tracker_router.get("/portfolio/")
async def get_portfolio(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT SUM(current_value) AS total_value
        FROM investments
        WHERE user_id = ?
    """, (user_id,))
    total_value = cursor.fetchone()[0]
    cursor.execute("""
        SELECT SUM(amount) AS total_investment
        FROM investments
        WHERE user_id = ?
    """, (user_id,))
    total_investment = cursor.fetchone()[0]
    return JSONResponse(content={"total_value": total_value, "total_investment": total_investment, "return_on_investment": (total_value - total_investment) / total_investment * 100 if total_investment != 0 else 0}, status_code=200)