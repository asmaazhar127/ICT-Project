"""Core account model and account-level banking operations."""

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Account:
    """Represent one bank account and protect its balance operations."""

    account_number: str
    holder_name: str
    balance: Decimal = Decimal("0")
    transactions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Reject account state that could never be valid."""
        if self.balance < 0:
            raise ValueError("Initial deposit cannot be negative!")

    def deposit(self, amount: Decimal) -> None:
        """Add a positive amount and record the transaction."""
        self._validate_amount(amount)
        self.balance += amount
        self.transactions.append(f"Deposited {amount}")

    def withdraw(self, amount: Decimal) -> None:
        """Remove a positive amount when the account has enough funds."""
        self._validate_amount(amount)
        if amount > self.balance:
            raise ValueError("Insufficient balance!")
        self.balance -= amount
        self.transactions.append(f"Withdrew {amount}")

    def transfer_to(self, amount: Decimal, target_account_number: str) -> None:
        """Remove transfer funds and record the destination account."""
        self._validate_amount(amount)
        if amount > self.balance:
            raise ValueError("Insufficient balance!")
        self.balance -= amount
        self.record_transfer_to(amount, target_account_number)

    def receive_transfer(self, amount: Decimal, source_account_number: str) -> None:
        """Add transfer funds and record the source account."""
        self._validate_amount(amount)
        self.balance += amount
        self.record_transfer_from(amount, source_account_number)

    def record_transfer_to(self, amount: Decimal, target_account_number: str) -> None:
        """Record money sent to another account."""
        self.transactions.append(f"Transferred {amount} to {target_account_number}")

    def record_transfer_from(self, amount: Decimal, source_account_number: str) -> None:
        """Record money received from another account."""
        self.transactions.append(f"Received {amount} from {source_account_number}")

    @staticmethod
    def _validate_amount(amount: Decimal) -> None:
        """Ensure a transaction amount is positive."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero!")
