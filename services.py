"""Application use cases for banking operations."""

from decimal import Decimal

from models import Account
from repository import AccountRepository


class BankingService:
    """Coordinate account use cases without depending on the console UI."""

    def __init__(self, account_repository: AccountRepository) -> None:
        self._accounts = account_repository

    def create_account(
        self,
        account_number: str,
        holder_name: str,
        initial_deposit: Decimal,
    ) -> Account:
        """Create and persist a new account."""
        account = Account(account_number, holder_name, initial_deposit)
        self._accounts.add(account)
        return account

    def deposit(self, account_number: str, amount: Decimal) -> None:
        """Deposit funds into an existing account."""
        self._accounts.require(account_number).deposit(amount)

    def withdraw(self, account_number: str, amount: Decimal) -> None:
        """Withdraw funds from an existing account."""
        self._accounts.require(account_number).withdraw(amount)

    def transfer(
        self,
        source_account_number: str,
        target_account_number: str,
        amount: Decimal,
    ) -> None:
        """Move funds between two different existing accounts."""
        if source_account_number == target_account_number:
            raise ValueError("Cannot transfer to the same account!")
        source_account = self._accounts.require(source_account_number)
        target_account = self._accounts.require(target_account_number)
        source_account.transfer_to(amount, target_account_number)
        target_account.receive_transfer(amount, source_account_number)

    def get_account(self, account_number: str) -> Account:
        """Return an account or raise a not-found error."""
        return self._accounts.require(account_number)

    def account_count(self) -> int:
        """Return the number of registered accounts."""
        return self._accounts.count()
