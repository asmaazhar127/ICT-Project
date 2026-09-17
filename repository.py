"""Account persistence abstraction used by the banking service."""

from models import Account


class AccountRepository:
    """Store accounts in memory behind a small replaceable interface."""

    def __init__(self) -> None:
        self._accounts: dict[str, Account] = {}

    def add(self, account: Account) -> None:
        """Store an account unless its number is already registered."""
        if account.account_number in self._accounts:
            raise ValueError("Account already exists!")
        self._accounts[account.account_number] = account

    def get(self, account_number: str) -> Account | None:
        """Return an account or ``None`` when it does not exist."""
        return self._accounts.get(account_number)

    def require(self, account_number: str) -> Account:
        """Return an account or raise a clear not-found error."""
        account = self.get(account_number)
        if account is None:
            raise ValueError("Account not found!")
        return account

    def count(self) -> int:
        """Return the number of stored accounts."""
        return len(self._accounts)
