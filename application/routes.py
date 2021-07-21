from application import app, db_connection
from flask import render_template, request, session

connection_db = db_connection.db_connection()
db = connection_db.connect_to_mongodb()


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/")
def packages():
    return render_template("tourpackages.html")

@app.route("/loginpage", methods=['GET', 'POST'])
def loginpage():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        custTable = db["customers"]
        email_found = custTable.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            password_val = email_found['password']
            if password == password_val:
                session["email"] = email_val
                return render_template("index.html", loggedIn=True)
            else:
                msg = 'Wrong password'
                return render_template('loginpage.html', msg=msg)
        else:
            msg = 'Email not found'
            return render_template('loginpage.html', msg=msg)
    return render_template("loginpage.html")


@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        custTable = db["customers"]
        new_cust = {"email": email, "password": password, "name": name}
        try:
            custTable.insert_one(new_cust)
        except Exception as e:
            print("An exception occurred ::", e)
        return render_template("loginpage.html", msg="Customer successfully created!!!")
