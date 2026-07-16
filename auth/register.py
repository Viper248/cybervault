import random
import string

from utils.hashing import hash_password
from database.users import add_user

OTP_CHARS = string.ascii_uppercase + string.digits
OTP_LENGTH = 3

def generate_otp():
    return ''.join(random.choices(OTP_CHARS, k=OTP_LENGTH))

def register_user(username, password):
    hashed_pw = hash_password(password)
    otp = generate_otp()
    success = add_user(username, hashed_pw, otp)
    if not success:
        return False, None
    return True, otp
    