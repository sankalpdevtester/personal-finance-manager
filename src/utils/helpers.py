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
    initial_amount = investment_data.get('initial_amount', 0)
    current_value = investment_data.get('current_value', 0)
    start_date = datetime.strptime(investment_data.get('start_date', ''), '%Y-%m-%d')
    end_date = datetime.strptime(investment_data.get('end_date', ''), '%Y-%m-%d')

    time_period = (end_date - start_date).days / 365

    if time_period <= 0:
        return 0

    return ((current_value - initial_amount) / initial_amount) / time_period * 100