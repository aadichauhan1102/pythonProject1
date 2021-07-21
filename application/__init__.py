from flask import Flask

app = Flask(__name__)
app.secret_key = "testing"

from application import routes, db_connection
