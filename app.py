import os

print("Database Path:", os.path.abspath("finance.db"))
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file,  Response
from flask import send_file
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/images"
app.secret_key = "my_secret_key"

app.config["UPLOAD_FOLDER"] = "static/images"


# ---------------- HOME ----------------
@app.route("/")
def home():

    return redirect(url_for("login"))


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
            session["user_id"] = user[0]
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

    # ---------------- TOTAL INCOME ----------------


    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE username=?",
        (session["username"],)
    )

    income_result = cursor.fetchone()
    income = income_result[0] if income_result and income_result[0] else 0
    
    # ---------------- TOTAL EXPENSE ----------------

    cursor.execute(
        "SELECT SUM(amount) FROM expense WHERE username=?",
        (session["username"],)
    )

    expense_result = cursor.fetchone()
    expense = expense_result[0] if expense_result and expense_result[0] else 0


    # ---------------- PROFILE PHOTO ----------------

    cursor.execute(
        "SELECT id, profile_photo FROM users WHERE id=?",
         (session["user_id"],)
    )
    user = cursor.fetchone()

    if user:
        profile_photo = user[1]
    else:
        profile_photo = None


    connection.close()


    # ---------------- BALANCE ----------------

    balance = income - expense

        # ---------------- AI INSIGHT ----------------

    if income == 0:

        insight = "⚠ Add your income to start financial tracking."

    elif expense == 0:

        insight = "🎉 Great! You haven't added any expense yet."

    elif expense > income:

        insight = "⚠ Your expenses are greater than your income."

    elif balance >= income * 0.5:

        insight = "💰 Excellent! You are saving more than 50% of your income."

    elif balance >= income * 0.2:

        insight = "👍 Good job! Your savings are on the right track."

    else:

        insight = "⚠ Try reducing unnecessary expenses to increase savings."



    print("SESSION USERNAME =", session["username"])
    print("PROFILE PHOTO =", profile_photo)


    return render_template(
        "dashboard.html",
        username=session["username"],
        income=float(income),
        expense=float(expense),
        balance=float(balance),
        profile_photo=profile_photo,
        insight=insight
    )



# ---------------- PROFILE ----------------
@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    if request.method == "POST":

        photo = request.files["profile_photo"]

        if photo and allowed_file(photo.filename):

            filename = secure_filename(photo.filename)

            photo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            cursor.execute(
                """
                UPDATE users
                SET profile_photo=?
                WHERE id=?
                """,
                (filename, session["user_id"])
            )

            connection.commit()

    connection.close()

    return redirect(url_for("dashboard"))

# ---------------- INCOME ----------------
@app.route("/income", methods=["GET", "POST"])
def income():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        amount = request.form["amount"]
        source = request.form["source"]
        date = request.form["date"]
        print("Amount =", amount)
        print("Source =", source)

        connection = sqlite3.connect("finance.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO income(username, amount, source, date)
            VALUES (?, ?, ?, ?)
            """,
            (session["username"], amount, source, date)
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

# ---------------- EDIT INCOME ----------------
@app.route("/edit_income/<int:id>", methods=["GET", "POST"])
def edit_income(id):

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    if request.method == "POST":

        amount = request.form["amount"]
        source = request.form["source"]
        date = request.form["date"]

        cursor.execute(
            """
            UPDATE income
            SET amount=?, source=?, date=?
            WHERE id=?
            """,
            (amount, source, date, id)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("history"))

    cursor.execute(
        "SELECT * FROM income WHERE id=?",
        (id,)
    )

    income = cursor.fetchone()

    connection.close()

    return render_template(
        "edit_income.html",
        income=income
    )

# ---------------- DELETE INCOME ----------------
@app.route("/delete_income/<int:id>")
def delete_income(id):

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM income WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("history"))


@app.route("/expense", methods=["GET", "POST"])
def expense():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]

        print("Amount =", amount)
        print("Category =", category)
        print("Date =", date)

        connection = sqlite3.connect("finance.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO expense(username, amount, category, date)
            VALUES (?, ?, ?, ?)
            """,
            (session["username"], amount, category, date)
        )

        connection.commit()
        connection.close()

        print("✅ Expense Saved Successfully")

        return redirect(url_for("expense_history"))

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

# ---------------- DELETE EXPENSE ----------------
@app.route("/delete_expense/<int:id>")
def delete_expense(id):

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expense WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("expense_history"))

# ---------------- EDIT EXPENSE ----------------
@app.route("/edit_expense/<int:id>", methods=["GET", "POST"])
def edit_expense(id):

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    if request.method == "POST":

        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]

        cursor.execute(
            """
            UPDATE expense
            SET amount=?, category=?, date=?
            WHERE id=?
            """,
            (amount, category, date, id)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("expense_history"))

    cursor.execute(
        "SELECT * FROM expense WHERE id=?",
        (id,)
    )

    expense = cursor.fetchone()

    connection.close()

    return render_template(
        "edit_expense.html",
        expense=expense
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

@app.route("/download_report")
def download_report():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE username=?",
        (session["username"],)
    )
    income = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT SUM(amount) FROM expense WHERE username=?",
        (session["username"],)
    )
    expense = cursor.fetchone()[0] or 0

    connection.close()

    balance = income - expense

    pdf = BytesIO()

    doc = SimpleDocTemplate(pdf)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Personal Finance Report</b>", styles["Title"]))
    story.append(Paragraph(f"User : {session['username']}", styles["Normal"]))
    story.append(Paragraph(f"Total Income : ₹{income}", styles["Normal"]))
    story.append(Paragraph(f"Total Expense : ₹{expense}", styles["Normal"]))
    story.append(Paragraph(f"Balance : ₹{balance}", styles["Normal"]))

    doc.build(story)

    pdf.seek(0)

    return send_file(
        pdf,
        download_name="Finance_Report.pdf",
        as_attachment=True,
        mimetype="application/pdf"
    )

    # ---------------- AI SUGGESTION ----------------
@app.route("/ai")
def ai():

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
    # Highest Expense Category

    cursor.execute(
        """
        SELECT category, SUM(amount)
        FROM expense
        WHERE username=?
        GROUP BY category
        ORDER BY SUM(amount) DESC
        LIMIT 1
        """,
        (session["username"],)
    )

    highest = cursor.fetchone()

    if highest:

        category = highest[0]
        spent = highest[1]

    else:

        category = "None"
        spent = 0

    connection.close()

    saving = income - expense

    # Saving Percentage
    if income > 0:
        saving_percent = round((saving / income) * 100, 1)
    else:
        saving_percent = 0

    # Financial Health Rating
    if saving_percent >= 50:
        rating = "⭐⭐⭐⭐⭐ Excellent"
    elif saving_percent >= 30:
        rating = "⭐⭐⭐⭐ Good"
    elif saving_percent >= 15:
        rating = "⭐⭐⭐ Average"
    else:
        rating = "⭐⭐ Needs Improvement"

    # Potential Savings
    potential = round(spent * 0.10, 2)

   # ---------------- AI Suggestion ----------------

    if income == 0:

        suggestion = (
            "⚠ No income found.\n"
            "Please add your income first."
        )

    elif expense > income:

        suggestion = (
            f"🚨 Financial Alert!\n\n"
            f"You spent ₹{expense:.0f} while your income is only ₹{income:.0f}.\n\n"
            f"Highest spending: {category} (₹{spent:.0f})\n\n"
            "Reduce unnecessary expenses immediately."
        )

    else:

        suggestion = (
            f"📊 AI Financial Report\n\n"
            f"Highest Expense Category : {category}\n"
            f"Amount Spent : ₹{spent:.0f}\n\n"
            f"Potential Monthly Savings : ₹{potential:.0f}\n\n"
            f"Saving Rate : {saving_percent}%\n"
            f"Financial Health : {rating}\n\n"
            "💡 Tip: Try reducing your highest expense category by at least 10% every month."
        )

        return render_template(
            "ai.html",
            income=income,
            expense=expense,
            saving=saving,
            category=category,
            spent=spent,
            suggestion=suggestion,
            saving_percent=saving_percent,
            rating=rating,
            potential=potential
        )
                
# ---------------- EXPORT CSV ----------------
@app.route("/export_csv")
def export_csv():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT amount, source, date
        FROM income
        WHERE username=?
        """,
        (session["username"],)
    )

    rows = cursor.fetchall()

    connection.close()

    output = "Amount,Source,Date\n"

    for row in rows:
        output += f"{row[0]},{row[1]},{row[2]}\n"

    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=income_report.csv"
        }
    )


    # ---------------- BUDGET PLANNER ----------------
@app.route("/budget", methods=["GET", "POST"])
def budget():

    if "username" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    if request.method == "POST":

        monthly_budget = request.form["monthly_budget"]

        cursor.execute(
            "SELECT * FROM budget WHERE username=?",
            (session["username"],)
        )

        data = cursor.fetchone()

        if data:

            cursor.execute(
                """
                UPDATE budget
                SET monthly_budget=?
                WHERE username=?
                """,
                (monthly_budget, session["username"])
            )

        else:

            cursor.execute(
                """
                INSERT INTO budget(username, monthly_budget)
                VALUES(?,?)
                """,
                (session["username"], monthly_budget)
            )

        connection.commit()

    # Budget
    cursor.execute(
        "SELECT monthly_budget FROM budget WHERE username=?",
        (session["username"],)
    )

    row = cursor.fetchone()

    budget = row[0] if row else 0

    # Expense
    cursor.execute(
        "SELECT SUM(amount) FROM expense WHERE username=?",
        (session["username"],)
    )

    expense = cursor.fetchone()[0] or 0

    connection.close()

    remaining = budget - expense

    if budget > 0:

        percent = (expense / budget) * 100

    else:

        percent = 0

    if percent >= 100:

        status = "🔴 Budget Exceeded"

    elif percent >= 80:

        status = "🟠 Budget Almost Finished"

    else:

        status = "🟢 Budget Under Control"

    return render_template(
        "budget.html",
        budget=budget,
        expense=expense,
        remaining=remaining,
        percent=round(percent,1),
        status=status
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


@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404

# ---------------- CREATE BUDGET TABLE ----------------

connection = sqlite3.connect("finance.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS budget(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    monthly_budget REAL
)
""")

connection.commit()
connection.close()

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)