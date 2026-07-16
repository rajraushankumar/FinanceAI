from modules.register import register
from modules.login import login

# ==========================================
# AI Personal Finance Manager
# Version: 1.0
# Developer: Rajraushan
# ==========================================

def show_banner():
    print("=" * 50)
    print("🤖 AI Personal Finance Manager")
    print("=" * 50)
    print("Welcome, Rajraushan!")
    print()


def main():
    show_banner()

    print("1. Login")
    print("2. Register")
    print("3. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        login()

    elif choice == "2":
        register()

    elif choice == "3":
        print("Thank you for using AI Personal Finance Manager!")

    else:
        print("Invalid Choice!")


if __name__ == "__main__":
    main()