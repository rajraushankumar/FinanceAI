import json

def register():

    print("\n===== Register =====")

    name = input("Enter Name: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")

    user = {
        "name": name,
        "email": email,
        "password": password,
    }


    with open("data/users.json", "r") as file:
        users = json.load(file)

    for existing_user in users:
     if existing_user["email"] == email:
        print("\n❌ Email already exists!")
        return

    users.append(user)

    with open("data/users.json", "w") as file:
        json.dump(users, file, indent=4)

    print("\n✅ User Registered Successfully!")