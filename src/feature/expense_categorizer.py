# src/feature/expense_categorizer.py

from src.models import Transaction
from src.feature.transaction_analyzer import TransactionAnalyzer
from src.utils.cache import Cache
from typing import List, Dict

class ExpenseCategorizer:
    def __init__(self):
        self.cache = Cache()
        self.transaction_analyzer = TransactionAnalyzer()

    def categorize_expenses(self, transactions: List[Transaction]) -> Dict[str, List[Transaction]]:
        """
        Categorize expenses based on transaction descriptions and merchant names.

        Args:
        transactions (List[Transaction]): List of transactions to categorize.

        Returns:
        Dict[str, List[Transaction]]: Dictionary with categories as keys and lists of transactions as values.
        """
        categorized_expenses = {}
        for transaction in transactions:
            category = self.get_category(transaction)
            if category not in categorized_expenses:
                categorized_expenses[category] = []
            categorized_expenses[category].append(transaction)
        return categorized_expenses

    def get_category(self, transaction: Transaction) -> str:
        """
        Get the category of a transaction based on its description and merchant name.

        Args:
        transaction (Transaction): Transaction to categorize.

        Returns:
        str: Category of the transaction.
        """
        cache_key = f"category:{transaction.id}"
        category = self.cache.get(cache_key)
        if category is None:
            category = self.transaction_analyzer.get_category(transaction.description, transaction.merchant_name)
            self.cache.set(cache_key, category, 60 * 60 * 24)  # cache for 1 day
        return category

    def update_category(self, transaction: Transaction, category: str) -> None:
        """
        Update the category of a transaction.

        Args:
        transaction (Transaction): Transaction to update.
        category (str): New category of the transaction.
        """
        cache_key = f"category:{transaction.id}"
        self.cache.set(cache_key, category, 60 * 60 * 24)  # cache for 1 day
        self.transaction_analyzer.update_category(transaction, category)

    def get_categories(self) -> List[str]:
        """
        Get a list of available categories.

        Returns:
        List[str]: List of available categories.
        """
        return self.transaction_analyzer.get_categories()

# Example usage:
# expense_categorizer = ExpenseCategorizer()
# transactions = [...]  # list of transactions
# categorized_expenses = expense_categorizer.categorize_expenses(transactions)
# print(categorized_expenses)