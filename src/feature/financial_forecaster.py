# src/feature/financial_forecaster.py
from datetime import datetime, timedelta
from typing import List
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from src.utils.helpers import get_user_data
from src.feature.expense_categorizer import categorize_expenses
from src.feature.investment_tracker import get_investment_data

class FinancialForecaster:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.expense_data = get_user_data(user_id, 'expenses')
        self.income_data = get_user_data(user_id, 'income')
        self.investment_data = get_investment_data(user_id)

    def predict_expenses(self, days_ahead: int = 30):
        """
        Predict future expenses based on historical data.
        """
        # Preprocess expense data
        expense_df = pd.DataFrame(self.expense_data)
        expense_df['date'] = pd.to_datetime(expense_df['date'])
        expense_df.set_index('date', inplace=True)
        expense_df = expense_df.resample('D').mean()

        # Split data into training and testing sets
        train_expense, test_expense = train_test_split(expense_df, test_size=0.2, random_state=42)

        # Create and train a linear regression model
        model = LinearRegression()
        model.fit(train_expense.index.values.reshape(-1, 1), train_expense['amount'].values)

        # Make predictions for the next 'days_ahead' days
        future_dates = pd.date_range(start=datetime.now(), periods=days_ahead)
        future_expenses = model.predict(future_dates.values.reshape(-1, 1))

        return future_expenses

    def predict_income(self, days_ahead: int = 30):
        """
        Predict future income based on historical data.
        """
        # Preprocess income data
        income_df = pd.DataFrame(self.income_data)
        income_df['date'] = pd.to_datetime(income_df['date'])
        income_df.set_index('date', inplace=True)
        income_df = income_df.resample('D').mean()

        # Split data into training and testing sets
        train_income, test_income = train_test_split(income_df, test_size=0.2, random_state=42)

        # Create and train a linear regression model
        model = LinearRegression()
        model.fit(train_income.index.values.reshape(-1, 1), train_income['amount'].values)

        # Make predictions for the next 'days_ahead' days
        future_dates = pd.date_range(start=datetime.now(), periods=days_ahead)
        future_income = model.predict(future_dates.values.reshape(-1, 1))

        return future_income

    def predict_investments(self, days_ahead: int = 30):
        """
        Predict future investment returns based on historical data.
        """
        # Preprocess investment data
        investment_df = pd.DataFrame(self.investment_data)
        investment_df['date'] = pd.to_datetime(investment_df['date'])
        investment_df.set_index('date', inplace=True)
        investment_df = investment_df.resample('D').mean()

        # Split data into training and testing sets
        train_investment, test_investment = train_test_split(investment_df, test_size=0.2, random_state=42)

        # Create and train a linear regression model
        model = LinearRegression()
        model.fit(train_investment.index.values.reshape(-1, 1), train_investment['return'].values)

        # Make predictions for the next 'days_ahead' days
        future_dates = pd.date_range(start=datetime.now(), periods=days_ahead)
        future_investments = model.predict(future_dates.values.reshape(-1, 1))

        return future_investments

def get_financial_forecast(user_id: int, days_ahead: int = 30):
    forecaster = FinancialForecaster(user_id)
    future_expenses = forecaster.predict_expenses(days_ahead)
    future_income = forecaster.predict_income(days_ahead)
    future_investments = forecaster.predict_investments(days_ahead)

    return {
        'expenses': future_expenses.tolist(),
        'income': future_income.tolist(),
        'investments': future_investments.tolist()
    }