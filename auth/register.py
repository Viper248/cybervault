from utils.hashing import hash_password
from database.users import add_user

def register_user(username, password):
    hashed_pw = hash_password(password)
    return add_user(username, hashed_pw)
    