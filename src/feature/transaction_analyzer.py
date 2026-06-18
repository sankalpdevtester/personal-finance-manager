# src/feature/transaction_analyzer.py
from typing import List, Dict
from src.models import Transaction
from src.utils.helpers import get_user_transactions
from src.utils.auth import get_current_user

class TransactionAnalyzer:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.transactions = get_user_transactions(user_id)

    def categorize_transactions(self) -> Dict[str, List[Transaction]]:
        categorized_transactions = {}
        for transaction in self.transactions:
            category = transaction.category
            if category not in categorized_transactions:
                categorized_transactions[category] = []
            categorized_transactions[category].append(transaction)
        return categorized_transactions

    def get_total_spent(self) -> float:
        total_spent = 0
        for transaction in self.transactions:
            if transaction.type == "expense":
                total_spent += transaction.amount
        return total_spent

    def get_average_spent_per_category(self) -> Dict[str, float]:
        average_spent_per_category = {}
        categorized_transactions = self.categorize_transactions()
        for category, transactions in categorized_transactions.items():
            total_spent = sum(transaction.amount for transaction in transactions if transaction.type == "expense")
            average_spent = total_spent / len(transactions)
            average_spent_per_category[category] = average_spent
        return average_spent_per_category

    def get_top_expenses(self, limit: int = 5) -> List[Transaction]:
        top_expenses = sorted(self.transactions, key=lambda x: x.amount, reverse=True)
        return [transaction for transaction in top_expenses if transaction.type == "expense"][:limit]

def analyze_user_transactions(user_id: int) -> Dict:
    analyzer = TransactionAnalyzer(user_id)
    return {
        "categorized_transactions": analyzer.categorize_transactions(),
        "total_spent": analyzer.get_total_spent(),
        "average_spent_per_category": analyzer.get_average_spent_per_category(),
        "top_expenses": analyzer.get_top_expenses()
    }

# Example usage:
# user_id = get_current_user().id
# analysis = analyze_user_transactions(user_id)
# print(analysis)