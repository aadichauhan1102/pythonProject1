from application import app, db_connection
from flask import render_template, request, session, redirect


connection_db = db_connection.db_connection()
db = connection_db.connect_to_mongodb()

#render to index
@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', loggedIn=session.get('loggedIn'), name=session.get('name'))

#render to packages
@app.route("/tourspackages")
def tourspackages():
    if not session.get('loggedIn'):
        return redirect("/loginpage")
    return render_template("tourspackages.html",  loggedIn=session.get('loggedIn'), name=session.get('name'))


@app.route("/cart", methods=['GET', 'POST'])
def cart(travel_pck={}):
    if not session.get('loggedIn'):
        return redirect("/loginpage")
    if request.method == 'POST':
        price = request.form.get("price")
        packages = request.form.get("packages")
        people = request.form.get("people")
        print("cart", price, packages, people)
        total = int(price.lstrip('$'))*int(people)
        travel_table = db["cart"]
        travel_pck = {"Package_name": packages, "Package_Price_per_person": price,
                      "total_people": people, "total_price": total}
        try:
            travel_table.insert_one(travel_pck)
        except Exception as e:
            print("An exception occurred ::", e)
    return render_template("cart.html", travel_pck=travel_pck,  loggedIn=session.get('loggedIn'), name=session.get('name'))


@app.route("/contactus")
def contactus():
    if not session.get('loggedIn'):
        return redirect("/loginpage")
    return render_template("contactus.html", loggedIn=session.get('loggedIn'), name=session.get('name'))


@app.route("/booking")
def booking():
    if not session.get('loggedIn'):
        return redirect("/loginpage")
    return render_template("booking.html",  loggedIn=session.get('loggedIn'), name=session.get('name'))


@app.route("/flightDetails")
def flightDetails():
    if not session.get('loggedIn'):
        return redirect("/loginpage")
    return render_template("flightDetails.html",  loggedIn=session.get('loggedIn'), name=session.get('name'))

#returns aboutus is page in the session
@app.route("/aboutus")
def aboutus():
    if not session.get('loggedIn'):
        return redirect("/loginpage")
    return render_template("aboutus.html",  loggedIn=session.get('loggedIn'), name=session.get('name'))

#returns login is page in the session and verify email passwordd
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
                session["name"] = name
                session['loggedIn'] = True
                return render_template("index.html", loggedIn=True, name=name)
            else:
                msg = 'Wrong password'
                session["name"] = None
                session['loggedIn'] = False
                return render_template('loginpage.html', loggedIn=False, msg=msg)
        else:
            msg = 'Email not found'
            return render_template('loginpage.html', loggedIn=False, msg=msg)
    return render_template("loginpage.html", loggedIn=False)


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


@app.route("/logout")
def logout():
    if session.get("name"):
        session['name'] = None
        session['loggedIn'] = False
        return redirect("/")
    return render_template("index.html")

