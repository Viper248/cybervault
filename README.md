# CyberVault

A small educational cybersecurity project built while learning Python and web
authentication. It is a learning sandbox, **not** a production password manager
and not intended for real accounts or real secrets.

The project has two parts:

1. A minimal Flask web app that simulates a user login/registration flow.
2. A `miscPrjct/` folder of standalone scripts used to explore hashing and
   basic password-cracking concepts as classroom exercises.

## The Flask app

A single-server demo (`app.py`) covering a typical authentication flow:

- **Register** a username and password with basic input validation
  (username ≥ 3 chars, password ≥ 6 chars).
- Passwords are hashed with **bcrypt** before being stored — plaintext
  passwords are never kept.
- **Login** verifies credentials, then requires a one-time code (a simple
  simulated OTP step) before granting access.
- **Account lockout** after 5 failed login attempts, for 5 minutes.
- Events are written to a plain-text audit log at `logs/security.log`.
- An optional "themed" background toggle on the login screen. :)

### Important limitations

This is a teaching demo, so it deliberately cuts corners a real system would not:

- Users are stored **in memory** (`database/users.py`), so all accounts are
  lost when the server restarts. There is no real database.
- The Flask `secret_key` is hardcoded and `debug=True` is on.
- The OTP is generated on the server and shown/logged for the demo rather than
  being delivered out-of-band.

Do not deploy this or use it for anything you actually care about.

## Project layout

```
app.py              Flask routes (home, register, login, OTP, lockout)
auth/               login and registration logic
database/users.py   in-memory user store
utils/hashing.py    bcrypt hash/verify helpers
utils/logger.py     appends events to logs/security.log
templates/          HTML pages for each screen
static/             image assets
miscPrjct/          standalone learning scripts (see below)
common.txt          tiny sample wordlist for the dictionary-attack exercise
```

## miscPrjct — learning scripts

Self-contained exercises from earlier assignments, kept here for reference.
They are not imported by the Flask app and are meant to be run and read
individually to understand the underlying concepts:

- Hashing with bcrypt, argon2, and hashlib (MD5/SHA-256), and salting.
- Brute-force and dictionary password-guessing demos run against a password
  you supply, to illustrate why weak passwords fail and strong hashing matters.
- A password-strength check using `zxcvbn`.

## Run instructions

```bash
# create and activate a virtual environment (first time)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in a browser.

## Requirements

Python 3.11+. Dependencies (`requirements.txt`): `flask`, `bcrypt`,
`argon2-cffi`, `zxcvbn`.
