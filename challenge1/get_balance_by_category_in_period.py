from datetime import datetime


def get_balance_by_category_in_period(category: str, start: datetime, end: datetime, *transactions: dict) -> int:
    """
    Calculates the balance in a specific category within the specified time period
    :param category: transaction category
    :param start: period start timestamp
    :param end: period end timestamp
    :param transactions: list of transactions
    :return: total balance
    """
    balance = 0
    for transaction in transactions:
        transaction_time = datetime.strptime(transaction["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if transaction["category"] == category and start <= transaction_time < end:
            balance += transaction["amount"]
    return balance
