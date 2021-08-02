from flask import Flask
from flask_session.__init__ import Session

app = Flask(__name__,template_folder='templates')
app.secret_key = "testing"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

from application import routes, db_connection
