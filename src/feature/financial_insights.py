# src/feature/financial_insights.py
from typing import Dict, List
from src.models.user import User
from src.feature.transaction_analyzer import TransactionAnalyzer
from src.feature.investment_portfolio import InvestmentPortfolio
from src.feature.budgeting_module import BudgetingModule
from src.feature.recurring_transactions import RecurringTransactions
from src.utils.helpers import calculate_total_expenses, calculate_total_income

class FinancialInsights:
    def __init__(self, user: User):
        self.user = user
        self.transaction_analyzer = TransactionAnalyzer(user)
        self.investment_portfolio = InvestmentPortfolio(user)
        self.budgeting_module = BudgetingModule(user)
        self.recurring_transactions = RecurringTransactions(user)

    def get_financial_summary(self) -> Dict:
        total_income = calculate_total_income(self.user.income)
        total_expenses = calculate_total_expenses(self.user.expenses)
        savings_rate = (total_income - total_expenses) / total_income if total_income > 0 else 0
        investment_return = self.investment_portfolio.get_total_return()
        recurring_transactions = self.recurring_transactions.get_recurring_transactions()

        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "savings_rate": savings_rate,
            "investment_return": investment_return,
            "recurring_transactions": recurring_transactions
        }

    def get_budgeting_recommendations(self) -> List:
        budgeting_recommendations = []
        budgeting_categories = self.budgeting_module.get_budgeting_categories()

        for category in budgeting_categories:
            if category["allocated_amount"] > category["actual_amount"]:
                budgeting_recommendations.append({
                    "category": category["name"],
                    "recommended_amount": category["allocated_amount"] - category["actual_amount"]
                })

        return budgeting_recommendations

    def get_investment_recommendations(self) -> List:
        investment_recommendations = []
        investment_portfolio = self.investment_portfolio.get_investment_portfolio()

        for investment in investment_portfolio:
            if investment["return_on_investment"] < 0.05:
                investment_recommendations.append({
                    "investment": investment["name"],
                    "recommended_action": "Consider diversifying or rebalancing your portfolio"
                })

        return investment_recommendations

    def get_transaction_insights(self) -> List:
        transaction_insights = []
        transactions = self.transaction_analyzer.get_transactions()

        for transaction in transactions:
            if transaction["amount"] > 1000:
                transaction_insights.append({
                    "transaction": transaction["name"],
                    "recommended_action": "Consider reviewing and categorizing large transactions"
                })

        return transaction_insights

def get_financial_insights(user: User) -> Dict:
    financial_insights = FinancialInsights(user)
    financial_summary = financial_insights.get_financial_summary()
    budgeting_recommendations = financial_insights.get_budgeting_recommendations()
    investment_recommendations = financial_insights.get_investment_recommendations()
    transaction_insights = financial_insights.get_transaction_insights()

    return {
        "financial_summary": financial_summary,
        "budgeting_recommendations": budgeting_recommendations,
        "investment_recommendations": investment_recommendations,
        "transaction_insights": transaction_insights
    }