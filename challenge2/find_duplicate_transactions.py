from datetime import timedelta
from typing import List

import pandas as pd


def find_duplicate_transactions(*transactions: dict) -> List[List[dict]]:
    """
    Finds all transactions that have the same sourceAccount, targetAccount, category, amount,
    and the time difference between each consecutive transaction is less than 1 minute.
    :param transactions: list of transactions
    :return: list of all the duplicate transaction groups, ordered by time ascending
    """
    duplicate_txns = []
    txn_table = pd.DataFrame(transaction for transaction in transactions)
    txn_groups = (v for k, v in txn_table.groupby(["sourceAccount", "targetAccount", "category", "amount"]))
    for txn_group in txn_groups:
        txn_group["dt_time"] = pd.to_datetime(txn_group["time"])
        txn_group.sort_values(by=["dt_time", "id"], inplace=True)
        # adding column with time difference between consecutive transactions
        txn_group["time_diff"] = txn_group["dt_time"].diff()
        # adding column to mark duplicated transactions
        txn_group["duplicate"] = txn_group["time_diff"] <= timedelta(minutes=1)
        txn_group.loc[(txn_group["duplicate"] == False) & (txn_group["duplicate"].shift(-1)==True), "duplicate"] = True
        txn_group = txn_group.loc[txn_group["duplicate"]==True].drop(["time_diff", "duplicate", "dt_time"], axis=1)
        txn_group_dict = txn_group.to_dict("records")
        if txn_group_dict:
            duplicate_txns.append(txn_group_dict)
    return sorted(duplicate_txns, key=lambda txn_group: txn_group[0]["time"])
