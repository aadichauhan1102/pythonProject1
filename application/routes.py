from application import app, db_connection
from flask import render_template, request, session
import pymongo
import flask

connection_db = db_connection.db_connection()
db = connection_db.connect_to_mongodb()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cart", methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        price = request.form.get("price")
        packages = request.form.get("packages")
        print(price)
        travel_table = db["Travel_Packages"]
        travel_pck = {"_id": 12, "Package_name": packages, "Package_Price": price}
        try:
            travel_table.insert_one(travel_pck)
        except Exception as e:
            print("An exception occurred ::", e)
    return render_template("cart.html")


@app.route("/contactus")
def contactus():
    return render_template("contactus.html")


@app.route("/flightDetails")
def flightDetails():
    return render_template("flightDetails.html")


@app.route("/tourspackages")
def tourspackages():
    return render_template("tourspackages.html")


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


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
                name = email_found['name']
                return render_template("index.html", loggedIn=True, name=name)
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
