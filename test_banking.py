"""Tests for the banking service and account business rules."""

import unittest
from decimal import Decimal

from repository import AccountRepository
from services import BankingService


class BankingServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = BankingService(AccountRepository())
        self.service.create_account("100", "Alice", Decimal("100"))
        self.service.create_account("200", "Bob", Decimal("25"))

    def test_deposit_withdraw_and_transfer(self) -> None:
        self.service.deposit("100", Decimal("10"))
        self.service.withdraw("100", Decimal("20"))
        self.service.transfer("100", "200", Decimal("30"))

        sender = self.service.get_account("100")
        receiver = self.service.get_account("200")
        self.assertEqual(sender.balance, Decimal("60"))
        self.assertEqual(receiver.balance, Decimal("55"))
        self.assertEqual(
            sender.transactions,
            ["Deposited 10", "Withdrew 20", "Transferred 30 to 200"],
        )
        self.assertEqual(receiver.transactions, ["Received 30 from 100"])

    def test_rejects_duplicate_account_numbers(self) -> None:
        with self.assertRaisesRegex(ValueError, "Account already exists"):
            self.service.create_account("100", "Another person", Decimal("10"))

    def test_rejects_invalid_transaction_amount(self) -> None:
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            self.service.deposit("100", Decimal("0"))

    def test_rejects_withdrawal_over_balance(self) -> None:
        with self.assertRaisesRegex(ValueError, "Insufficient balance"):
            self.service.withdraw("100", Decimal("101"))

    def test_reports_missing_account(self) -> None:
        with self.assertRaisesRegex(ValueError, "Account not found"):
            self.service.get_account("999")


if __name__ == "__main__":
    unittest.main()
