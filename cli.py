"""Console interface for the banking application."""

from decimal import Decimal, InvalidOperation

from services import BankingService


class BankingCLI:
    """Handle console presentation, input, and user authentication."""

    def __init__(self, service: BankingService, admins: dict[str, str]) -> None:
        self._service = service
        self._admins = admins

    def run(self) -> None:
        while True:
            print("\nBanking Application")
            print("1. Login")
            print("2. Exit")
            choice = input("Enter choice: ")
            if choice == "1":
                self.login()
            elif choice == "2":
                return
            else:
                print("Invalid choice!")

    def login(self) -> None:
        while True:
            print("\nLogin")
            login_name = input("Enter username (type 'exit' to quit): ")
            if login_name.lower() == "exit":
                return
            password = input("Enter password (type 'exit' to quit): ")
            if password.lower() == "exit":
                return
            if self._is_admin(login_name, password):
                self.admin_menu()
            elif self._is_account_user(login_name, password):
                self.user_menu(login_name)
            else:
                print("Invalid credentials!")

    def admin_menu(self) -> None:
        while True:
            print("\nAdmin Menu")
            print("1. Create Account")
            print("2. Generate Statement")
            print("3. Total Number of Accounts")
            print("4. Logout")
            choice = input("Enter choice: ")
            try:
                if choice == "1":
                    self._create_account()
                elif choice == "2":
                    self._generate_statement()
                elif choice == "3":
                    print(f"Total number of accounts: {self._service.account_count()}")
                elif choice == "4":
                    return
                else:
                    print("Invalid choice!")
            except ValueError as error:
                print(error)

    def user_menu(self, account_number: str) -> None:
        actions = {
            "1": self._withdraw,
            "2": self._deposit,
            "3": self._check_balance,
            "4": self._transfer,
        }
        while True:
            print("\nUser Menu")
            print("1. Withdraw")
            print("2. Deposit")
            print("3. Check Balance")
            print("4. Transfer Cash")
            print("5. Logout")
            choice = input("Enter choice: ")
            if choice == "5":
                return
            try:
                action = actions.get(choice)
                if action is None:
                    print("Invalid choice!")
                else:
                    action(account_number)
            except ValueError as error:
                print(error)

    def _create_account(self) -> None:
        account_number = input("Enter new account number: ")
        holder_name = input("Enter account holder's name: ")
        initial_deposit = self._read_amount("Enter initial deposit: ")
        self._service.create_account(account_number, holder_name, initial_deposit)
        print("Account created successfully!")

    def _generate_statement(self) -> None:
        account_number = input("Enter account number: ")
        account = self._service.get_account(account_number)
        print(f"Statement for account number {account_number}")
        print(f"Account holder: {account.holder_name}")
        print(f"Current balance: {account.balance}")
        print("Transactions:")
        for transaction in account.transactions:
            print(transaction)

    def _withdraw(self, account_number: str) -> None:
        self._service.withdraw(account_number, self._read_amount("Enter amount to withdraw: "))
        print("Withdrawal successful!")

    def _deposit(self, account_number: str) -> None:
        self._service.deposit(account_number, self._read_amount("Enter amount to deposit: "))
        print("Deposit successful!")

    def _check_balance(self, account_number: str) -> None:
        print(f"Current balance: {self._service.get_account(account_number).balance}")

    def _transfer(self, account_number: str) -> None:
        target = input("Enter target account number: ")
        amount = self._read_amount("Enter amount to transfer: ")
        self._service.transfer(account_number, target, amount)
        print("Transfer successful!")

    def _is_admin(self, login_name: str, password: str) -> bool:
        return self._admins.get(login_name) == password

    def _is_account_user(self, login_name: str, password: str) -> bool:
        try:
            account = self._service.get_account(login_name)
        except ValueError:
            return False
        return account.holder_name == password

    @staticmethod
    def _read_amount(prompt: str) -> Decimal:
        try:
            return Decimal(input(prompt))
        except InvalidOperation as error:
            raise ValueError("Enter a valid amount!") from error
