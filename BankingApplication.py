"""Application composition root and executable entry point."""

from cli import BankingCLI
from repository import AccountRepository
from services import BankingService


def build_application() -> BankingCLI:
    """Build the application with its replaceable dependencies."""
    repository = AccountRepository()
    service = BankingService(repository)
    admins = {"admin": "test", "asma": "afsaf123"}
    return BankingCLI(service, admins)


if __name__ == "__main__":
    build_application().run()