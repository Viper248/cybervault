# venv\scripts\activate <--- run this first time
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, session
from auth.login import login_user
from auth.register import register_user
from database.users import get_user
from utils.logger import log_event

app = Flask(__name__)
app.secret_key = "supersecretkey"

MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_PERIOD = timedelta(minutes=5)
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

        if login_user(username, password):
            session["pending_user"] = username
            return redirect(url_for("login_otp"))

        attempts = login_attempts.get(username, 0) + 1
        login_attempts[username] = attempts

        if attempts >= MAX_LOGIN_ATTEMPTS:
            lockouts[username] = datetime.utcnow() + LOCKOUT_PERIOD
            login_attempts.pop(username, None)
            remaining = 0
            log_event(
                f"Login failed for user: {username}. Account locked after {attempts} failed attempts. Remaining attempts before lockout: {remaining}"
            )
            error = f"Too many failed attempts. Account locked for {int(LOCKOUT_PERIOD.total_seconds() // 60)} minutes."
        else:
            remaining = MAX_LOGIN_ATTEMPTS - attempts
            log_event(
                f"Login failed for user: {username}. Remaining attempts before lockout: {remaining}"
            )
            error = f"Login failed. Invalid credentials. {remaining} attempt(s) remaining."

    return render_template("login.html", error=error, username=username)


@app.route("/login-otp", methods=["GET", "POST"])
def login_otp():
    username = session.get("pending_user")
    if not username:
        return redirect(url_for("login"))

    error = None

    if request.method == "POST":
        otp = request.form.get("otp") or ""
        user = get_user(username)

        if not user or not user.get("otp"):
            error = "OTP not available for this account. Please login again."
            session.pop("pending_user", None)
            return render_template("login.html", error=error, username=username)

        if otp.strip().upper() == user.get("otp"):
            user["otp"] = None
            session.pop("pending_user", None)
            login_attempts.pop(username, None)
            return render_template("login_success.html", username=username)

        error = "Invalid OTP. Please try again."

    return render_template("otp_verification.html", username=username, error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username") or ""
        password = request.form.get("password") or ""

        if not username.strip() or not password:
            error = "Please fill out all fields before registering."
            return render_template("register.html", error=error, username=username)

        if len(username.strip()) < 3:
            error = "Username must be at least 3 characters."
            return render_template("register.html", error=error, username=username)

        if len(password) < 6:
            error = "Password must be at least 6 characters."
            return render_template("register.html", error=error, username=username)

        success, otp = register_user(username.strip(), password)
        if success:
            return render_template("registration_success.html", otp=otp)
        else:
            return render_template("registration_failed.html")

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)