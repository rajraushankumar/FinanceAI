import json

def add_expense(user):

    print("\n===== Add Expense =====")

    amount = float(input("Enter Amount : "))
    category = input("Enter Category : ")
    date = input("Enter Date (DD-MM-YYYY) : ")

    expense = {
        "email": user["email"],
        "amount": amount,
        "category": category,
        "date": date
    }

    print("\nExpense Data")
    print(expense)

    with open("data/expense.json", "r") as file:
        expenses = json.load(file)

    expenses.append(expense)

    with open("data/expense.json", "w") as file:
        json.dump(expenses, file, indent=4)

    print("\n✅ Expense Saved Successfully!")