```python
from datetime import datetime
from typing import Dict

def calculate_investment_returns(investment_data: Dict) -> float:
    """
    Calculate the returns on an investment based on the initial amount, 
    current value, and time period.

    Args:
    investment_data (Dict): A dictionary containing the initial amount, 
                             current value, and time period of the investment.

    Returns:
    float: The calculated return on investment.
    """
    initial_amount = investment_data['initial_amount']
    current_value = investment_data['current_value']
    start_date = datetime.strptime(investment_data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(investment_data['end_date'], '%Y-%m-%d')
    time_period = (end_date - start_date).days / 365  # calculate time period in years

    if time_period <= 0:
        raise ValueError("Time period must be greater than zero")

    return ((current_value - initial_amount) / initial_amount) / time_period * 100
```