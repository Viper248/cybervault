from utils.hashing import verify_password
from database.users import get_user
from utils.logger import log_event

def login_user(username, password):
    user = get_user(username)

    if not user:
        #log_event(f"Login failed for user: {username}")
        return False
    else:
        log_event(f"Login successful for user: {username}")
        return verify_password(password, user["password"]) 