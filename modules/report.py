import json

# Monthly Report Module
# Display monthly finance summary

def monthly_report(user):

    # Read income data
    with open("data/income.json", "r") as file:
        incomes = json.load(file)

    # Read expense data
    with open("data/expense.json", "r") as file:
        expenses = json.load(file)

    # Calculate total income
    total_income = 0

    for income in incomes:
        if income["email"] == user["email"]:
            total_income += income["amount"]

    # Calculate total expense
    total_expense = 0

    for expense in expenses:
        if expense["email"] == user["email"]:
            total_expense += expense["amount"]

    # Calculate monthly summary
    balance = total_income - total_expense
    total_transactions = len(incomes) + len(expenses)
    savings = (balance / total_income) * 100

    # Display report
    print("\n===== MONTHLY REPORT =====")
    print("Total Income  :", total_income)
    print("Total Expense :", total_expense)
    print("Balance       :", balance)
    print("Transactions  :", total_transactions)
    print("Savings       :", round(savings, 2), "%")

    # AI status

    if savings >= 50:
        print("Status       : Excellent 😊")

    elif savings >= 20:
        print("Status       : Good 👍")

    else:
       print("Status       : Needs Improvement ⚠️")