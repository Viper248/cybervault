from utils.hashing import verify_password
from database.users import get_user

def login_user(username, password):
    user = get_user(username)

    if not user:
        return False  
    else:
        return verify_password(password, user["password"]) 