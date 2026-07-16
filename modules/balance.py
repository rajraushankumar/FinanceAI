import json

def view_balance(user):

    print("\n===== View Balance =====")

    with open("data/income.json", "r") as file:
        incomes = json.load(file)

    total = 0

    for income in incomes:
        total = total + income["amount"]

    with open("data/expense.json", "r") as file:
        expenses = json.load(file)

    total_expense = 0

    for expense in expenses:
        total_expense = total_expense + expense["amount"]

    balance = total - total_expense

    print("\nTotal Income :", total)
    print("Total Expense :", total_expense)
    print("Current Balance :", balance)