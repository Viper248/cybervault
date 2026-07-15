# venv\scripts\activate <--- run this first time
from flask import Flask, render_template, request, redirect, url_for
from auth.login import login_user
from auth.register import register_user

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        success = login_user(username, password)

        if success:
            return f"Welcome {username}! Login successful."
        else:
            return f"Login failed. Invalid credentials. <a href=\"{url_for('login')}\">Try again</a>"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        success = register_user(username, password)

        if success:
            return f"User registered successfully. <a href=\"{url_for('login')}\">Login</a>"
        else:
            return f"Registration failed. User already exists. <a href=\"{url_for('register')}\">Try again</a>"

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)