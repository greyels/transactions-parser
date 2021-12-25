import unittest

from find_duplicate_transactions import find_duplicate_transactions


class TestFindDuplicateTransactions(unittest.TestCase):

    def setUp(self) -> None:
        self.transaction1 = {
            "id": 1,
            "sourceAccount": "company_x",
            "targetAccount": "my_account",
            "amount": 10000,
            "category": "salary",
            "time": "2018-02-25T08:00:00.000Z",
        }
        self.transaction2 = {
            "id": 2,
            "sourceAccount": "company_x",
            "targetAccount": "my_account",
            "amount": 10000,
            "category": "salary",
            "time": "2018-02-25T08:01:01.000Z",
        }
        self.transaction3 = {
            "id": 3,
            "sourceAccount": "company_x",
            "targetAccount": "my_account",
            "amount": 10000,
            "category": "salary",
            "time": "2018-02-25T08:02:02.000Z",
        }
        self.transaction4 = {
            "id": 4,
            "sourceAccount": "company_y",
            "targetAccount": "my_account",
            "amount": 555,
            "category": "bonus",
            "time": "2018-02-25T12:05:01.000Z",
        }
        self.transaction5 = {
            "id": 5,
            "sourceAccount": "company_y",
            "targetAccount": "my_account",
            "amount": 555,
            "category": "bonus",
            "time": "2018-02-25T12:06:01.000Z",
        }

    def test_no_duplicate_transactions_one_group(self):
        transactions = [self.transaction2, self.transaction3, self.transaction1]
        self.assertEqual(find_duplicate_transactions(*transactions), [])

    def test_no_duplicate_transactions_several_groups(self):
        self.transaction5["time"] = "2018-02-25T12:06:01.001Z"
        transactions = [self.transaction5, self.transaction1, self.transaction4, self.transaction2, self.transaction3]
        self.assertEqual(find_duplicate_transactions(*transactions), [])

    def test_duplicate_transactions_one_group(self):
        transactions = [self.transaction5, self.transaction4]
        expected_result = [[self.transaction4, self.transaction5]]
        self.assertEqual(find_duplicate_transactions(*transactions), expected_result)

    def test_duplicate_transactions_several_groups(self):
        self.transaction1["time"] = "2018-02-25T08:00:00.000Z"
        self.transaction2["time"] = "2018-02-25T08:01:00.000Z"
        transactions = [self.transaction5, self.transaction4, self.transaction3, self.transaction1, self.transaction2]
        expected_result = [[self.transaction1, self.transaction2], [self.transaction4, self.transaction5]]
        self.assertEqual(find_duplicate_transactions(*transactions), expected_result)

    def test_duplicate_transactions_same_time(self):
        self.transaction2["time"] = "2018-02-25T08:00:00.000Z"
        transactions = [self.transaction2, self.transaction1]
        expected_result = [[self.transaction1, self.transaction2]]
        self.assertEqual(find_duplicate_transactions(*transactions), expected_result)

    def test_duplicate_transactions_one_min_difference(self):
        self.transaction1["time"] = "2018-02-25T08:00:01.000Z"
        self.transaction3["time"] = "2018-02-25T08:02:01.000Z"
        transactions = [self.transaction2, self.transaction3, self.transaction1]
        expected_result = [[self.transaction1, self.transaction2, self.transaction3]]
        self.assertEqual(find_duplicate_transactions(*transactions), expected_result)
