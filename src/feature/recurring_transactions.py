# src/feature/recurring_transactions.py
from datetime import datetime, timedelta
from typing import List
from src.models import Transaction, User
from src.utils.helpers import get_current_user
from src.utils.cache import cache

class RecurringTransaction:
    def __init__(self, user: User, transaction: Transaction, frequency: str):
        self.user = user
        self.transaction = transaction
        self.frequency = frequency

    def schedule(self):
        # Schedule the recurring transaction
        if self.frequency == 'daily':
            self.schedule_daily()
        elif self.frequency == 'weekly':
            self.schedule_weekly()
        elif self.frequency == 'monthly':
            self.schedule_monthly()

    def schedule_daily(self):
        # Schedule the transaction to run daily
        current_date = datetime.now()
        next_date = current_date + timedelta(days=1)
        self.transaction.date = next_date
        self.user.transactions.append(self.transaction)

    def schedule_weekly(self):
        # Schedule the transaction to run weekly
        current_date = datetime.now()
        next_date = current_date + timedelta(weeks=1)
        self.transaction.date = next_date
        self.user.transactions.append(self.transaction)

    def schedule_monthly(self):
        # Schedule the transaction to run monthly
        current_date = datetime.now()
        next_date = current_date.replace(day=1) + timedelta(days=32)
        next_date = next_date.replace(day=1)
        self.transaction.date = next_date
        self.user.transactions.append(self.transaction)

def get_recurring_transactions(user: User) -> List[RecurringTransaction]:
    # Get all recurring transactions for the user
    recurring_transactions = []
    for transaction in user.transactions:
        if transaction.recurring:
            recurring_transaction = RecurringTransaction(user, transaction, transaction.frequency)
            recurring_transactions.append(recurring_transaction)
    return recurring_transactions

def create_recurring_transaction(user: User, transaction: Transaction, frequency: str):
    # Create a new recurring transaction
    recurring_transaction = RecurringTransaction(user, transaction, frequency)
    recurring_transaction.schedule()
    return recurring_transaction

@cache(ttl=60)  # Cache for 1 minute
def get_recurring_transactions_cache(user: User) -> List[RecurringTransaction]:
    # Get recurring transactions from cache
    return get_recurring_transactions(user)

def main():
    user = get_current_user()
    transaction = Transaction(amount=100, description='Test transaction')
    frequency = 'daily'
    recurring_transaction = create_recurring_transaction(user, transaction, frequency)
    print(recurring_transaction.transaction.date)

if __name__ == '__main__':
    main()