from modules.income import add_income
from modules.balance import view_balance
from modules.expense import add_expense
from modules.history import transaction_history
from modules.ai import ai_suggestion
from modules.report import monthly_report

def dashboard(user):

    print("\n" + "=" * 50)
    print("🤖 AI Personal Finance Manager")
    print("=" * 50)

    print(f"Welcome {user['name']} 😊")

    print("\n========== DASHBOARD ==========")

    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Balance")
    print("4. Transaction History")
    print("5. AI Suggestion")
    print("6. Monthly Report")
    print("7. Logout")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_income(user)

    elif choice == "2":
        add_expense(user)

    elif choice == "3":
        view_balance(user)

    elif choice == "4":
        transaction_history(user)

    elif choice == "5":
        ai_suggestion(user)

    elif choice == "6":
        monthly_report(user)

    elif choice == "7":
        print("👋 Logged Out Successfully!")

    else:
        print("❌ Invalid Choice!")