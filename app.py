# venv\scripts\activate <--- run this first time
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for
from auth.login import login_user
from auth.register import register_user

app = Flask(__name__)

MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_PERIOD = timedelta(minutes=10)
login_attempts = {}
lockouts = {}
 

def get_lockout_expiry(username):
    expiry = lockouts.get(username)
    if not expiry:
        return None

    if expiry <= datetime.utcnow():
        lockouts.pop(username, None)
        return None

    return expiry


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    username = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        expiry = get_lockout_expiry(username)
        if expiry:
            remaining = expiry - datetime.utcnow()
            minutes = int(remaining.total_seconds() // 60) + 1
            error = f"Account locked. Try again in {minutes} minute(s)."
            return render_template("login.html", error=error, username=username)

        success = login_user(username, password)
        if success:
            login_attempts.pop(username, None)
            return render_template("login_success.html", username=username)

        attempts = login_attempts.get(username, 0) + 1
        login_attempts[username] = attempts

        if attempts >= MAX_LOGIN_ATTEMPTS:
            lockouts[username] = datetime.utcnow() + LOCKOUT_PERIOD
            login_attempts.pop(username, None)
            error = f"Too many failed attempts. Account locked for {int(LOCKOUT_PERIOD.total_seconds() // 60)} minutes."
        else:
            remaining = MAX_LOGIN_ATTEMPTS - attempts
            error = f"Login failed. Invalid credentials. {remaining} attempt(s) remaining."

    return render_template("login.html", error=error, username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        success = register_user(username, password)

        if success:
            return render_template("registration_success.html")
        else:
            return render_template("registration_failed.html")

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)