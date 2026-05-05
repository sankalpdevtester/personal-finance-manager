```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import status
from pydantic import BaseModel
import uvicorn
import sqlite3
import os
from src.utils.helpers import create_database

# Create the database if it doesn't exist
create_database()

# Create the FastAPI application
app = FastAPI()

# Define the CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a route for the root URL
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Personal Finance Manager Platform"}

# Define a route for the dashboard
@app.get("/dashboard")
async def read_dashboard():
    return {"message": "This is the dashboard page"}

# Define a route for the settings
@app.get("/settings")
async def read_settings():
    return {"message": "This is the settings page"}

# Define a route for handling errors
@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred"})

# Define a route for handling not found errors
@app.exception_handler(404)
async def handle_not_found(request: Request, exc: Exception):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Page not found"})

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Create the database tables
def create_tables():
    conn = sqlite3.connect("personal_finance.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            budget_name TEXT NOT NULL,
            budget_amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expense_name TEXT NOT NULL,
            expense_amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()

create_tables()
```