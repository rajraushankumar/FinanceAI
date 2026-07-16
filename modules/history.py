import json

def transaction_history(user):

    print("\n===== Transaction History =====")

    # Income
    with open("data/income.json", "r") as file:
        incomes = json.load(file)

    print("\n========== INCOME ==========")

    count = 1

    for income in incomes:

        if income["email"] == user["email"]:

            print(f"\nIncome #{count}")
            print("Amount   :", income["amount"])
            print("Category :", income["category"])
            print("Date     :", income["date"])

            count = count + 1

    # Expense
    with open("data/expense.json", "r") as file:
        expenses = json.load(file)

    print("\n========== EXPENSE ==========")

    count = 1

    for expense in expenses:

        if expense["email"] == user["email"]:

            print(f"\nExpense #{count}")
            print("Amount   :", expense["amount"])
            print("Category :", expense["category"])
            print("Date     :", expense["date"])

            count = count + 1