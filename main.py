import database


def add_income():
    amount = float(input("Enter income amount: "))
    category = input("Enter category (e.g. Salary, Allowance, Freelance): ")
    date = input("Enter date (YYYY-MM-DD): ")
    note = input("Enter a note (optional): ")
    database.add_transaction("income", amount, category, date, note)
    print("Income added successfully.\n")


def add_expense():
    amount = float(input("Enter expense amount: "))
    category = input("Enter category (e.g. Food, Hostel, Shopping, Travel): ")
    date = input("Enter date (YYYY-MM-DD): ")
    note = input("Enter a note (optional): ")
    database.add_transaction("expense", amount, category, date, note)
    print("Expense added successfully.\n")


def view_all():
    rows = database.get_all_transactions()
    if not rows:
        print("No transactions found.\n")
        return
    print(f"\n{'ID':<5}{'Type':<10}{'Amount':<10}{'Category':<15}{'Date':<12}{'Note'}")
    print("-" * 65)
    for row in rows:
        t_id, t_type, amount, category, date, note = row
        print(f"{t_id:<5}{t_type:<10}{amount:<10.2f}{category or '-':<15}{date:<12}{note or '-'}")
    print()


def monthly_report():
    year_month = input("Enter month to report on (YYYY-MM): ")
    totals_by_type, totals_by_category = database.get_monthly_report(year_month)

    print(f"\n--- Report for {year_month} ---")
    income_total = 0
    expense_total = 0
    for t_type, total in totals_by_type:
        if t_type == "income":
            income_total = total
        elif t_type == "expense":
            expense_total = total

    print(f"Total Income:  {income_total:.2f}")
    print(f"Total Expense: {expense_total:.2f}")
    print(f"Net Savings:   {income_total - expense_total:.2f}")

    if totals_by_category:
        print("\nExpense breakdown by category:")
        for category, total in totals_by_category:
            print(f"  {category or 'Uncategorized':<15} {total:.2f}")
    print()


def search():
    keyword = input("Enter keyword to search (category, note, or date): ")
    rows = database.search_transactions(keyword)
    if not rows:
        print("No matching transactions found.\n")
        return
    print(f"\n{'ID':<5}{'Type':<10}{'Amount':<10}{'Category':<15}{'Date':<12}{'Note'}")
    print("-" * 65)
    for row in rows:
        t_id, t_type, amount, category, date, note = row
        print(f"{t_id:<5}{t_type:<10}{amount:<10.2f}{category or '-':<15}{date:<12}{note or '-'}")
    print()


def main():
    database.init_db()

    while True:
        print("==== Expense Tracker ====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. Monthly Report")
        print("5. Search Transactions")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_income()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_all()
        elif choice == "4":
            monthly_report()
        elif choice == "5":
            search()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.\n")


if __name__ == "__main__":
    main()