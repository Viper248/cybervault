from utils.logger import log_event

users = {}

def get_user(username):
    return users.get(username)

def add_user(username, hashed_password, otp):
    if username in users:
        return False

    users[username] = {
        "username": username,
        "password": hashed_password,
        "otp": otp
    }
    log_event(f"User added: {username} | verification code: {otp}")
    return True