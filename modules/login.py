import json
from modules.dashboard import dashboard

def login():

        print("\n===== Login =====")

        email = input("Enter Email: ")
        password = input("Enter Password: ")

        with open("data/users.json", "r") as file:
            users = json.load(file)

        found = False

        for existing_user in users:
            if existing_user["email"] == email:
                found = True

                if existing_user["password"] == password:
                    print("✅ Login Successful")
                    print(f"Welcome {existing_user['name']} 😊")

                    dashboard(existing_user)
                    
                    break

                else:
                    print("❌ Wrong Password")
                    break
                
        if not found:
            print("❌ Email Not Found")