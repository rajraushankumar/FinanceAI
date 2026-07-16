import json

# AI Suggestion Module
# Analyze user's income and expense

def ai_suggestion(user):

    print("\n===== AI Suggestion =====")

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
            total_income = total_income + income["amount"]

    print("Total Income :", total_income)

        # Calculate total expense
    total_expense = 0

    for expense in expenses:

        if expense["email"] == user["email"]:
            total_expense = total_expense + expense["amount"]

    print("Total Expense :", total_expense)

    # AI Decision

    if total_expense > total_income:

        print("\n⚠️ Warning!")
        print("Your expenses are higher than your income.")

    elif total_expense >= (total_income * 0.7):

        print("\n⚠️ Be Careful!")
        print("You are spending more than 70% of your income.")

    else:

        print("\n✅ Great!")
        print("Your spending is under control. Keep saving!")