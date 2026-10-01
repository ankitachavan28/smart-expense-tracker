from datetime import datetime


# ============================================================
# DECORATORS
# ============================================================

def log_transaction(func):
    """Decorator to log transaction operations."""

    def wrapper(*args, **kwargs):
        print("\n[LOG] Performing transaction...")
        result = func(*args, **kwargs)
        print(
            f"[LOG] {func.__name__} completed at "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return result

    return wrapper


def validate_amount(func):
    """Decorator to validate transaction amount."""

    def wrapper(self, amount, *args, **kwargs):

        if amount <= 0:
            print("Error: Amount must be greater than 0.")
            return

        return func(self, amount, *args, **kwargs)

    return wrapper


# ============================================================
# TRANSACTION CLASS
# ============================================================

class Transaction:

    def __init__(self, transaction_id, amount, category, description):
        self.transaction_id = transaction_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def display(self):
        print(
            f"ID: {self.transaction_id} | "
            f"Amount: ₹{self.amount:.2f} | "
            f"Category: {self.category} | "
            f"Description: {self.description} | "
            f"Date: {self.date}"
        )


# ============================================================
# INCOME CLASS
# ============================================================

class Income(Transaction):

    def __init__(
        self,
        transaction_id,
        amount,
        category,
        description
    ):
        super().__init__(
            transaction_id,
            amount,
            category,
            description
        )

    def display(self):
        print(
            f"[INCOME] "
            f"ID: {self.transaction_id} | "
            f"₹{self.amount:.2f} | "
            f"{self.category} | "
            f"{self.description} | "
            f"{self.date}"
        )


# ============================================================
# EXPENSE CLASS
# ============================================================

class Expense(Transaction):

    def __init__(
        self,
        transaction_id,
        amount,
        category,
        description
    ):
        super().__init__(
            transaction_id,
            amount,
            category,
            description
        )

    def display(self):
        print(
            f"[EXPENSE] "
            f"ID: {self.transaction_id} | "
            f"₹{self.amount:.2f} | "
            f"{self.category} | "
            f"{self.description} | "
            f"{self.date}"
        )


# ============================================================
# EXPENSE TRACKER CLASS
# ============================================================

class ExpenseTracker:

    def __init__(self):
        self.transactions = []
        self.next_id = 1

    # --------------------------------------------------------
    # ADD INCOME
    # --------------------------------------------------------

    @log_transaction
    @validate_amount
    def add_income(
        self,
        amount,
        category,
        description
    ):

        income = Income(
            self.next_id,
            amount,
            category,
            description
        )

        self.transactions.append(income)

        self.next_id += 1

        print("Income added successfully.")

    # --------------------------------------------------------
    # ADD EXPENSE
    # --------------------------------------------------------

    @log_transaction
    @validate_amount
    def add_expense(
        self,
        amount,
        category,
        description
    ):

        expense = Expense(
            self.next_id,
            amount,
            category,
            description
        )

        self.transactions.append(expense)

        self.next_id += 1

        print("Expense added successfully.")

    # --------------------------------------------------------
    # DISPLAY TRANSACTIONS
    # --------------------------------------------------------

    def display_transactions(self):

        if not self.transactions:
            print("\nNo transactions available.")
            return

        print("\n========== TRANSACTIONS ==========")

        for transaction in self.transactions:
            transaction.display()

    # --------------------------------------------------------
    # CALCULATE TOTAL INCOME
    # --------------------------------------------------------

    def get_total_income(self):

        total = 0

        for transaction in self.transactions:

            if isinstance(transaction, Income):
                total += transaction.amount

        return total

    # --------------------------------------------------------
    # CALCULATE TOTAL EXPENSE
    # --------------------------------------------------------

    def get_total_expense(self):

        total = 0

        for transaction in self.transactions:

            if isinstance(transaction, Expense):
                total += transaction.amount

        return total

    # --------------------------------------------------------
    # CALCULATE BALANCE
    # --------------------------------------------------------

    def get_balance(self):

        income = self.get_total_income()
        expense = self.get_total_expense()

        return income - expense

    # --------------------------------------------------------
    # DISPLAY SUMMARY
    # --------------------------------------------------------

    def display_summary(self):

        income = self.get_total_income()
        expense = self.get_total_expense()
        balance = self.get_balance()

        print("\n========== FINANCIAL SUMMARY ==========")

        print(f"Total Income  : ₹{income:.2f}")
        print(f"Total Expense : ₹{expense:.2f}")
        print(f"Balance       : ₹{balance:.2f}")

    # --------------------------------------------------------
    # SEARCH BY CATEGORY
    # --------------------------------------------------------

    def search_by_category(self, category):

        found = False

        print(
            f"\n========== {category.upper()} TRANSACTIONS =========="
        )

        for transaction in self.transactions:

            if transaction.category.lower() == category.lower():

                transaction.display()
                found = True

        if not found:
            print("No transactions found in this category.")

    # --------------------------------------------------------
    # CATEGORY-WISE EXPENSE SUMMARY
    # --------------------------------------------------------

    def category_summary(self):

        categories = {}

        for transaction in self.transactions:

            if isinstance(transaction, Expense):

                category = transaction.category

                if category not in categories:
                    categories[category] = 0

                categories[category] += transaction.amount

        if not categories:
            print("\nNo expenses available.")
            return

        print("\n========== EXPENSE BY CATEGORY ==========")

        for category, amount in categories.items():

            print(
                f"{category:<20} ₹{amount:.2f}"
            )


# ============================================================
# INPUT HELPER FUNCTIONS
# ============================================================

def get_amount():

    try:

        amount = float(
            input("Enter amount: ₹")
        )

        return amount

    except ValueError:

        print("Invalid amount.")
        return None


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    tracker = ExpenseTracker()

    while True:

        print("\n")
        print("=" * 55)
        print("             SMART EXPENSE TRACKER")
        print("=" * 55)

        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. View Financial Summary")
        print("5. Search by Category")
        print("6. Category-wise Expense Summary")
        print("7. Exit")

        print("=" * 55)

        choice = input("Enter your choice: ")

        # ----------------------------------------------------
        # ADD INCOME
        # ----------------------------------------------------

        if choice == "1":

            amount = get_amount()

            if amount is None:
                continue

            category = input(
                "Enter income category: "
            )

            description = input(
                "Enter description: "
            )

            tracker.add_income(
                amount,
                category,
                description
            )

        # ----------------------------------------------------
        # ADD EXPENSE
        # ----------------------------------------------------

        elif choice == "2":

            amount = get_amount()

            if amount is None:
                continue

            category = input(
                "Enter expense category: "
            )

            description = input(
                "Enter description: "
            )

            tracker.add_expense(
                amount,
                category,
                description
            )

        # ----------------------------------------------------
        # VIEW TRANSACTIONS
        # ----------------------------------------------------

        elif choice == "3":

            tracker.display_transactions()

        # ----------------------------------------------------
        # FINANCIAL SUMMARY
        # ----------------------------------------------------

        elif choice == "4":

            tracker.display_summary()

        # ----------------------------------------------------
        # SEARCH CATEGORY
        # ----------------------------------------------------

        elif choice == "5":

            category = input(
                "Enter category to search: "
            )

            tracker.search_by_category(category)

        # ----------------------------------------------------
        # CATEGORY SUMMARY
        # ----------------------------------------------------

        elif choice == "6":

            tracker.category_summary()

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        elif choice == "7":

            print(
                "\nThank you for using "
                "Smart Expense Tracker!"
            )

            break

        else:

            print(
                "Invalid choice. Please try again."
            )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
