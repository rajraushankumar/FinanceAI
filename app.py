import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = "my_secret_key"


# ---------------- HOME ----------------
@app.route("/")
def home():
    name = "Rajraushan"
    return render_template("home.html", username=name)


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("finance.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        connection.close()

        if user and check_password_hash(user[3], password):

            print("User =", user)
            session["username"] = user[1]
            print("✅ Login Successful")
            return redirect(url_for("dashboard"))

        else:
            print("❌ Invalid Email or Password")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    # Total Income
    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE username=?",
        (session["username"],)
    )

    income = cursor.fetchone()[0] or 0

    # Total Expense
    cursor.execute(
        "SELECT SUM(amount) FROM expense WHERE username=?",
        (session["username"],)
    )

    expense = cursor.fetchone()[0] or 0

    connection.close()

    balance = income - expense

    return render_template(
        "dashboard.html",
        username=session["username"],
        income=income,
        expense=expense,
        balance=balance
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect(url_for("login"))


# ---------------- INCOME ----------------
@app.route("/income", methods=["GET", "POST"])
def income():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        amount = request.form["amount"]
        source = request.form["source"]

        print("Amount =", amount)
        print("Source =", source)

        connection = sqlite3.connect("finance.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO income(username, amount, source)
            VALUES (?, ?, ?)
            """,
            (session["username"], amount, source)
        )

        connection.commit()
        connection.close()

        print("✅ Income Saved Successfully")

    return render_template("income.html")


# ---------------- INCOME HISTORY ----------------
@app.route("/history")
def history():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM income WHERE username=?",
        (session["username"],)
    )

    incomes = cursor.fetchall()

    connection.close()

    return render_template(
        "history.html",
        incomes=incomes
    )


# ---------------- EXPENSE ----------------
@app.route("/expense", methods=["GET", "POST"])
def expense():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        amount = request.form["amount"]
        category = request.form["category"]

        print("Amount =", amount)
        print("Category =", category)

        connection = sqlite3.connect("finance.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO expense(username, amount, category)
            VALUES (?, ?, ?)
            """,
            (session["username"], amount, category)
        )

        connection.commit()
        connection.close()

        print("✅ Expense Saved Successfully")

    return render_template("expense.html")


# ---------------- EXPENSE HISTORY ----------------
@app.route("/expense_history")
def expense_history():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM expense WHERE username=?",
        (session["username"],)
    )

    expenses = cursor.fetchall()

    connection.close()

    return render_template(
        "expense_history.html",
        expenses=expenses
    )


# ---------------- BALANCE ----------------
@app.route("/balance")
def balance():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    # Total Income
    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE username=?",
        (session["username"],)
    )
    total_income = cursor.fetchone()[0]

    # Total Expense
    cursor.execute(
        "SELECT SUM(amount) FROM expense WHERE username=?",
        (session["username"],)
    )
    total_expense = cursor.fetchone()[0]

    connection.close()

    if total_income is None:
        total_income = 0

    if total_expense is None:
        total_expense = 0

    balance = total_income - total_expense

    return render_template(
        "balance.html",
        income=total_income,
        expense=total_expense,
        balance=balance
    )


# ---------------- MONTHLY REPORT ----------------
@app.route("/report")
def report():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    # Total Income
    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE username=?",
        (session["username"],)
    )
    income = cursor.fetchone()[0] or 0

    # Total Expense
    cursor.execute(
        "SELECT SUM(amount) FROM expense WHERE username=?",
        (session["username"],)
    )
    expense = cursor.fetchone()[0] or 0

    connection.close()

    balance = income - expense

    return render_template(
        "report.html",
        income=income,
        expense=expense,
        balance=balance
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match!"
        
        hashed_password = generate_password_hash(password)

        connection = sqlite3.connect("finance.db")
        cursor = connection.cursor()
       
        # Check if email already exists
        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        if user:
            connection.close()
            return "Email already registered!"

        # Save new user
        cursor.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, hashed_password)
        )

        connection.commit()
        connection.close()

        print("✅ User Registered Successfully")

        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)