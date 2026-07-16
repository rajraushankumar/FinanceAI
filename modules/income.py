import json

def add_income(user):

    print("\n===== Add Income =====")

    amount = float(input("Enter Amount : "))
    category = input("Enter Category : ")
    date = input("Enter Date (DD-MM-YYYY) : ")

    income = {
        "email": user["email"],
        "amount": amount,
        "category": category,
        "date": date
    }

    print("\nIncome Data")
    print(income)

    with open("data/income.json", "r") as file:
       incomes = json.load(file)

    incomes.append(income)

    with open("data/income.json", "w") as file:
        json.dump(incomes, file, indent=4)

    print("\n✅ Income Saved Successfully!")