from datetime import datetime
import unittest

from get_balance_by_category_in_period import get_balance_by_category_in_period


class TestBalanceByCategoryInPeriod(unittest.TestCase):

    def setUp(self) -> None:
        self.category = "salary"
        self.transactions = [
            {
                "id": 1,
                "sourceAccount": "company_x",
                "targetAccount": "my_account",
                "amount": 10000,
                "category": "salary",
                "time": "2018-02-25T08:00:00.000Z",
            },
            {
                "id": 2,
                "sourceAccount": "my_account",
                "targetAccount": "company_y",
                "amount": -999,
                "category": "salary",
                "time": "2019-03-12T10:23:00.000Z",
            },
            {
                "id": 3,
                "sourceAccount": "company_z",
                "targetAccount": "my_account",
                "amount": 555,
                "category": "bonus",
                "time": "2018-12-12T07:00:00.000Z",
            },
        ]

    def test_transactions_within_period_category1(self):
        # test period boundary conditions
        self.start = datetime(2018, 2, 25, 8, 0, 0, 0)
        self.end = datetime(2019, 3, 12, 10, 23, 0, 1)
        self.assertEqual(
            get_balance_by_category_in_period(self.category, self.start, self.end, *self.transactions),
            9001
        )

    def test_transactions_within_period_category2(self):
        # test period boundary conditions
        self.category = "bonus"
        self.start = datetime(2018, 12, 12, 7, 0, 0, 0)
        self.end = datetime(2018, 12, 12, 7, 0, 0, 1)
        self.assertEqual(
            get_balance_by_category_in_period(self.category, self.start, self.end, *self.transactions),
            555
        )

    def test_period_before_first_transaction(self):
        self.start = datetime(2017, 1, 10, 20, 44, 1, 120)
        self.end = datetime(2018, 2, 25, 7, 59, 59, 999)
        self.assertEqual(get_balance_by_category_in_period(self.category, self.start, self.end, *self.transactions), 0)

    def test_period_after_last_transaction(self):
        self.start = datetime(2019, 3, 12, 10, 23, 0, 1)
        self.end = datetime(2020, 11, 10, 20, 44, 1, 120)
        self.assertEqual(get_balance_by_category_in_period(self.category, self.start, self.end, *self.transactions), 0)

    def test_period_between_transaction(self):
        self.start = datetime(2018, 2, 25, 8, 0, 0, 1)
        self.end = datetime(2019, 3, 12, 10, 23, 0, 0)
        self.assertEqual(get_balance_by_category_in_period(self.category, self.start, self.end, *self.transactions), 0)
