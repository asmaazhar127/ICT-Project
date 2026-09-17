# Global data structures to store account information
accounts = {}
admins = {'admin': 'test',
          'asma' : 'afsaf123'}

# Function to create an account
def create_account():
    account_number = input("Enter new account number: ")
    if account_number in accounts:
        print("Account already exists!")
        return
    name = input("Enter account holder's name: ")
    initial_deposit = float(input("Enter initial deposit: "))
    accounts[account_number] = {
        'name': name,
        'balance': initial_deposit,
        'transactions': []
    }
    print("Account created successfully!")

# Function to generate account statement
def generate_statement():
    account_number = input("Enter account number: ")
    if account_number not in accounts:
        print("Account not found!")
        return
    print(f"Statement for account number {account_number}")
    print(f"Account holder: {accounts[account_number]['name']}")
    print(f"Current balance: {accounts[account_number]['balance']}")
    print("Transactions:")
    for transaction in accounts[account_number]['transactions']:
        print(transaction)

# Function to display total number of accounts
def total_accounts():
    print(f"Total number of accounts: {len(accounts)}")

# User functions
def withdraw(account_number):
    amount = float(input("Enter amount to withdraw: "))
    if accounts[account_number]['balance'] < amount:   
        print("Insufficient balance!")
        return
    accounts[account_number]['balance'] -= amount
    accounts[account_number]['transactions'].append(f"Withdrew {amount}")  
    print("Withdrawal successful!")

# Function to deposit money
def deposit(account_number):
    amount = float(input("Enter amount to deposit: "))
    accounts[account_number]['balance'] += amount  # deposit amount added to original balance
    accounts[account_number]['transactions'].append(f"Deposited {amount}")  # deposit amount added to transaction list
    print("Deposit successful!")

# Function to check balance
def check_balance(account_number):
    print(f"Current balance: {accounts[account_number]['balance']}")

# Function to transfer amount
def transfer_cash(account_number):
    target_account = input("Enter target account number: ")
    if target_account not in accounts:
        print("Target account not found!")
        return
    amount = float(input("Enter amount to transfer: "))
    if accounts[account_number]['balance'] < amount:  # balance must be greater than transfer amount
        print("Insufficient balance!")
        return
    accounts[account_number]['balance'] -= amount  # money deducted from sender account
    accounts[target_account]['balance'] += amount  # money added to receiver account
    accounts[account_number]['transactions'].append(f"Transferred {amount} to {target_account}") 
    accounts[target_account]['transactions'].append(f"Received {amount} from {account_number}")
    print("Transfer successful!")

# Main application logic
def admin_menu():
    while True:
        print("\nAdmin Menu")
        print("1. Create Account")
        print("2. Generate Statement")
        print("3. Total Number of Accounts")
        print("4. Logout")
        choice = input("Enter choice: ")
        if choice == '1':
            create_account()
        elif choice == '2':
            generate_statement()
        elif choice == '3':
            total_accounts()
        elif choice == '4':
            break
        else:
            print("Invalid choice!")

def user_menu(account_number):
    while True:
        print("\nUser Menu")
        print("1. Withdraw")
        print("2. Deposit")
        print("3. Check Balance")
        print("4. Transfer Cash")
        print("5. Logout")
        choice = input("Enter choice: ")
        if choice == '1':
            withdraw(account_number)
        elif choice == '2':
            deposit(account_number)
        elif choice == '3':
            check_balance(account_number)
        elif choice == '4':
            transfer_cash(account_number)
        elif choice == '5':
            break
        else:
            print("Invalid choice!")

def login():
    while True:
        print("\nLogin")
        username = input("Enter username (type 'exit' to quit): ")
        
        if username.lower() == 'exit':
            break
        
        password = input("Enter password (type 'exit' to quit): ")
        
        if password.lower() == 'exit':
            break
        
        if username in admins and admins[username] == password:
            admin_menu()
        elif username in accounts and accounts[username]['name'] == password:
            user_menu(username)
        else:
            print("Invalid credentials!")

# Start the application
if __name__ == "__main__":
    while True:
        print("\nBanking Application")
        print("1. Login")
        print("2. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            login()
        elif choice == '2':
            break
        else:
            print("Invalid choice!")